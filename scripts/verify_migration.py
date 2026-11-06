#!/usr/bin/env python3
"""Check source citation/link coverage and optionally a built Jekyll directory."""
import argparse
import json
from html.parser import HTMLParser
from pathlib import Path

from generate_publications import ROOT, bibtex, validate
from import_google_sites import split_citation


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.images = []
        self.text = []
        self.articles = 0
        self.bibtex_entries = []
        self.code = None
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        elif tag == "img":
            self.images.append(attrs.get("src", ""))
        elif tag == "article" and attrs.get("class") == "publication":
            self.articles += 1
        elif tag == "code":
            self.code = []

    def handle_endtag(self, tag):
        if tag == "code" and self.code is not None:
            entry = "".join(self.code)
            if entry.startswith("@"):
                self.bibtex_entries.append(entry)
            self.code = None

    def handle_data(self, data):
        self.text.append(data)
        if self.code is not None:
            self.code.append(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path)
    args = parser.parse_args()
    records = json.loads((ROOT / "_data/publications.json").read_text())
    source = json.loads((ROOT / "migration/google-sites-publications.json").read_text())
    overrides = json.loads((ROOT / "migration/publication-overrides.json").read_text())
    validate(records)
    by_citation = {record["source_citation"]: record for record in records}
    assert len(by_citation) == len(records), "Duplicate source citations"
    assert len({record["order"] for record in records}) == len(records), "Duplicate publication order"
    migrated = []
    for original in source:
        assert original["text"] in by_citation, "A source publication was dropped"
        record = by_citation[original["text"]]
        migrated.append(record)
        assert all(link in record["links"] for link in original["links"]), record["id"]
    assert migrated == sorted(migrated, key=lambda record: record["order"]), "Original publication order changed"
    for record in records:
        year, authors, title, venue = split_citation(record["source_citation"])
        expected = {"year": year, "authors": authors, "title": title, "venue": venue}
        expected.update(overrides.get(record["id"], {}).get("fields", {}))
        assert all(record[k] == value for k, value in expected.items()), record["id"]
        if args.site:
            page = Page(args.site / "publication" / record["id"] / "index.html")
            assert all(link["url"] in page.links for link in record["links"]), record["id"]
            text = "".join(page.text)
            assert record["title"] in text and record["authors"] in text, record["id"]
            assert page.bibtex_entries == [bibtex(record)], f"Missing or incorrect BibTeX: {record['id']}"
            for alias in record.get("redirect_from", []):
                assert (args.site / alias.strip("/") / "index.html").exists(), alias
    if args.site:
        archive = Page(args.site / "publications/index.html")
        assert archive.articles == len(records), "Archive has missing or duplicate papers"
        assert '<h2 class="publication-year">' not in "".join(archive.text), "Year heading rendered as source code"
        assert all(link["url"] in archive.links for record in records for link in record["links"])
        assert len(archive.bibtex_entries) == len(records), "Archive BibTeX count differs from paper count"
        assert all(bibtex(record) in archive.bibtex_entries for record in records), "Archive BibTeX differs from paper metadata"
        featured_path = ROOT / "_data/selected_research.json"
        if featured_path.exists():
            featured = json.loads(featured_path.read_text())
            by_id = {record["id"]: record for record in records}
            assert len({item["publication_id"] for item in featured}) == len(featured), "Duplicate featured paper"
            home = Page(args.site / "index.html")
            home_text = "".join(home.text)
            for item in featured:
                record = by_id[item["publication_id"]]
                assert record["title"] in home_text, record["id"]
                assert f"/publication/{record['id']}/" in home.links, record["id"]
                assert item["image"] in home.images, record["id"]
                assert item["figure_source"] in home.links, record["id"]
        for path in ["index.html", "group/index.html", "teaching/index.html", "prospective-students/index.html"]:
            page = Page(args.site / path)
            for image in page.images:
                if image.startswith("/") and not image.startswith("//"):
                    target = args.site / image.lstrip("/").split("?", 1)[0]
                    assert target.exists(), f"Missing image: {target}"
                    assert target.read_bytes()[:15].lower().find(b"html") == -1, f"Invalid image: {target}"
    print(f"Verified {len(records)} complete citations, all {sum(len(p['links']) for p in source)} original links, and {sum(len(p['links']) for p in records)} total resource links.")
    if args.site:
        print("Built archive, individual paper pages, redirects and page images verified.")
        print(f"Verified BibTeX on all {len(records)} paper pages and archive entries.")
        if featured_path.exists():
            print(f"Verified {len(featured)} selected papers, their figures and citation-page links.")


if __name__ == "__main__":
    main()
