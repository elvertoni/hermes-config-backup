#!/usr/bin/env python3
"""Wrapper: runs hermes-newsletter/collect.py for cron job context injection."""
import sys
sys.path.insert(0, "/root/.hermes/scripts/hermes-newsletter")
import collect
collect.main()
