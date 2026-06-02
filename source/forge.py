#!/usr/bin/env python3
"""Forge the standalone dante.html — all data inlined, no server needed.

Run this after editing source/index.html or after re-parsing EPUBs.
"""
import json, re, os, shutil


def forge():
    base = os.path.dirname(os.path.abspath(__file__))  # source/
    root = os.path.dirname(base)                        # github/

    # Read sources
    with open(os.path.join(base, 'index.html'), 'r') as f:
        html = f.read()
    with open(os.path.join(base, 'books.json'), 'r') as f:
        books = json.load(f)

    # Build metadata for /api/books
    books_meta = {}
    for bid, b in books.items():
        cantos = b.get('cantos', [])
        books_meta[bid] = {
            'id': bid,
            'title': b['title'],
            'author': b['author'],
            'translator': b.get('translator'),
            'language': b['language'],
            'description': b.get('description', ''),
            'cantos_count': len(cantos),
            'total_lines': sum(len(c.get('lines', [])) for c in cantos),
            'has_notes': b.get('has_notes', False),
            'has_images': b.get('has_images', False),
        }

    # Build canto lists for /api/books/{id}/cantos
    canto_lists = {}
    for bid, b in books.items():
        canto_lists[bid] = [
            {'section': c['section'], 'number': c['number'],
             'title': c.get('title', ''), 'global_number': c['global_number']}
            for c in b.get('cantos', [])
        ]

    # Inline data APIs
    data_js = '\nconst BOOKS_DATA = ' + json.dumps(books, ensure_ascii=False) + ';\n'
    meta_js = 'const BOOKS_META = ' + json.dumps(books_meta, ensure_ascii=False) + ';\n'
    canto_list_js = 'const CANTO_LISTS = ' + json.dumps(canto_lists, ensure_ascii=False) + ';\n'

    standalone_api = '''async function api(path) {
  await new Promise(r => setTimeout(r, 0));
  if (path === '/api/books') return BOOKS_META;
  const m1 = path.match(/^\\/api\\/books\\/([^\\/]+)\\/cantos$/);
  if (m1) return CANTO_LISTS[m1[1]] || [];
  const m2 = path.match(/^\\/api\\/books\\/([^\\/]+)\\/canto\\/(\\d+)$/);
  if (m2) {
    const canto = BOOKS_DATA[m2[1]].cantos.find(c => c.global_number === +m2[2]);
    if (!canto) throw new Error('Canto not found');
    return canto;
  }
  throw new Error('Unknown API path: ' + path);
}'''

    # Replace API function
    old_start = html.index('async function api(path) {')
    old_end = html.index('\nfunction ', old_start + 1)
    html = html.replace(html[old_start:old_end], standalone_api)

    # Inject data after <script>
    insert = html.index('<script>') + len('<script>')
    html = html[:insert] + '\n' + data_js + meta_js + canto_list_js + html[insert:]

    # Remove Google Fonts
    html = re.sub(r'<link rel="preconnect"[^>]*>\s*', '', html)
    html = re.sub(r'<link href="https://fonts.googleapis.com[^"]*"[^>]*>\s*', '', html)

    # Fix image paths: /en_images/xxx.jpg → illustrations/xxx.jpg
    html = html.replace('"/en_images/', '"illustrations/')

    out = os.path.join(root, 'dante.html')
    with open(out, 'w') as f:
        f.write(html)

    print(f'Forged {out} ({len(html):,} bytes)')


if __name__ == '__main__':
    forge()
