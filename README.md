# Divina Commedia

Three-pane parallel reader for Dante's *Divine Comedy*.  
Translations, commentary, and Doré engravings — side by side.

**[Open dante.html](dante.html)** — no install, no server, just a browser.

[![Netlify Status](https://api.netlify.com/api/v1/badges/REPLACE_ME/deploy-status)](https://REPLACE_ME.netlify.app)

---

## What's inside

| Pane | Content |
|------|---------|
| **Text** | Лозинский · Мин · Cary (EN) · Italian original |
| **Notes** | All commentary combined, color-coded by source, sorted by line |
| **Illustrations** | 136 Gustave Doré engravings |

Click a ★ in the text → notes scroll to that line.  
Click a note → text scrolls to that line.

All four translations of all 100 cantos, 2,600+ editorial notes, 136 illustrations.  
No internet, no server, no dependencies — one HTML file + an images folder.

---

## Quick start

### Just read (no install)
```
open dante.html
```
Works offline in any modern browser. Keep `illustrations/` in the same folder.

### Local server (for development)
```bash
pip install flask
python3 server.py
# → http://localhost:5000
```

### Rebuild standalone (after editing the frontend)
```bash
cd source && python3 forge.py
# → regenerates ../dante.html
```

---

## Public domain

All content is free of copyright restrictions:

| Work | Author | Year | Status |
|------|--------|------|--------|
| *Divina Commedia* | Dante Alighieri | 1321 | Public domain |
| Russian translation | Михаил Лозинский | d. 1955 | Public domain (2026) |
| Russian translation (Inferno) | Михаил Мин | — | Public domain |
| English translation | Henry Francis Cary | d. 1844 | Public domain |
| Illustrations | Gustave Doré | d. 1883 | Public domain |

---

## Project structure

```
├── dante.html          ← standalone reader (open in browser)
├── illustrations/      ← 136 Doré engravings
├── server.py           ← Flask API + dev server
├── requirements.txt    ← Flask
└── source/
    ├── index.html      ← editable SPA frontend
    ├── forge.py        ← builds ../dante.html
    └── books.json      ← pre-parsed book data
```

---

## License

The code is MIT. The content is public domain — do whatever you want with it.
