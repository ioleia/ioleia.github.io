# Preview validation — 2 November 2026

## Final simplified source review

The founder-review branch was simplified after the first browser-validation pass.

Current page structure:

- one continuous scrolling page;
- no section navigation tabs;
- hero email signup above the fold;
- one short honesty section;
- bottom email signup repeating the same action;
- no feature/principles grid;
- no Light Field explanation;
- no first-name field;
- no consent checkbox;
- no “See the light respond” interaction;
- no marketing CTA other than **Join early access**.

## Static safeguards retained

- One H1 and two H2 headings.
- Skip link, header/main/footer landmarks, visible email placeholders plus programmatic labels, decorative light excluded from the accessibility tree.
- Both email inputs are required and use native email validation.
- Both preview submit buttons are disabled in HTML and enabled only by the local script.
- Valid preview submission is prevented locally, clears the entered email, and announces that nothing was sent or saved.
- No form endpoint, fetch/XHR, analytics, cookies, storage API, or third-party font is present.
- CSP keeps `connect-src 'none'` and `form-action 'none'`.
- Reduced-motion CSS removes animation and transitions.
- A visible pause-motion control remains for ordinary motion settings.
- Hidden-tab and offscreen animation pausing remain.
- Responsive rules cover narrow mobile through desktop layouts; email/button rows stack on small screens.
- Canonical A2.1/brand assets are unchanged.
- `CNAME` is unchanged.
- No deployment workflow or AWS configuration is added.

## Evidence distinction

The earlier desktop/tablet/phone screenshots in this folder were produced for the prior, more complex page and are preserved as historical review evidence only.

They are **not** evidence that the final simplified layout has received founder visual approval.

The final source reuses the same already-reviewed visual implementation primitives, but the changed layout should still be viewed by the founder before merge/deployment. Do not manufacture a browser PASS for a viewport that was not actually re-run.

## Consent / subscription boundary

Founder UX direction is email-only submission without a separate checkbox. The design-only consent record documents the intended affirmative action, but production legal/CASL sufficiency remains for counsel/final launch review.

The preview stores and sends nothing.

## Live boundary

Draft PR #2 remains unmerged. No live website, DNS, email records, AWS, SES, Cognito, Apple, or production system is changed by this preview source.
