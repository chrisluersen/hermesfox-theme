# Local banner work — homed 2026-09-28

These three local banner/branding edits used to ride inside the **repair** bundle
(`hermes-patches-archive/live/hermes-local.patch`). They were removed from it deliberately, and the
removal is recorded as a decision, not as drift: they are display preferences, and the repair bundle
is the unit `hermes update` must reapply — it now has a one-owner-of-record contract covering only
update fixes.

`banner-local.patch` (8,578 bytes) is the exact live delta as of 2026-09-28, captured from the home
checkout **before** the working tree was reconciled to the six-file bundle. It was verified to apply
to a pristine `HEAD` (`8f21606116`) in a shared clone, so it is a real backup rather than a diff
against an unknown base.

| File | Change |
|---|---|
| `hermes_cli/banner.py` | +8 / −1 |
| `ui-tui/src/banner.ts` | +48 / −12 |
| `ui-tui/src/components/branding.tsx` | +24 / −4 |

3 files changed, 59 insertions(+), 21 deletions(-). The art itself (source `.txt`, row plan, previews)
lives in the parent `banner-art/` directory; this bundle is the *code* that renders it.

## Applying it

From a checkout whose tree is otherwise at `HEAD`:

```bash
git -C <hermes-agent> apply banner-art/banner-local-20260928/banner-local.patch
```

Then confirm it took — `git -C <hermes-agent> diff --stat` should list exactly those three files.

## Do not do this

Do **not** fold these hunks back into `hermes-patches-archive/live/hermes-local.patch`. The repair
bundle's contract is forward/reverse checks plus the focused tests, Ruff, workspace lint and a
same-session registry update; display preferences are out of scope by decision (2026-09-28).

## Provenance

- Earlier form of the same work: `hermes-patches-archive/retired/banner-local-20260925/banner-local.patch`.
- The 7-file bundle that still carried them: hermes-config `5b2ceead`.
- Related, separate, and **stale**: `banner-art/animated-hero-redo-bundle/upstream-diff-7-files.patch`
  (2026-08-14; does not apply — see `hermes-patches-archive/FIXES-REGISTRY.md` §5).