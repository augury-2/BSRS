#!/usr/bin/env python3
"""Lightweight Markdown -> .docx converter for the revised manuscript.
Handles: # ## ### headings, paragraphs, blockquotes, bullet lists,
pipe tables, **bold**, *italic*, and --- horizontal rules.
"""
import re
import sys
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH


def add_runs(paragraph, text):
    """Parse **bold** and *italic* inline markup into runs."""
    # Split on bold/italic tokens while keeping delimiters
    pattern = re.compile(r'(\*\*.+?\*\*|\*.+?\*)')
    pos = 0
    for m in pattern.finditer(text):
        if m.start() > pos:
            paragraph.add_run(text[pos:m.start()])
        token = m.group(0)
        if token.startswith('**'):
            r = paragraph.add_run(token[2:-2]); r.bold = True
        else:
            r = paragraph.add_run(token[1:-1]); r.italic = True
        pos = m.end()
    if pos < len(text):
        paragraph.add_run(text[pos:])


def parse_table(lines):
    rows = []
    for ln in lines:
        cells = [c.strip() for c in ln.strip().strip('|').split('|')]
        rows.append(cells)
    # drop the separator row (---)
    rows = [r for r in rows if not all(re.fullmatch(r':?-{2,}:?', c or '-') for c in r)]
    return rows


def main(md_path, docx_path):
    with open(md_path, encoding='utf-8') as f:
        lines = f.readlines()

    doc = Document()
    style = doc.styles['Normal']
    style.font.name = 'Calibri'
    style.font.size = Pt(11)

    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i].rstrip('\n')
        stripped = raw.strip()

        # blank
        if not stripped:
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r'-{3,}', stripped):
            i += 1
            continue

        # table block
        if stripped.startswith('|') and i + 1 < n and re.search(r'\|\s*:?-{2,}', lines[i+1]):
            block = []
            while i < n and lines[i].strip().startswith('|'):
                block.append(lines[i])
                i += 1
            rows = parse_table(block)
            if rows:
                t = doc.add_table(rows=len(rows), cols=len(rows[0]))
                t.style = 'Light Grid Accent 1'
                for ri, row in enumerate(rows):
                    for ci, cell in enumerate(row):
                        if ci < len(t.rows[ri].cells):
                            cellp = t.rows[ri].cells[ci].paragraphs[0]
                            add_runs(cellp, cell)
                            if ri == 0:
                                for rn in cellp.runs:
                                    rn.bold = True
                doc.add_paragraph()
            continue

        # headings
        if stripped.startswith('#'):
            m = re.match(r'(#+)\s+(.*)', stripped)
            level = min(len(m.group(1)), 4)
            doc.add_heading(m.group(2), level=level - 1 if level > 1 else 0)
            i += 1
            continue

        # blockquote (figure notes)
        if stripped.startswith('>'):
            text = stripped.lstrip('>').strip()
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Pt(18)
            add_runs(p, text)
            for rn in p.runs:
                rn.italic = True
            i += 1
            continue

        # bullet list
        if stripped.startswith('- ') or stripped.startswith('* '):
            p = doc.add_paragraph(style='List Bullet')
            add_runs(p, stripped[2:])
            i += 1
            continue

        # normal paragraph
        p = doc.add_paragraph()
        add_runs(p, stripped)
        i += 1

    doc.save(docx_path)
    print(f"Saved {docx_path}")


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
