import datetime
import json
import re
from pathlib import Path

import click
import requests

ROOT = Path(__file__).resolve().parent.parent


def normalize_isbn(isbn):
    s = re.sub(r"[\s\-]", "", isbn or "").upper()
    if len(s) == 13 and s.startswith(("978", "979")) and s.isdigit():
        return s
    if len(s) == 10 and s[:9].isdigit() and (s[9].isdigit() or s[9] == "X"):
        return isbn10_to_13(s)
    return None


def isbn10_to_13(isbn10):
    digits = [int(c) for c in isbn10[:9]]
    base = [9, 7, 8] + digits
    check = (10 - sum((3 if i % 2 else 1) * d for i, d in enumerate(base)) % 10) % 10
    return "".join(map(str, base)) + str(check)


def normalize_title(s):
    return re.sub(r"[^\w\s]", "", (s or "").lower()).strip()


def title_matches(target, candidate):
    if not candidate:
        return False
    stripped = re.sub(r"\[.*?\]", "", candidate)
    return normalize_title(stripped) == target


def lookup_isbns(title, author, limit=8):
    candidates = []
    seen = set()
    target = normalize_title(title)

    def add(source, ctitle, cauthor, isbn):
        norm = normalize_isbn(isbn)
        if norm and norm not in seen and title_matches(target, ctitle):
            seen.add(norm)
            candidates.append(
                {"title": ctitle, "author": cauthor or "?", "isbn": norm, "source": source}
            )

    try:
        q = f"intitle:{title} inauthor:{author}"
        r = requests.get(
            "https://www.googleapis.com/books/v1/volumes", params={"q": q, "maxResults": 5}, timeout=15
        )
        r.raise_for_status()
        for item in r.json().get("items", [])[:5]:
            vi = item.get("volumeInfo", {})
            isbn13 = next(
                (i.get("identifier") for i in vi.get("industryIdentifiers", []) if i.get("type") == "ISBN_13"),
                None,
            )
            if isbn13:
                add("Google Books", vi.get("title"), ", ".join(vi.get("authors") or []), isbn13)
    except Exception as e:
        click.echo(f"Google Books lookup failed: {e}", err=True)

    try:
        params = {"title": title, "author": author, "fields": "title,author_name,isbn"}
        r = requests.get("https://openlibrary.org/search.json", params=params, timeout=15)
        r.raise_for_status()
        for doc in r.json().get("docs", [])[:4]:
            authors = doc.get("author_name") or ["?"]
            for isbn in doc.get("isbn") or []:
                add("Open Library", doc.get("title"), authors[0], isbn)
                if len(candidates) >= limit:
                    break
            if len(candidates) >= limit:
                break
    except Exception as e:
        click.echo(f"Open Library lookup failed: {e}", err=True)

    return candidates[:limit]


def lookup_and_pick(title, author, accept):
    candidates = lookup_isbns(title, author)
    if not candidates:
        click.echo("No ISBN found via lookup.")
        manual = click.prompt("Enter ISBN manually (or press Enter to skip)", default="", show_default=False)
        return normalize_isbn(manual) or None

    click.echo("\nFound possible matches:")
    for i, c in enumerate(candidates, 1):
        click.echo(f"  {i}. {c['title']} by {c['author']} — {c['isbn']} ({c['source']})")

    if accept:
        return candidates[0]["isbn"]

    choice = click.prompt("\nWhich match to use? (number, 0 to skip)", default="1", show_default=False)
    if choice.strip() == "0":
        manual = click.prompt("Enter ISBN manually (or press Enter to skip)", default="", show_default=False)
        return normalize_isbn(manual) or None
    try:
        idx = int(choice) - 1
        return candidates[idx]["isbn"]
    except (ValueError, IndexError):
        click.echo("Invalid choice, skipping ISBN.", err=True)
        return None


def update_markdown(title, author, year):
    reading_dir = ROOT / "content" / "reading"
    reading_dir.mkdir(parents=True, exist_ok=True)
    path = reading_dir / f"{year}.md"
    line = f"- {title} - {author}"

    if path.exists():
        content = path.read_text()
        if any(l.strip() == line for l in content.splitlines()):
            click.echo(f"Already present in {path}")
            return
        with path.open("a") as f:
            if content and not content.endswith("\n"):
                f.write("\n")
            f.write(line + "\n")
    else:
        front = f"---\ntitle: {year} Reading Log\ndate: {year}-01-01\n---\n\n"
        path.write_text(front + line + "\n")
    click.echo(f"Logged in {path}")


def update_books_json(title, author, isbn, year):
    path = ROOT / "data" / "books.json"
    if not path.exists():
        raise click.ClickException(f"{path} not found")

    data = json.loads(path.read_text())
    year = str(year)

    norm_title = re.sub(r"[^\w\s]", "", title.lower())
    for b in data["books"]:
        if re.sub(r"[^\w\s]", "", b.get("title", "").lower()) == norm_title:
            years = b.setdefault("yearRead", [])
            if year not in years:
                years.append(year)
            if isbn and not b.get("isbn"):
                b["isbn"] = isbn
            click.echo(f"Updated existing entry '{b['title']}' (year {year})")
            break
    else:
        data["books"].append(
            {
                "title": title,
                "author": author,
                "isbn": isbn or "",
                "yearRead": [year],
            }
        )
        click.echo(f"Added new entry '{title}'")

    with path.open("w") as f:
        json.dump(data, f, indent=2, ensure_ascii=True)


@click.command()
@click.option("--title", help="Book title (prompted if omitted)")
@click.option("--author", help="Book author (prompted if omitted)")
@click.option("--isbn", help="ISBN-13 (skips lookup if provided)")
@click.option("--year", default=str(datetime.date.today().year), show_default=True, help="Reading log year")
@click.option("--yes", is_flag=True, help="Accept the first lookup match without asking")
def main(title, author, isbn, year, yes):
    """Add a book I've read to the current reading log and data/books.json."""

    if not title:
        title = click.prompt("Title").strip()
    if not author:
        author = click.prompt("Author").strip()
    if not title or not author:
        raise click.ClickException("Title and author are required")

    if isbn:
        isbn = normalize_isbn(isbn)
        if not isbn:
            raise click.ClickException(f"'{isbn}' is not a valid ISBN")
    else:
        entered = click.prompt("ISBN (blank to look up)", default="", show_default=False).strip()
        if entered:
            isbn = normalize_isbn(entered)
            if not isbn:
                raise click.ClickException(f"'{entered}' is not a valid ISBN")
        else:
            isbn = lookup_and_pick(title, author, yes)

    if not yes:
        click.echo(f"\nAdding for {year}: {title} by {author} (ISBN {isbn or 'n/a'})")
        if not click.confirm("Continue?"):
            raise click.Abort()

    update_markdown(title, author, year)
    update_books_json(title, author, isbn, year)
    click.echo("Done.")


if __name__ == "__main__":
    main()