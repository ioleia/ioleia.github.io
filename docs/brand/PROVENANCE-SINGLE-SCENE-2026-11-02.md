# A2.1 luminous rendering — single-scene refinement, 2 November 2026

This supersedes the cropped-orb implementation described in `PROVENANCE-2026-11-02.md`, which is retained as historical evidence. A2.1 geometry is fixed. Rendering may change; geometry may not.

## Source and exact geometry

The website's displayed orb and favicon now use `assets/ioleia-a2-1-luminous.svg`. The hero does not crop the brand board. The board remains only a decorative Light Field reference.

The canonical source is `docs/brand/ioleia-a2-1-master-monochrome.svg`, verified byte-for-byte against the archived file in `ioleia/god-agent` at commit `4533ae01ac54341b0fc082fd72a734a9ba08e054`.

- Canonical file SHA-256: `91d8887574fdd73d124d251d641b6a23e2ce256a63ee71ffdb9db33c0511de98`.
- Exact `d` attribute SHA-256: `8fc6f627c8fe07d7985e6a1beeb8a067da87d8ec4190c0ee89bb477eb2091086`.
- ViewBox remains `0 0 350 350`; even-odd fill and clip rules remain unchanged.
- The new SVG contains one path definition, copied verbatim. Every rendered layer uses that path. The compound path's five subpaths remain intact; they encode the existing outer boundary and negative spaces, not five ribbons.
- No retracing, path simplification, coordinate transform, generated logo concept, or rejected colour-v1 source is used.

## Rendering

`python3 tools/render-logo.py` reproducibly creates the asset after checking the canonical file and path hashes. The unchanged path is the final clip. Amber-to-magenta/violet light, cyan-to-blue/violet light, seeded translucent texture, soft inner-edge light, fine glass highlights, a restrained rim mask, and a small right-side highlight are applied inside it. The render is static; only three decorative CSS layers move on the page. No animated SVG filter or WebGL is used.

The two flowing presences, right-side handoff and transparent negative space remain those of the locked master. There is no third ribbon. Clipping all light preserves the negative space rather than blurring into it.

## Validation and status

Direct path-string comparison and SHA-256 match pass. At 700×700, the browser raster comparison counted 79,671 canonical pixels, zero rendered pixels outside the canonical silhouette, and zero missing opaque interior pixels. Side-by-side visual review against the monochrome export confirms the same contour, handoff and two-flow arrangement. The comparison and full-scene captures are delivered with the exact final PR-head review bundle.

This is the deterministic luminous rendering implemented for founder review, not a newly approved logo geometry or a claim that it reproduces every atmospheric pixel of the generated brand board. The geometry is established; the new rendering remains reviewable. Wordmark typography remains provisional.
