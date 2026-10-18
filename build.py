"""Build a small, dependency-free static portfolio. Only public/ is copied."""
from pathlib import Path
from html import escape
import json
import shutil

ROOT = Path(__file__).parent
OUT = ROOT / "dist"
SITE_URL = "https://jiyeon98613.github.io"
PAGES = [
    ("", "PostgreSQL DBA 포트폴리오", "건강보험 청구 시스템의 데이터 모델링, 정합성, OCR와 운영 경험을 정리한 김지연의 포트폴리오.", "home"),
    ("projects/postgres-ops", "PostgreSQL 운영 실습", "실제 백업 복구와 기존 인덱스 비교, 권한 분리, 스트리밍 복제·PITR·CloudNativePG 장애조치를 검증한 기록.", "ops"),
    ("projects/nhis-billing", "건강보험 청구 시스템", "문서의 유효성과 대체 관계, 월별 관리와 기간별 청구, 개인정보 마스킹을 설계한 과정.", "billing"),
    ("projects/admin-console", "관리자 콘솔", "환자 상세 청구내역서의 API, PostgreSQL 제한 함수·권한·발행 이력과 실제 관리자 UI를 설명한 기록.", "console"),
    ("projects/education-db", "교육용 데이터베이스 설계", "공개 데이터의 구조를 관찰하고 15개 PostgreSQL 테이블을 설계·생성·검증한 기록.", "education"),
    ("about", "소개", "업무의 문제에서 출발해 데이터의 정합성과 안전한 운영을 공부하는 PostgreSQL DBA 지원자 김지연.", "about"),
]

def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ROOT / "public", OUT, dirs_exist_ok=True)
    template = (ROOT / "templates/base.html").read_text()
    for route, title, description, key in PAGES:
        body = (ROOT / f"content/{key}.html").read_text()
        values = {"TITLE": escape(title), "DESCRIPTION": escape(description, quote=True),
                  "URL": SITE_URL + "/" + (route + "/" if route else ""),
                  "BODY": body, "PAGE": key, "YEAR": "2026"}
        page = template
        for name, value in values.items():
            page = page.replace("{{" + name + "}}", value)
        destination = OUT / route
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "index.html").write_text(page)
    error = template
    body = '<section class="error-page wrap"><span class="eyebrow">404</span><h1>페이지를 찾을 수 없습니다.</h1><p>프로젝트와 설계 기록은 첫 화면에서 찾을 수 있습니다.</p><a class="button primary" href="/">첫 화면으로 돌아가기 <span aria-hidden="true">↗</span></a></section>'
    for name, value in {"TITLE": "페이지를 찾을 수 없습니다", "DESCRIPTION": "김지연 포트폴리오", "URL": SITE_URL + "/404.html", "BODY": body, "PAGE": "404", "YEAR": "2026"}.items():
        error = error.replace("{{" + name + "}}", value)
    (OUT / "404.html").write_text(error)
    urls = [SITE_URL + "/" + (p[0] + "/" if p[0] else "") for p in PAGES]
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join("<url><loc>" + u + "</loc></url>" for u in urls) + "</urlset>")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\nSitemap: " + SITE_URL + "/sitemap.xml\n")
    (OUT / ".nojekyll").touch()
    # Preserve useful resume/bookmark entry points without publishing the old vault.
    aliases = {
        "portfolio": "/",
        "portfolio/projects": "/#work",
        "portfolio/projects/nhis-rpa": "/projects/nhis-billing/",
        "portfolio/projects/nhis-rpa/db-schema": "/projects/nhis-billing/#model",
        "portfolio/projects/nhis-rpa/ocr-flow": "/projects/nhis-billing/#ocr",
        "portfolio/projects/edu-data-pipeline": "/projects/education-db/",
        "portfolio/projects/edu-data-pipeline/schema-design": "/projects/education-db/#erd",
    }
    for old, new in aliases.items():
        folder = OUT / old
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "index.html").write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0;url=' + new + '"><title>새 포트폴리오로 이동</title><p><a href="' + new + '">새 포트폴리오로 이동</a></p></html>')
    print(json.dumps({"pages": len(PAGES), "redirects": len(aliases), "output": str(OUT)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
