"""
Divine Comedy reader — Flask server.
Run: pip install flask && python3 server.py
"""
import json, os
from flask import Flask, jsonify, send_from_directory, request

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE, static_url_path="")
BOOKS_PATH = os.path.join(BASE, "source", "books.json")

with open(BOOKS_PATH, 'r', encoding='utf-8') as f:
    books = json.load(f)


@app.route("/")
def index():
    return send_from_directory(os.path.join(BASE, "source"), "index.html")

@app.route("/api/books")
def get_books():
    result = {}
    for bid, book in books.items():
        result[bid] = {
            "id": book["id"], "title": book["title"],
            "author": book["author"], "translator": book.get("translator"),
            "language": book["language"], "description": book.get("description", ""),
            "has_notes": book.get("has_notes", False),
            "has_images": book.get("has_images", False),
            "canto_count": len(book["cantos"]),
            "sections": list(set(c["section"] for c in book["cantos"])),
        }
    return jsonify(result)

@app.route("/api/books/<book_id>/cantos")
def get_cantos(book_id):
    if book_id not in books: return jsonify({"error": "Book not found"}), 404
    return jsonify([{
        "section": c["section"], "number": c["number"],
        "title": c["title"], "global_number": c["global_number"],
        "line_count": len(c["lines"]), "note_count": len(c.get("notes", [])),
    } for c in books[book_id]["cantos"]])

@app.route("/api/books/<book_id>/canto/<int:gn>")
def get_canto(book_id, gn):
    if book_id not in books: return jsonify({"error": "Book not found"}), 404
    canto = next((c for c in books[book_id]["cantos"] if c["global_number"] == gn), None)
    if not canto: return jsonify({"error": "Canto not found"}), 404
    return jsonify({
        "section": canto["section"], "number": canto["number"],
        "global_number": canto["global_number"], "title": canto["title"],
        "lines": canto["lines"], "notes": canto.get("notes", []),
        "images": canto.get("images", []),
    })

@app.route("/api/books/<book_id>/canto/by-section/<section>/<int:number>")
def get_canto_by_section(book_id, section, number):
    if book_id not in books: return jsonify({"error": "Book not found"}), 404
    canto = next((c for c in books[book_id]["cantos"]
                  if c["section"] == section and c["number"] == number), None)
    if not canto: return jsonify({"error": "Canto not found"}), 404
    return jsonify({
        "section": canto["section"], "number": canto["number"],
        "global_number": canto["global_number"], "title": canto["title"],
        "lines": canto["lines"], "notes": canto.get("notes", []),
        "images": canto.get("images", []),
    })

@app.route("/api/search")
def search():
    q = request.args.get("q", "").lower()
    if not q or len(q) < 2: return jsonify([])
    results = []
    for book_id, book in books.items():
        for canto in book["cantos"]:
            for line in canto["lines"]:
                if q in line["text"].lower():
                    results.append({"book_id": book_id, "book_title": book["title"],
                        "section": canto["section"], "canto_number": canto["number"],
                        "global_number": canto["global_number"],
                        "line_number": line["n"], "text": line["text"]})
            for note in canto.get("notes", []):
                if q in note["text"].lower():
                    results.append({"book_id": book_id, "book_title": book["title"],
                        "section": canto["section"], "canto_number": canto["number"],
                        "global_number": canto["global_number"],
                        "type": "note", "ref": note["ref"], "text": note["text"]})
        if len(results) > 200: break
    return jsonify(results[:200])

if __name__ == "__main__":
    print("Divina Commedia — http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

