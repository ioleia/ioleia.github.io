# Preview validation — 2 November 2026

## Browser checks completed

- Responsive layouts at 320, 390, 768, 1024, and 1440 CSS pixels: no horizontal document overflow. Full-page desktop/tablet/phone captures reviewed for wrapping, section order, and form fit.
- One H1, meaningful H2/H3 hierarchy, navigation/main/footer landmarks, visible input labels, alt naming for the orb, decorative fields excluded from the accessibility tree, and a skip link.
- Keyboard activation of the form, pause/resume, and Light Field response. Native invalid-email and missing-consent messages focus the relevant field. Preview confirmation is a live status and receives focus. The form clears its temporary values afterward.
- Empty/invalid email rejected; unchecked consent rejected; first name may be empty. Consent begins unchecked and is cleared after a valid preview. No account or list membership is implied.
- Pause stops all six CSS animation layers; resume restarts the visible hero field. The response study announces its temporary warmth and returns to resting.
- Chrome DevTools `prefers-reduced-motion: reduce`: `matchMedia` true, zero running animations, animation name `none`, transition duration `0s`. The pause control disappears. Emulation restored after testing.
- Chrome JavaScript disabled and reloaded: preview submit remains disabled, explanatory no-script text appears, content remains readable. JavaScript restored after testing.
- Browser preview reported no application console errors. Chrome DevTools' optional workspace discovery request was blocked by `connect-src 'none'`, as expected; it is not an application network request.

## Static and integrity checks completed

- JavaScript syntax and `git diff --check` pass.
- Local asset links and anchor targets resolve. IDs are unique.
- Text contrast pairs checked against static surfaces and a conservative brighter violet surface: lowest tested text ratio 7.22:1. Input boundaries and focus indicators meet 3:1. This is a basics check, not an exhaustive animated-pixel or full WCAG audit.
- No form endpoint, network library, analytics, cookies, storage API, or third-party font is present. CSP blocks connections and form submission even if the local validation script fails. Inputs have no submission names.
- Canonical A2.1 master and monochrome dark-background mark match their existing local source bytes; the downloaded luminous reference is preserved unchanged. See the brand manifest.
- `CNAME` is unchanged. No deployment workflow, AWS configuration, or production code is added.

## Live boundary verified

GitHub Pages settings were inspected read-only: `Deploy from a branch`, `main`, `/ (root)`, existing custom domain `ioleia.com`. The last deployment shown was the prior main deployment. Main was `363f79ea5e8c0cf2687879963fe33e7bf1fdd5db` when work began. The branch descends from the earlier website branch, not from a new production deployment.

No live website changes, merges, DNS/email-record changes, AWS deployments, SES changes, Cognito changes, Apple changes, or other production changes were performed by this task. The final publication receipt is retained outside the repository after the draft PR is created, so the exact published tree can be verified without a self-referential commit.

## Scope limits

Browser viewport checks are not physical-device acceptance or a full assistive-technology audit. The small monochrome favicon retains the original fine-detail limitation. The luminous board is a rendering reference; it is not newly certified as pixel-identical to A2.1. Production artwork preparation and backend/hosting qualification remain later implementation work, distinct from founder visual approval.
