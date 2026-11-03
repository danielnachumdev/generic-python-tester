# generic-python-tester

**Generic stdin/stdout tester for HUJI OOP (Java) assignments** — declare input/output cases in one place, run them against a local executable via [`danielutils`](https://pypi.org/project/danielutils/) `TestFactory`.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

Requires **Python 3** (creates a local `venv/` on first run). Aimed at **Windows / macOS**; WSL is not fully supported yet.

## Why this exists

HUJI OOP exercises often need many interactive stdin/stdout checks. This script turns a small `FILES` table into generated test runs so you can iterate without rewriting harness code each time.

## Quick start

1. Put `main.py` next to (or point it at) the program under test — for Java, compile so the class name in `FILES` is runnable (`java Chat`, etc.).
2. Edit the **`FILES`** block at the top of [`main.py`](./main.py) (the section marked `EDIT`).
3. Run:

```bash
python main.py
# or: python3 main.py
```

On first run the script creates `./venv`, upgrades pip, and installs `danielutils`. Later runs reuse that venv.

## Configuring cases

Each entry in `FILES` is:

| Field | Meaning |
| ----- | ------- |
| executer | Program launcher (e.g. `java`) |
| executable | Target (e.g. class name `Chat`) |
| args | Extra CLI args (historically lightly tested) |
| inputs | List of stdin case payloads |
| outputs | Expected stdout fragments per case |

Example shape (already in `main.py`):

```python
FILES = [
    [
        "java",   # executer
        "Chat",   # executable
        [],       # args
        [         # inputs
            ["hi", 5],
            ["hello", 3],
        ],
        [         # outputs
            [""],
            [""],
        ],
    ],
]
```

Fill `outputs` with the strings you expect on stdout for each corresponding input case.

## Notes

- The harness writes a temporary `__TEMP_TEST_FILE__.py`, runs it with the venv Python, then deletes it.
- Optional version check compares local `VERSION` to a remote file under the historical [HUJI-OOP-tests](https://github.com/danielnachumdev/HUJI-OOP-tests) tree.
- **WSL:** current path/venv wiring still assumes Windows-style paths; contributions welcome.

## Contributing & development

Agent/developer workflow (layout, CI labels, domain pitfalls): see [`AGENTS.md`](./AGENTS.md).

## License

MIT — see [`LICENSE`](./LICENSE).
