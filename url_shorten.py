import os
import sqlite3

from flask import Flask, redirect, render_template, request

from url_hash import generate_short_url_hash

app = Flask(__name__, template_folder="templates")

DB_PATH = os.environ.get("URL_SHORTENER_DB_PATH", os.path.join(os.path.dirname(__file__), "url_shortener.db"))


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS url_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_url TEXT NOT NULL UNIQUE,
            access_count INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten_url():
    long_url = request.form.get("long_url", "").strip()
    if not long_url:
        return "Invalid URL", 400

    if "://" not in long_url:
        long_url = f"https://{long_url}"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT short_url FROM url_mapping WHERE long_url = ?", (long_url,))
    existing_entry = cursor.fetchone()
    if existing_entry:
        short_url = existing_entry["short_url"]
        conn.close()
        return f"shortened url: <a href='{request.host_url}{short_url}'>{request.host_url}{short_url}</a>"

    short_url = generate_short_url_hash(long_url)
    counter = 1
    while True:
        cursor.execute("SELECT 1 FROM url_mapping WHERE short_url = ?", (short_url,))
        if not cursor.fetchone():
            break
        short_url = generate_short_url_hash(f"{long_url}:{counter}")
        counter += 1

    cursor.execute(
        "INSERT INTO url_mapping (long_url, short_url) VALUES (?, ?)",
        (long_url, short_url),
    )
    conn.commit()
    conn.close()

    return f"shortened url: <a href='{request.host_url}{short_url}'>{request.host_url}{short_url}</a>"


@app.route("/<short_url>", methods=["GET"])
def redirect_to_long_url(short_url):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT long_url FROM url_mapping WHERE short_url = ?", (short_url,))
    entry = cursor.fetchone()
    if entry:
        cursor.execute(
            "UPDATE url_mapping SET access_count = access_count + 1 WHERE short_url = ?",
            (short_url,),
        )
        conn.commit()
        conn.close()
        return redirect(entry["long_url"])

    conn.close()
    return "URL not found", 404


if __name__ == "__main__":
    app.run(debug=True)
