# -*- coding: utf-8 -*-
import json, io, sys
src = r"C:\Users\leonn\Documents\web\senorlimon\_review\menu.json"
data = json.load(open(src, encoding="utf-8"))
out = io.StringIO()
for slug, page in data.items():
    out.write("\n=== %s | titulo=%s\n" % (slug, page["title"]))
    for sub in page["subsections"]:
        out.write("  -- %s (%d)\n" % (sub["name"], len(sub["items"])))
        for it in sub["items"]:
            img = "IMG" if it["img"] else "---"
            out.write("     [%s] %s | price=%s | desc=%s | variants=%d\n" % (
                img, it["name"], it["price"], (it["desc"][:90] or ""), len(it["variants"])))
            for v in it["variants"]:
                out.write("           v: %s = %s\n" % (v["name"], v["price"]))
open(r"C:\Users\leonn\Documents\web\senorlimon\_review\menu_dump.txt", "w", encoding="utf-8").write(out.getvalue())
print("ok", len(out.getvalue()))
