#!/usr/bin/env python3
"""Import publication HTML without guessing where an author list ends.

Uses only Python's standard library. Unknown unquoted citations fail explicitly;
add their exact title to UNQUOTED_TITLES after reviewing the source.
"""
import argparse
import html
import json
import re
import unicodedata
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://sites.google.com/view/sachinkumar/research"
UNQUOTED_TITLES = [
    "Controlled Text Generation as Continuous Optimization with Multiple Constraints",
    "Improving the Diversity of Unsupervised Paraphrasing with Embedding Outputs",
    "Machine Translation into Low-Resource Language Varieties",
    "An Exploration of Data Augmentation Techniques for Improving English to Tigrinya Translation",
    "A Deep Reinforced Model for Zero-Shot Cross-Lingual Summarization with Bilingual Semantic Similarity Rewards",
    "A Margin-based Loss with Synthetic Negative Samples for Continuous-output Machine Translation",
    "Topics to Avoid: Demoting Latent Confounds in Text Classification",
    "Von Mises-Fisher Loss for Training Sequence to Sequence Models with Continuous Outputs",
    "Mining & Summarizing E-petitions for Enhanced Understanding of Public Opinion",
    "Machine Translation with Continuous Outputs",
    "Earth Mover Distance Pooling over Siamese LSTMs for Automatic Short Answer Grading",
    "Decisions under drift: Adapting binary decision thresholds to drifts in test distribution",
]


def normalize(value):
    return re.sub(r"\s+", " ", value).strip()


def slug(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


class PublicationHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.entries = []
        self.current = None
        self.anchor = None
        self.parents = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "li":
            self.parents.append(self.current)
            self.current = {"text": "", "links": []}
        elif tag == "a" and self.current is not None:
            self.anchor = {"label": "", "url": attrs.get("href", "")}
        elif tag == "br" and self.current is not None:
            self.current["text"] += " "

    def handle_data(self, data):
        if self.current is not None:
            self.current["text"] += data
        if self.anchor is not None:
            self.anchor["label"] += data

    def handle_endtag(self, tag):
        if tag == "a" and self.anchor is not None:
            self.anchor["label"] = normalize(self.anchor["label"])
            self.current["links"].append(self.anchor)
            self.anchor = None
        elif tag == "li" and self.current is not None:
            self.current["text"] = normalize(self.current["text"])
            if re.match(r"^\[\s*20\s*\d\s*\d\s*\]", self.current["text"]):
                self.entries.append(self.current)
            self.current = self.parents.pop()


def split_citation(text):
    year_match = re.match(r"^\[([\d\s]+)\]", text)
    year = int(re.sub(r"\s", "", year_match[1]))
    rest = text[year_match.end():]
    rest = re.sub(r"^(?:\s*\[+\s*[a-z][a-z &-]*\s*\]+\s*|\s*\]\s*)+", "", rest).strip()
    quoted = re.search(r'["“](.+?)["”]', rest)
    if quoted:
        authors = rest[:quoted.start()].strip(" ,.")
        title = quoted[1].rstrip(" ,.")
        venue = rest[quoted.end():].strip(" ,.")
    else:
        matches = [title for title in UNQUOTED_TITLES if title in rest]
        if len(matches) != 1:
            raise ValueError(f"Review unquoted title instead of guessing: {text}")
        title = matches[0]
        authors, venue = rest.split(title, 1)
        authors, venue = authors.strip(" ,."), venue.strip(" ,.")
    if "Sachin Kumar" not in authors or len(title.split()) < 3 or not venue:
        raise ValueError(f"Invalid citation fields: {text}")
    return year, authors, title, venue


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Downloaded Google Sites research HTML")
    parser.add_argument("--legacy-metadata", type=Path, help="Optional JSON export of old Jekyll front matter")
    args = parser.parse_args()
    source = PublicationHTML()
    source.feed(args.html.read_text(encoding="utf-8"))
    if not source.entries:
        raise ValueError("No publications found; no files have been changed")

    previous_path = ROOT / "_data/publications.json"
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else []
    legacy = json.loads(args.legacy_metadata.read_text()) if args.legacy_metadata else []
    records = []
    for index, entry in enumerate(source.entries):
        year, authors, title, venue = split_citation(entry["text"])
        prior = next((p for p in previous if p.get("source_citation") == entry["text"] or slug(p["title"]) == slug(title)), None)
        old = [(f, p) for f, p in legacy if slug(html.unescape(p["title"])) == slug(title)]
        identifier = prior["id"] if prior else Path(old[0][0]).stem if old else f"{year}-01-01-{slug(title)}"
        records.append({
            "id": identifier, "year": year, "order": index,
            "title": title, "authors": authors, "venue": venue,
            "links": [dict(link) for link in entry["links"]], "source_url": SOURCE,
            "source_citation": entry["text"],
            "redirect_from": prior.get("redirect_from", []) if prior else [],
        })

    # Keep old URLs for the malformed duplicate documents as redirects.
    for filename, metadata in legacy:
        identifier = Path(filename).stem
        if any(p["id"] == identifier for p in records):
            continue
        paper = metadata.get("paperurl")
        matches = [p for p in records if paper and any(link["url"] == paper for link in p["links"])]
        if metadata["title"] == "John Wieting":
            matches = [p for p in records if p["title"].startswith("Improving the Diversity")]
        if len(matches) != 1:
            raise ValueError(f"Review unmatched existing publication: {filename}")
        matches[0]["redirect_from"].append(metadata["permalink"])

    if len({p["id"] for p in records}) != len(records):
        raise ValueError("Duplicate publication IDs; no files have been changed")
    overrides_path = ROOT / "migration/publication-overrides.json"
    overrides = json.loads(overrides_path.read_text()) if overrides_path.exists() else {}
    for record in records:
        reviewed = overrides.get(record["id"], {})
        record.update(reviewed.get("fields", {}))
        record["links"].extend(link for link in reviewed.get("additional_links", []) if link not in record["links"])
        if reviewed:
            record["verification_sources"] = reviewed["sources"]
    previous_path.write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    snapshot = ROOT / "migration/google-sites-publications.json"
    snapshot.write_text(json.dumps(source.entries, ensure_ascii=False, indent=2) + "\n")
    print(f"Imported {len(records)} publications, {sum(len(p['links']) for p in source.entries)} source links, and {sum(len(p['links']) for p in records)} total reviewed links.")


if __name__ == "__main__":
    main()
