"""Guard the canonical logo geometry and its use on the page."""
from pathlib import Path
import hashlib
import xml.etree.ElementTree as E

root = Path(__file__).resolve().parents[1]
master = root / 'docs/brand/ioleia-a2-1-master-monochrome.svg'
rendered = root / 'assets/ioleia-a2-1-luminous.svg'
assert hashlib.sha256(master.read_bytes()).hexdigest() == '91d8887574fdd73d124d251d641b6a23e2ce256a63ee71ffdb9db33c0511de98'
a, b = E.parse(master), E.parse(rendered)
assert a.getroot().get('viewBox') == b.getroot().get('viewBox') == '0 0 350 350'
original = a.find('.//{*}path')
paths = b.findall('.//{*}path')
assert len(paths) == 1
assert paths[0].attrib == original.attrib
assert hashlib.sha256(paths[0].get('d').encode()).hexdigest() == '8fc6f627c8fe07d7985e6a1beeb8a067da87d8ec4190c0ee89bb477eb2091086'
assert not any(node.get('transform') for node in b.iter())
assert all(node.get('href') == '#a21-geometry' for node in b.findall('.//{*}use'))
assert b.getroot()[-1].get('clip-path') == 'url(#locked)'
assert len(b.findall('.//{*}image')) == 0
html = (root / 'index.html').read_text()
assert html.count('./assets/ioleia-a2-1-luminous.svg') == 2
assert 'approved-light-field-board' not in html
print('PASS: canonical file, exact path, viewBox, fill/clip rules, negative-space clip, no transforms/new paths/raster, hero + favicon reference.')
