# Validation and local execution

Use Python 3.11 or newer in an existing approved environment containing the versions in `requirements-dev.txt`. The file is a reproducibility manifest, not permission to install software. The implementation used PyYAML 6.0.3, Rich 14.3.3, and an existing Ruff 0.15.10 executable; no package was installed or runtime modified. Ruff is pinned to the version actually available and tested rather than the plan's uninstalled newer version.

Before Python initializes `tempfile`, bind `TMPDIR`, `TEMP`, and `TMP` to the same task-owned directory under the active Hermes home. On Windows all three matter. Bind `TOKENCAT_PYTHON`, `TOKENCAT_RUFF` and `TOKENCAT_SHELLCHECK` to verified existing native executable paths, not guessed PATH aliases. From repository root:

```bash
: "${HERMES_HOME:?Use the actual active Hermes home}"
: "${TOKENCAT_PYTHON:?Bind an approved Python 3.11+ with the declared dependencies}"
: "${TOKENCAT_RUFF:?Bind the existing Ruff 0.15.10 executable}"
: "${TOKENCAT_SHELLCHECK:?Bind an approved existing ShellCheck executable}"
export TMPDIR="$HERMES_HOME/cache/scratch"
export TEMP="$TMPDIR"
export TMP="$TMPDIR"
"$TOKENCAT_PYTHON" -B -c "import tempfile; print(tempfile.gettempdir())"
"$TOKENCAT_RUFF" check scripts tests
"$TOKENCAT_RUFF" format --check scripts tests
"$TOKENCAT_PYTHON" -B -m unittest discover -s tests -v
"$TOKENCAT_PYTHON" -B scripts/validate_theme.py
"$TOKENCAT_PYTHON" -B -m scripts.validate_theme
bash -n fonts/install-hack-nerd-font.sh
"$TOKENCAT_SHELLCHECK" --norc --format=json fonts/install-hack-nerd-font.sh
git diff --check
```

Expected: actual temporary paths under the chosen home; Ruff exits zero; unit tests `OK`; both validator entry points print `PASS: hermesfox theme validation`; syntax/ShellCheck/whitespace commands exit zero. The stable validator message deliberately retains the existing repository name. Missing Ruff/ShellCheck is **blocked**, never a pass, and tool setup must follow the applicable approval policy. CI configuration is not evidence that CI ran; local-only work does not push or dispatch it.

## What the checks prove

- Seven normalized-text hashes preserve the shipped legacy palette, exports and cat sources. Upgrade base values retain every original token.
- Strict JSON/YAML rejects duplicate keys, malformed structures, non-finite JSON values (including exponent overflow) and non-string skin colors. CLI and package import paths share the same parser implementations.
- Missing source art/exports/hero, semantic pin drift, unrecognized palette tokens, missing mappings and changed/extra export colors fail validation. Copied mutation fixtures must validate before mutation.
- Shared skin aliases are explicit. VS Code workbench exports agree, all 16 ANSI colors are present, and the manifest points the two selector labels to distinct existing files.
- Named normal-text and word-diff pairs satisfy the measured contrast thresholds. Rich rendering matches the source geometry/escaping; one-span-per-row artwork remains default.
- Font fixtures supply their own archives and fake registry command. Before launching the installer, a Bash guard checks that resolved `reg` is the exact fake fixture file; a shadowed command aborts with exit 97.

## What remains independent

The tests are repository contracts, not complete vendor schemas or rendered acceptance. Effective selection/diff/disabled/hover/focus colors, cold starts, theme-switch cleanup, profile persistence, font rendering, narrow/wide terminal layouts and real dashboard normalization require isolated app/runtime evidence. See [compatibility.md](compatibility.md). Do not invoke model reviewers or alter Hermes to obtain it.

Private commands, RED/GREEN logs, model/budget notes and runtime readiness remain under ignored `.hermes/evidence/`; they are not release payloads. Source/docs scans still reject workstation paths and placeholder markers in shipped material. No tracked validation record should include credentials, private paths or model-provider details.
