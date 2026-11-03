# Ioleia public website — prepared, AWS pending

**PR #2 remains draft and must not merge yet.** On 2 November 2026, the founder chose to keep AWS changes pending. No signup infrastructure or contact records were created. The existing GitHub Pages site remains unchanged.

The reviewed draft preserves the plain midnight navy background, centered luminous orb, frozen three-message copy/crossfade and one fixed email-only signup. The header/favicon now use a transparent warm-ivory mark derived directly from the approved A2.1 source raster. No generated substitute, tracing, resampling or silhouette filtering is involved.

`index.html` deliberately retains the two draft-only labels. `signup-config.js` has no endpoint, so the form stays disabled and never simulates success. `site.js` contains the real POST behavior for a future verified endpoint. Failure retains the entered email; valid submissions get a generic response, including duplicates. No checkbox or first name is collected.

The exact prepared disclosure is: **By joining, you agree to receive launch updates from Ioleia Inc. Unsubscribe anytime.** Version: `ioleia-early-access-v3-2026-11-02`. It is not live and is not a legal-compliance determination. The adjacent Early Access Privacy link describes only the proposed register. Counsel review, including mailing/contact disclosure and unsubscribe handling, remains required before any commercial launch email.

See [current validation](docs/review/CURRENT-VALIDATION.md), [current source manifest](docs/review/current-source-manifest.json), [header comparison](docs/brand/header-matte-comparison.png), and the [bounded backend package](deployment/early-access/README.md).

## Production preparation

`tools/build-production.py` requires an exact `https://<api-id>.execute-api.ca-central-1.amazonaws.com/early-access` endpoint and a new output directory. It removes preview-only labels/noindex and allows only that API origin in CSP. It does not deploy, verify AWS, or authorize release. Do not publish a test-fixture endpoint.

Hosting stays on GitHub Pages. Preserve CNAME and all DNS/email records. No Sites hosting registration, AWS hosting migration, CRM service, dashboard, tracker or mail sender is included.

## Verification scope

The focused browser suite tests a local production-build fixture with intercepted API responses. It does not create AWS records or prove live CORS, encryption, or provider logging. The separate Python suite uses fake storage/encryption clients. Current results and limitations are explicit in the validation record. Historical evidence lives under `docs/review/history/` and older brand documents are marked historical.

`real_data_admission=false`; all God Agent core Alpha gates remain untouched.
