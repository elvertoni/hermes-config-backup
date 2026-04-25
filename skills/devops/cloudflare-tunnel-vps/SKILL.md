---
name: cloudflare-tunnel-vps
description: Gerenciar Cloudflare Tunnel na VPS Contabo — config remotely-managed, adicionar hostnames públicos, debugging de ingress rules.
version: 1.0.0
---

# Cloudflare Tunnel — VPS Contabo

Túnel Cloudflare na VPS é **remotely-managed** — as regras de ingress são controladas pelo dashboard (one.dash.cloudflare.com), NÃO pelo YAML local.

## Detalhes do túnel

- **Tunnel ID:** `c491d088-b884-46e5-a787-67a594ff715d`
- **Systemd service:** `cloudflared-hermes`
- **Config local:** `/root/.cloudflared/hermes-terminal.yml` (APENAS tunnel ID + credentials, ingress é ignorado)
- **Rotas atuais:** `obsidian.tonicoimbra.com:8081`, `terminal.tonicoimbra.com:7681`
- **Serviços systemd:** `hermes-newsletter` (HTTP :8082 — Python http.server servindo `/root/.hermes/cron/output/`)

## Adicionar novo hostname

1. **Dashboard Cloudflare** → Zero Trust → Networks → Tunnels → hermes-terminal → Configure
2. Aba **Public Hostname** → Add
3. Subdomain, Domain, Service (HTTP + localhost:PORT)

⚠️ NUNCA use `cloudflared tunnel route dns` ANTES de adicionar no dashboard — isso cria o CNAME sem a regra de ingress, causando conflito. Se já fez isso, delete o CNAME pelo DNS dashboard primeiro.

## Pitfalls

- Alterar o YAML local (`ingress:`) **não tem efeito** — o túnel carrega config dos servidores Cloudflare
- DNS CNAME pré-existente bloqueia a adição de Public Hostname no dashboard → deletar CNAME primeiro
- O comando `cloudflared tunnel route dns` NÃO adiciona regra de ingress, apenas DNS

## Debug

```bash
# Logs
sudo journalctl -u cloudflared-hermes --no-pager -n 20

# Status do túnel
cloudflared tunnel info hermes-terminal

# Ver config carregada (remota)
sudo journalctl -u cloudflared-hermes --no-pager -n 5 | grep "Updated to new"
```
