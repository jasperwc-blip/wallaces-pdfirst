from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if len(args) != 3:
        print("Usage: pdf2docx_worker <input.pdf> <output.docx> <pages-json>", file=sys.stderr)
        return 2

    source = Path(args[0])
    output = Path(args[1])
    pages = json.loads(args[2])
    output.parent.mkdir(parents=True, exist_ok=True)

    converter = None
    try:
        from pdf2docx import Converter

        converter = Converter(str(source))
        converter.convert(str(output), pages=pages)
    finally:
        if converter is not None:
            converter.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
