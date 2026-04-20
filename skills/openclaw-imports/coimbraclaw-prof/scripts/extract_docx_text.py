import re
import sys
import zipfile
from xml.etree import ElementTree as ET

src = sys.argv[1]
out = sys.argv[2]
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
with zipfile.ZipFile(src) as z:
    xml = z.read('word/document.xml')
root = ET.fromstring(xml)
lines = []
for p in root.findall('.//w:p', ns):
    texts = []
    for t in p.findall('.//w:t', ns):
        texts.append(t.text or '')
    line = ''.join(texts).strip()
    if line:
        lines.append(line)
text = '\n'.join(lines)
text = re.sub(r'\n{3,}', '\n\n', text)
open(out, 'w').write(text)
print(out)
