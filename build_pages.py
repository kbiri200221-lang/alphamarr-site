"""Generate about/stock/news/contact pages from index.html (same app, different sections + SEO head)."""
import re, html
PAGES = {'about': ('About AlphaMarr — Seafood Exporter & Trader in Nouadhibou, Mauritania', 'AlphaMarr SARL is a seafood export and trading company in Nouadhibou, Mauritania: who we are, our fleet and partners, why buyers work with us and the markets we serve.'), 'stock': ('Live Seafood Stock — Frozen Fish Available FOB Nouadhibou | AlphaMarr', 'Live stock of frozen fish, cephalopods, fishmeal and fish oil available now in Nouadhibou, Mauritania — lot photos, sizes and quick price requests, FOB Nouadhibou.'), 'news': ('Seafood Market News — Mauritania & World Fisheries | AlphaMarr', 'Latest seafood, fishing and fishmeal market news for Mauritania and international buyers, updated automatically by AlphaMarr.'), 'contact': ('Contact AlphaMarr — Request a Seafood Quote from Mauritania', 'Contact AlphaMarr SARL in Nouadhibou, Mauritania: request a quote for frozen fish, cephalopods, fishmeal or fish oil. Email, phone and WhatsApp.')}
src = open("index.html", encoding="utf-8").read()
for pg, (ti, de) in PAGES.items():
    c = src
    c = re.sub(r"<title>.*?</title>", lambda m: "<title>" + html.escape(ti, quote=False) + "</title>", c, count=1)
    c = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m.group(1) + html.escape(de), c, count=1)
    c = c.replace('<link rel="canonical" href="https://alphamarr.com/">', '<link rel="canonical" href="https://alphamarr.com/%s.html">' % pg, 1)
    c = c.replace('<meta property="og:url" content="https://alphamarr.com/">', '<meta property="og:url" content="https://alphamarr.com/%s.html">' % pg, 1)
    c = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m.group(1) + html.escape(ti), c, count=1)
    c = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m.group(1) + html.escape(de), c, count=1)
    open(pg + ".html", "w", encoding="utf-8").write(c)
    print("built", pg)
