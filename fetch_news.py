#!/usr/bin/env python3
"""Fetch seafood / fisheries news (Google News RSS) in 5 languages -> news.json.
Run by .github/workflows/news.yml every 6 hours. Standard library only."""
import json, re, urllib.request, urllib.parse, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

QUERIES = {
    "en": ("US", "en", ["seafood industry OR fisheries export OR fishmeal market",
                        "Mauritania fisheries OR West Africa fishing OR cephalopod market"]),
    "fr": ("FR", "fr", ['"produits de la mer" OR "pêche maritime" OR "farine de poisson"',
                        "Mauritanie pêche OR Nouadhibou OR poulpe marché"]),
    "es": ("ES", "es", ['"productos del mar" OR "sector pesquero" OR "harina de pescado"',
                        "Mauritania pesca OR pulpo mercado OR Conxemar"]),
    "zh": ("CN", "zh-Hans", ["水产品 OR 渔业 OR 鱼粉", "毛里塔尼亚 渔业 OR 章鱼 进口"]),
    "ar": ("MA", "ar", ["الصيد البحري OR صادرات الأسماك", "موريتانيا الصيد OR دقيق السمك"]),
}
MAX = 12

def fetch(q, gl, hl):
    url = ("https://news.google.com/rss/search?q=" + urllib.parse.quote(q + " when:14d")
           + f"&hl={hl}&gl={gl}&ceid={gl}:{hl}")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AlphaMarrNewsBot"})
    with urllib.request.urlopen(req, timeout=30) as r:
        root = ET.fromstring(r.read())
    out = []
    for it in root.iter("item"):
        title = (it.findtext("title") or "").strip()
        src = (it.findtext("source") or "").strip()
        if src and title.endswith(" - " + src):
            title = title[: -len(src) - 3]
        try:
            d = parsedate_to_datetime(it.findtext("pubDate")).astimezone(timezone.utc).isoformat()
        except Exception:
            d = ""
        out.append({"t": title, "s": src, "u": it.findtext("link"), "d": d})
    return out

def norm(t):
    return re.sub(r"\W+", "", t.lower())[:60]

def main():
    try:
        old = json.load(open("news.json", encoding="utf-8"))
    except Exception:
        old = {"items": {}}
    items = {}
    for lang, (gl, hl, qs) in QUERIES.items():
        seen, res = set(), []
        for q in qs:
            try:
                for x in fetch(q, gl, hl):
                    k = norm(x["t"])
                    if k and k not in seen:
                        seen.add(k); res.append(x)
            except Exception as e:
                print("WARN", lang, q, e)
        res.sort(key=lambda x: x["d"], reverse=True)
        items[lang] = res[:MAX] or old.get("items", {}).get(lang, [])
        print(lang, len(items[lang]))
    json.dump({"updated": datetime.now(timezone.utc).isoformat(timespec="minutes"), "items": items},
              open("news.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
