"""Build only into a separate directory after deployment and verification of a real API."""
import argparse, json, re
from pathlib import Path
from shutil import copy2, copytree
from urllib.parse import urlsplit
p=argparse.ArgumentParser()
p.add_argument('--endpoint',required=True)
p.add_argument('--output',required=True,type=Path)
a=p.parse_args()
if not re.fullmatch(r'https://[a-z0-9]+\.execute-api\.ca-central-1\.amazonaws\.com/early-access',a.endpoint):
    p.error('Use the verified ca-central-1 API Gateway /early-access endpoint.')
r=Path(__file__).resolve().parents[1]
out=a.output.resolve()
if out == r or out.exists():
    p.error('Use a new output directory; source and previous builds are preserved.')
consent=json.loads((r/'docs/signup-consent-contract.json').read_text())
h=(r/'index.html').read_text()
assert consent['text'] in h
out.mkdir(parents=True)
for asset in ['ioleia-a2-1-header-ivory.png','ioleia-luminous-orb-centered.png']:
    (out/'assets').mkdir(exist_ok=True)
    copy2(r/'assets'/asset,out/'assets'/asset)
for file in ['CNAME','styles.css','site.js']:
    copy2(r/file,out/file)
origin=urlsplit(a.endpoint)
origin=origin.scheme+'://'+origin.netloc
h=h.replace("connect-src 'none'",'connect-src '+origin)
h=re.sub(r'^.*<meta name="robots".*\n','',h,flags=re.M)
h=re.sub(r'^.*class="[^\"]*preview-only[^\"]*".*\n','',h,flags=re.M)
assert 'preview-only' not in h and 'Signups are not live' not in h and 'Nothing is sent or saved' not in h
(out/'index.html').write_text(h)
privacy=(r/'early-access-privacy.html').read_text()
privacy=re.sub(r'^.*class="draft-note".*\n','',privacy,flags=re.M)
(out/'early-access-privacy.html').write_text(privacy)
(out/'signup-config.js').write_text("'use strict';\nwindow.IOLEIA_SIGNUP = Object.freeze("+json.dumps({'endpoint':a.endpoint,'consentVersion':consent['consent_version']})+");\n")
(out/'.nojekyll').touch()
print('Production build prepared at '+str(out)+'. This does not verify or deploy the endpoint.')
