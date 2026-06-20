# -*- coding: utf-8 -*-
"""Re-embed the monochrome conceptual-model PNG as Figure 4 (rId9 / image4.png)
in 'Manuscript Metaverse.docx', updating drawing extents to the new aspect ratio
without distortion. Replaces only the rId9 drawing block's extents.
"""
import zipfile, shutil, re, hashlib, struct, os

DOCX = "Manuscript Metaverse.docx"
PNG = "Figure1_Conceptual_Model.png"
NEW_CX = 5634072            # keep width
OLD_PAIR = 'cx="5634072" cy="3237972"'

# compute new cy from PNG pixel aspect, keeping cx fixed
img = open(PNG, "rb").read()
pw = struct.unpack(">I", img[16:20])[0]
ph = struct.unpack(">I", img[20:24])[0]
new_cy = round(NEW_CX * ph / pw)
NEW_PAIR = f'cx="{NEW_CX}" cy="{new_cy}"'
print("new pixel", pw, ph, "-> extent", NEW_PAIR)

z = zipfile.ZipFile(DOCX)
doc = z.read("word/document.xml").decode("utf-8")

# Locate the <w:drawing> ... </w:drawing> block containing rId9
embed_idx = doc.find('r:embed="rId9"')
assert embed_idx != -1, "rId9 not found"
start = doc.rfind("<w:drawing", 0, embed_idx)
end = doc.find("</w:drawing>", embed_idx) + len("</w:drawing>")
assert start != -1 and end != -1, "drawing block not found"
block = doc[start:end]
print("drawing block length", len(block))
print("OLD_PAIR count in block:", block.count(OLD_PAIR))

# Replace extents only inside this block
new_block = block.replace(OLD_PAIR, NEW_PAIR)
print("OLD_PAIR count after replace:", new_block.count(OLD_PAIR))
new_doc = doc[:start] + new_block + doc[end:]

# Sanity: other images' extents untouched
print("total OLD_PAIR remaining in doc:", new_doc.count(OLD_PAIR))

# Rewrite docx with new document.xml and replaced image4.png
tmp = DOCX + ".tmp"
with zipfile.ZipFile(DOCX) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
    for item in zin.infolist():
        data = zin.read(item.filename)
        if item.filename == "word/document.xml":
            data = new_doc.encode("utf-8")
        elif item.filename == "word/media/image4.png":
            data = img
        zout.writestr(item, data)
shutil.move(tmp, DOCX)

# Verify
z2 = zipfile.ZipFile(DOCX)
emb = z2.read("word/media/image4.png")
print("embedded image4.png sha", hashlib.sha256(emb).hexdigest()[:16], "matches:", emb == img)
doc2 = z2.read("word/document.xml").decode("utf-8")
print("NEW_PAIR present:", NEW_PAIR in doc2)
print("OK")
