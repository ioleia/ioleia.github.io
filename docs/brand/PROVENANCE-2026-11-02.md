# Brand provenance — preview v1, 2 November 2026

## Established references

- Geometry: A2.1, `a2.1-trace-1`; the canonical master is copied unchanged to `ioleia-a2-1-master-monochrome.svg`.
- Master SHA-256: `91d8887574fdd73d124d251d641b6a23e2ce256a63ee71ffdb9db33c0511de98`.
- Locked path SHA-256: `8fc6f627c8fe07d7985e6a1beeb8a067da87d8ec4190c0ee89bb477eb2091086`.
- Original source: [canonical A2.1 package](https://github.com/ioleia/god-agent/tree/4533ae01ac54341b0fc082fd72a734a9ba08e054/docs/brand/a2-1-master). The header/footer/favicon use the unchanged dark-background monochrome export from that package.
- Rendering reference: **Ioleia Light Field Brand System.png**, 1536 × 1024, downloaded from generated image 23 in [Oct 31 Chat](https://chatgpt.com/c/6ae61e79-034c-83ea-b42d-9539fbe8d978) on 2 November 2026. This is the latest board with the orb, resting and active Light Field panels, and the approved palette family.

## What this implementation does

`assets/reference/approved-light-field-board.png` preserves the downloaded bytes. CSS presents only the orb and the interior of the resting Light Field panel. No image was regenerated, retraced, repainted, or substituted with `colour-v1`. The source board's wordmark/tagline are outside both display windows. This board is a rendering reference, not a new permanent combined logo asset.

The orb window is approximately source x=120, y=20, width=395, height=375 at scale 0.4. A soft edge mask removes the rectangular source background; brightness 0.81 and saturation 0.84 calm the page presentation. The source orb itself is neither warped nor redrawn. The field window is source x=640, y=130, width=820, height=240; CSS stretches this atmospheric layer to its container and moves it slowly. This field does not define logo geometry.

The earlier cached 518-pixel board thumbnail was used only during initial layout and was replaced before the final review captures. It is not in this branch.

## Status and limits

A2.1 remains the geometry authority. Preserving the approved generated artwork does **not** prove that its pixels conform exactly to the canonical vector. This branch does not promote the generated board to a production master or claim a new geometry qualification. A faithful optimized production export can be prepared against the unchanged A2.1 reference after visual review, without reopening logo design.

Wordmark: live provisional Georgia/system-serif text, separate from the orb. No permanent font has been selected or licensed. The approved monochrome mark is unchanged at favicon size; its fine handoff is not claimed to be fully resolved at 16–24 pixels.

Rejected `colour-v1` assets are absent. No new brand decision is made by this implementation. Asset checksums are in `asset-hashes.json`.
