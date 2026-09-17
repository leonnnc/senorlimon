# -*- coding: utf-8 -*-
"""Lista los enlaces internos del sitio agrupados"""
import re, sys, json
files = sys.argv[1:]
found = {}
for f in files:
    html = open(f, encoding="utf-8").read()
    for m in re.finditer(r'<a\b[^>]*href="(https?://senorlimon\.com[^"]*)"[^>]*>(.*?)</a>', html, re.S | re.I):
        url = m.group(1)
        if "wp-content" in url or "wp-json" in url or "feed" in url:
            continue
        txt = re.sub(r"<[^>]+>", " ", m.group(2))
        txt = re.sub(r"\s+", " ", txt).strip()[:60]
        key = url.rstrip("/") or url
        found.setdefault(key, set()).add(txt)
for k in sorted(found):
    labels = " | ".join(sorted(t for t in found[k] if t))[:90]
    print("%-52s %s" % (k.replace("https://senorlimon.com", ""), labels))
