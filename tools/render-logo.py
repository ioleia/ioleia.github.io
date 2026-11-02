"""Render the locked A2.1 path; never redraw, simplify, or transform it."""
from pathlib import Path
import hashlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
master = ROOT / 'docs/brand/ioleia-a2-1-master-monochrome.svg'
assert hashlib.sha256(master.read_bytes()).hexdigest() == '91d8887574fdd73d124d251d641b6a23e2ce256a63ee71ffdb9db33c0511de98'
path = ET.parse(master).find('.//{*}path').get('d')
assert hashlib.sha256(path.encode()).hexdigest() == '8fc6f627c8fe07d7985e6a1beeb8a067da87d8ec4190c0ee89bb477eb2091086'

# Light and texture are composited INSIDE the exact even-odd clip. The final
# clip preserves every hole, the outer contour, and the right-side handoff.
svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 350 350" role="img" aria-labelledby="title desc">
  <title id="title">Ioleia A2.1 luminous orb</title>
  <desc id="desc">Two flowing presences in amber, magenta, cyan and violet. Rendering of the unchanged a2.1-trace-1 geometry.</desc>
  <metadata>Geometry SHA-256: 8fc6f627c8fe07d7985e6a1beeb8a067da87d8ec4190c0ee89bb477eb2091086. Rendering v1. No new silhouette or ribbons.</metadata>
  <defs>
    <path id="a21-geometry" fill-rule="evenodd" clip-rule="evenodd" d="PATH"/>
    <clipPath id="locked"><use href="#a21-geometry"/></clipPath>
    <linearGradient id="colour" x1="0" y1="0" x2="1" y2=".4">
      <stop stop-color="#ffc17a"/><stop offset=".28" stop-color="#ffb365"/>
      <stop offset=".58" stop-color="#e882db"/><stop offset="1" stop-color="#a183ff"/>
    </linearGradient>
    <linearGradient id="cool" x1=".2" y1=".45" x2=".8" y2="1">
      <stop stop-color="#6ef2ff"/><stop offset=".4" stop-color="#52caff"/>
      <stop offset=".75" stop-color="#708aff"/><stop offset="1" stop-color="#b28aff"/>
    </linearGradient>
    <linearGradient id="lower-fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset=".52" stop-color="black"/><stop offset=".59" stop-color="white"/>
    </linearGradient>
    <mask id="lower"><rect width="350" height="350" fill="url(#lower-fade)"/></mask>
    <radialGradient id="rim" cx="177" cy="177" r="163" gradientUnits="userSpaceOnUse">
      <stop offset=".89" stop-color="white"/><stop offset=".95" stop-color="#888"/>
      <stop offset=".99" stop-color="#555"/><stop offset="1" stop-color="#444"/>
    </radialGradient>
    <mask id="restrained-rim"><rect width="350" height="350" fill="url(#rim)"/></mask>
    <radialGradient id="depth" cx=".4" cy=".3" r=".76">
      <stop stop-color="#100d30" stop-opacity=".04"/><stop offset=".6" stop-color="#0b0b31" stop-opacity=".1"/>
      <stop offset=".88" stop-color="#0b0b31" stop-opacity=".55"/><stop offset="1" stop-color="#05091e" stop-opacity=".78"/>
    </radialGradient>
    <radialGradient id="handoff" gradientUnits="userSpaceOnUse" cx="309" cy="160" r="9">
      <stop stop-color="#fff0d6" stop-opacity=".95"/><stop offset=".15" stop-color="#ffd9b2" stop-opacity=".65"/>
      <stop offset=".5" stop-color="#ecb8ed" stop-opacity=".14"/><stop offset="1" stop-color="#eeb3ec" stop-opacity="0"/>
    </radialGradient>
    <filter id="silk" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency=".008 .24" numOctaves="2" seed="21" result="noise"/>
      <feColorMatrix in="noise" type="matrix" values="0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 .65 .65 .65 0 -.58" result="veils"/>
      <feComposite in="SourceGraphic" in2="veils" operator="in"/>
    </filter>
    <filter id="inner-light" x="-10%" y="-10%" width="120%" height="120%">
      <feGaussianBlur stdDeviation="3.2"/>
    </filter>
    <radialGradient id="glass" cx=".3" cy=".2" r=".85">
      <stop stop-color="#fff0d9" stop-opacity=".65"/><stop offset=".3" stop-color="#ffd9ed" stop-opacity=".08"/>
      <stop offset=".65" stop-color="#a1abff" stop-opacity=".05"/><stop offset="1" stop-color="#8bd8fa" stop-opacity=".38"/>
    </radialGradient>
  </defs>
  <g clip-path="url(#locked)">
    <g mask="url(#restrained-rim)">
      <g id="warm-light">
        <use href="#a21-geometry" fill="url(#colour)" opacity=".08"/>
        <use href="#a21-geometry" fill="url(#colour)" opacity=".28" filter="url(#silk)"/>
        <use href="#a21-geometry" fill="none" stroke="url(#colour)" stroke-width="16" opacity=".5" filter="url(#inner-light)"/>
        <use href="#a21-geometry" fill="none" stroke="url(#colour)" stroke-width="1.7" opacity=".9"/>
        <use href="#a21-geometry" fill="none" stroke="url(#colour)" stroke-width="7" opacity=".14"/>
        <use href="#a21-geometry" fill="none" stroke="url(#colour)" stroke-width="13" opacity=".10"/>
      </g>
      <g mask="url(#lower)">
        <use href="#a21-geometry" fill="url(#cool)" opacity=".15"/>
        <use href="#a21-geometry" fill="url(#cool)" opacity=".32" filter="url(#silk)"/>
        <use href="#a21-geometry" fill="none" stroke="url(#cool)" stroke-width="16" opacity=".8" filter="url(#inner-light)"/>
        <use href="#a21-geometry" fill="none" stroke="url(#cool)" stroke-width="1.7"/>
        <use href="#a21-geometry" fill="none" stroke="url(#cool)" stroke-width="7" opacity=".2"/>
        <use href="#a21-geometry" fill="none" stroke="url(#cool)" stroke-width="13" opacity=".13"/>
      </g>
      <use href="#a21-geometry" fill="url(#depth)" opacity=".35"/>
      <use href="#a21-geometry" fill="none" stroke="url(#glass)" stroke-width=".8"/>
    </g>
    <use href="#a21-geometry" fill="url(#handoff)"/>
  </g>
</svg>
'''.replace('PATH', path)
(ROOT / 'assets/ioleia-a2-1-luminous.svg').write_text(svg)
print('Rendered luminous SVG from the verified canonical A2.1 path.')
