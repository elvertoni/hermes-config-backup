import re, sys, zipfile
from xml.etree import ElementTree as ET
src, out = sys.argv[1], sys.argv[2]
ns = {'a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
lines=[]
with zipfile.ZipFile(src) as z:
    for name in sorted(n for n in z.namelist() if n.startswith('ppt/slides/slide') and n.endswith('.xml')):
        root=ET.fromstring(z.read(name))
        texts=[]
        for t in root.findall('.//a:t', ns):
            if t.text:
                texts.append(t.text)
        line=' '.join(texts).strip()
        if line:
            lines.append(f'[{name}] {line}')
text='\n'.join(lines)
text=re.sub(r'\s+',' ',text)
open(out,'w').write(text)
print(out)
