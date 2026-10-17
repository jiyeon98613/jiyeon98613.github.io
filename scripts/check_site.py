"""Check built routes, anchors, assets and accidental private-file publication."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import re

ROOT=Path(__file__).resolve().parents[1]/"dist"
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=set(); self.links=[]; self.h1=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if "id" in attrs: self.ids.add(attrs["id"])
        if tag=="h1": self.h1+=1
        if tag in ("a","link","img","script"):
            value=attrs.get("href") if tag in ("a","link") else attrs.get("src")
            if value:self.links.append(value)

def main():
    pages={}
    for path in ROOT.rglob("*.html"):
        page=Page();page.feed(path.read_text());pages[path]=page
    errors=[]
    for path,page in pages.items():
        for link in page.links:
            u=urlparse(link)
            if u.scheme or u.netloc:continue
            target=(ROOT/unquote(u.path).lstrip("/")) if u.path.startswith("/") else path.parent/unquote(u.path)
            if not u.path:target=path
            if target.is_dir():target=target/"index.html"
            if not target.is_file():
                errors.append(f"{path.relative_to(ROOT)}: missing {link}");continue
            if u.fragment and target.suffix==".html" and unquote(u.fragment) not in pages.get(target,Page()).ids:
                errors.append(f"{path.relative_to(ROOT)}: missing anchor {link}")
        if "/portfolio/" not in str(path) and path.name!="404.html" and page.h1!=1:
            errors.append(f"{path.relative_to(ROOT)}: expected one h1, got {page.h1}")
    for path in ROOT.rglob("*"):
        if any(part in (".private-sources",".git","node_modules",".local","secrets") for part in path.relative_to(ROOT).parts):
            errors.append("Unexpected private/build path: "+str(path.relative_to(ROOT)))
        if path.is_file() and path.suffix in (".html",".js",".css",".json",".md",".txt"):
            text=path.read_text()
            if re.search(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9]{20,})\b",text):
                errors.append("Possible credential in "+str(path.relative_to(ROOT)))
            if "/home/jiyeon/" in text or "/tmp/" in text:
                errors.append("Local source path in "+str(path.relative_to(ROOT)))
    if errors:raise SystemExit("\n".join(errors))
    print(f"PASS: {len(pages)} HTML routes; internal links, anchors, assets and public output boundary")

if __name__=="__main__":main()
