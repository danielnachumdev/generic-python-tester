# generic-python-tester – Agent Context

Implementation guide for coding agents changing **generic-python-tester**. Product pitch and user-facing usage: [`README.md`](README.md).

---

## Orientation

| Question | Answer |
| -------- | ------ |
| What is this? | Single-file **stdin/stdout** harness for HUJI OOP (typically **Java**) assignments |
| Code | Root [`main.py`](main.py) only (no importable package) |
| Toolchain | Plain Python 3 + on-first-run `./venv` (installs `danielutils`) |
| Tests | No `tests/` suite — the script *is* the tester for student programs |
| Secrets | None expected; never commit tokens or personal credentials |

```text
.
├── .github/          # When present: CODEOWNERS, dependabot, thin CI (see below)
├── main.py           # Edit FILES; rest is harness (setup + generated TestFactory runs)
├── README.md         # Marketing / user docs
├── AGENTS.md
├── LICENSE           # MIT
└── .gitignore
```

Runtime behavior lives entirely in `main.py`: `setup()` (version check + venv/`danielutils`) then `test()` (emit temp script → run → delete).

Shared CI/CD patterns (when workflows exist): [`danielnachumdev/actions`](https://github.com/danielnachumdev/actions) (`@latest`). How to adopt: [`HOW-TO-USE.md`](https://github.com/danielnachumdev/actions/blob/latest/HOW-TO-USE.md).

---

## Develop

```bash
python3 main.py    # creates ./venv on first run; installs danielutils
# After venv exists:
./venv/bin/python main.py          # Unix
.\venv\Scripts\python.exe main.py  # Windows
```

There is **no** `pyproject.toml` / `uv` / pytest lane on `main` today. Do not invent a packaging layout unless an explicit issue/PR asks for it.

| Task | Command / note |
| ---- | -------------- |
| Run harness | `python3 main.py` (after editing `FILES`) |
| Smoke import of dep | activate venv, `python -c "import danielutils"` |
| Unit tests | N/A — no project test suite |

### Dependencies

- **Runtime (installed by `setup()` into `./venv`):** `danielutils` (`TestFactory`, `Test`, `acm`, `bytes_to_str`)
- **External under test:** whatever `FILES` launches (commonly a compiled Java class on `PATH`)

---

## Domain notes

- **Only edit the `FILES` block** for normal assignment use; keep the `DONT TOUCH BELOW` harness stable unless fixing the harness itself.
- Generated temp file is `__TEMP_TEST_FILE__.py` (path uses Windows `.\` by default; WSL branch rewrites separators but still raises `RuntimeWarning` — WSL is incomplete).
- `acm(...)` drives interactive stdin with a short `i_timeout`; empty-string enter presses are synthesized from the numeric part of each input case in the current generator.
- Version probe hits a raw GitHub URL under `danielnachumdev/HUJI-OOP-tests` — network failures should stay non-fatal for local testing when changing that path.
- Prefer portable `os` path handling if extending beyond Windows; avoid hard-coding only `nul` redirects without a Unix equivalent when touching install commands.

---

## PRs, CI, and releases

1. Branch off `main`; open a PR into `main`.
2. Attach **exactly one** semver label: `noBump` | `bumpPatch` | `bumpMinor` | `bumpMajor` (labels already exist on the repo).
3. **CI** — thin orchestrator via `danielnachumdev/actions` (`ci.yml@latest` with `allow-empty: true`, `semver-ci.yml@latest`). Prefer required checks **`CI / CI`** and **`Semver / Semver`** once workflows are on `main`.
4. No PyPI / release CD for this script repo — do not add publish secrets or wheel publish without an explicit request.
5. Dependabot PRs stay on `noBump`.
6. Change shared CI/semver behavior in **`danielnachumdev/actions`**, not by re-vendoring here.

### Repo gates

- `.github/CODEOWNERS` — `@danielnachumdev` (when workflows branch is merged)
- Semver label required on PRs via shared `semver-ci` once enabled

---

## Sensitive / ignored

Do not commit: `venv/`, `.venv/`, `__pycache__/`, `__TEMP_TEST_FILE__.py`, API keys, tokens. Respect `.gitignore`. No student PII or live university credentials in docs/PRs.
