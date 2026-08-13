#!/usr/bin/env python3
"""Prepare a canonical UTF-8 text source from Markdown, text, or PDF input."""

import argparse
import pathlib
import sys


def extract_pdf(source: pathlib.Path) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.exit("Missing dependency 'pypdf'. Run: python -m pip install -r requirements.txt")

    reader = PdfReader(source)
    pages = []
    extracted_text = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        extracted_text.append(text)
        pages.append(f"--- Page {index} ---\n{text.strip()}")
    if not any(any(character.isalnum() for character in text) for text in extracted_text):
        sys.exit("PDF contains no extractable text. Run OCR and provide a UTF-8 .txt or .md source.")
    return "\n\n".join(pages).strip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=pathlib.Path)
    parser.add_argument("--output", type=pathlib.Path)
    args = parser.parse_args()

    source = args.source.resolve()
    if not source.is_file():
        sys.exit(f"Source does not exist: {source}")

    suffix = source.suffix.lower()
    if suffix in {".md", ".txt"}:
        source.read_text(encoding="utf-8")
        print(source)
        return
    if suffix != ".pdf":
        sys.exit("Unsupported source type. Use .md, .txt, or .pdf.")

    output = args.output or source.with_suffix(".extracted.txt")
    output = output.resolve()
    output.write_text(extract_pdf(source), encoding="utf-8", newline="\n")
    print(output)


if __name__ == "__main__":
    main()
