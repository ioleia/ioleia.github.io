"""Pixelwise matte/paint treatment of the approved flattened raster; no tracing/resampling."""
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw
import hashlib, json, argparse
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
source = ROOT/'assets/ioleia-a2-1-approved-symbol.png'
assert hashlib.sha256(source.read_bytes()).hexdigest() == 'bd5d4bf145f3245ddcaf07ae32197c2ae91a11e1e353fff5010a026e8dde0caa'
im = Image.open(source).convert('RGB')
parser=argparse.ArgumentParser()
parser.add_argument('--board',type=Path,required=True,help='Original approved A2.1 board')
args=parser.parse_args()
assert hashlib.sha256(args.board.read_bytes()).hexdigest()=='f2259727a4926afd49f01936d8ed01609b34a6c6f6f7710fee17621f69fafccf'
assert Image.open(args.board).convert('RGB').crop((770,100,1120,450)).tobytes()==im.tobytes()
# The source is flattened RGB, so latent authoring alpha cannot be recovered.
# Map source luminance directly to coverage, without moving or filtering pixels.
# 233 is below the measured background-only luminance minimum; 23 is black ink.
# The midpoint is exactly 128, preserving the original visible 50% contour.
lum = np.array(im.convert('L')).astype(float)
alpha = np.rint(np.clip((233-lum)/210, 0, 1)*255).astype('uint8')
rgba = np.zeros((im.height, im.width, 4), dtype='uint8')
rgba[:,:,:3] = (248,241,232)
rgba[:,:,3] = alpha
result = Image.fromarray(rgba, 'RGBA')
output = ROOT/'assets/ioleia-a2-1-header-ivory.png'
result.save(output)
checks=[]
for threshold in [1,32,64,128,192,224,254]:
    source_mask = np.rint(np.clip((233-lum)/210,0,1)*255)>=threshold
    result_mask = np.array(Image.open(output))[:,:,3]>=threshold
    checks.append({'alpha_threshold':threshold,'changed_pixel_coordinates':int((source_mask!=result_mask).sum())})
visible = alpha>=128
original_visible = lum<=128
assert np.array_equal(visible,original_visible)
y,x=np.where(visible)
record={'board_sha256':hashlib.sha256(args.board.read_bytes()).hexdigest(),'board_crop':[770,100,1120,450],'board_crop_pixel_differences':0,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'output_sha256':hashlib.sha256(output.read_bytes()).hexdigest(),
        'source_size':list(im.size),'output_size':list(result.size),
        'method':'pixelwise alpha=round(255*clamp((233-L)/210)); RGB=(248,241,232), L=Pillow RGB-to-L',
        'no_resampling_tracing_smoothing_dilation_or_erosion':True,
        'visible_contour_mask_differences':int((visible!=original_visible).sum()),
        'visible_bounds_exclusive':[int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)],
        'transparent_pixels':int((alpha==0).sum()),'partially_transparent_pixels':int(((alpha>0)&(alpha<255)).sum()),
        'mask_checks':checks,
        'limitation':'Original is flattened RGB, not an authored alpha mask. This preserves source pixel positions and the exact visible 50% contour (inclusive luminance 128); original latent subpixel coverage cannot be proved. Pale matte is keyed out and remaining edge gradations are mapped directly, never traced or spatially filtered.'}
(ROOT/'docs/brand/HEADER-MATTE-2026-11-02-v1.json').write_text(json.dumps(record,indent=2)+'\n')
canvas=Image.new('RGB',(1050,390),(9,9,43))
canvas.paste(im,(0,30)); canvas.paste(result,(350,30),result)
# Compare the original and resulting visible masks: white means agreement.
mask=np.zeros((350,350,3),dtype='uint8'); mask[visible]=255
canvas.paste(Image.fromarray(mask),(700,30))
d=ImageDraw.Draw(canvas); d.text((8,8),'APPROVED SOURCE',fill='white');d.text((358,8),'IVORY + TRANSPARENCY',fill='white');d.text((708,8),'VISIBLE MASK: 0 CHANGED PIXELS',fill='white')
canvas.save(ROOT/'docs/brand/header-matte-comparison.png')
print(json.dumps(record,indent=2))
