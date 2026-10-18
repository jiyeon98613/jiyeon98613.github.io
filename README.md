# 김지연 · PostgreSQL DBA 포트폴리오

건강보험 청구 시스템의 데이터 모델링·OCR 개선 과정, 관리자 콘솔의 실제 UI와 DB·백엔드 기여, 교육용 DB 설계와 PostgreSQL 운영 실습 기록을 소개하는 정적 사이트입니다.

게시 주소: https://jiyeon98613.github.io/

## 구성

- 홈: 소개와 대표 프로젝트
- PostgreSQL 운영 실습: 실제 백업 복구, 기존 인덱스 비교, 권한 분리, 복제·PITR·CloudNativePG 장애조치
- 건강보험 청구 시스템: 문서 유효성·대체, 월별 관리·기간별 청구, OCR의 역할 분리
- 관리자 콘솔: 실제 UI에 가상 API 응답을 넣어 촬영한 화면과 담당 범위
- 교육용 DB: 15개 테이블 설계, DDL 생성·카탈로그 확인 범위
- 소개: 경력, 기술, 협업·AI 활용, GitHub 링크

## 로컬 실행

Python 3.11 이상만 있으면 빌드할 수 있습니다. 런타임 외부 패키지와 데이터베이스가 필요하지 않습니다.

    python3 scripts/generate_erd.py
    python3 scripts/generate_billing_erd.py
    python3 scripts/generate_ocr_example.py
    python3 build.py
    python3 scripts/check_site.py
    python3 -m http.server 4173 --bind 127.0.0.1 --directory dist

브라우저에서 http://127.0.0.1:4173 을 엽니다.

## 글과 디자인 수정

| 경로 | 역할 |
| --- | --- |
| content/home.html | 첫 화면과 대표 프로젝트 |
| content/ops.html | PostgreSQL 운영 실습과 결과·GitHub 기록 |
| content/billing.html | 청구 시스템 설계 사례 |
| content/console.html | 관리자 콘솔과 기여 범위 |
| content/education.html | 교육용 데이터베이스 설계 |
| content/about.html | 소개와 경력 |
| templates/base.html | 공통 메뉴·메타데이터·푸터 |
| public/assets/site.css | 반응형 레이아웃·색·타이포그래피 |
| public/assets/site.js | 메뉴·문서 사례·청구 타임라인·이미지 확대 |
| scripts/generate_erd.py | 교육용 ERD SVG의 재생성 |
| scripts/generate_billing_erd.py | 청구 관련 실제 테이블·주요 컬럼의 ERD 재생성 |
| scripts/generate_ocr_example.py | 가상 처방전의 마스킹 전후 설명용 SVG 재생성 |
| docs/CONTENT_EVIDENCE.md | 주장별 근거와 검증 범위 |

본문은 HTML 파일로 관리하며 Obsidian 동기화와 독립되어 있습니다. 수정 후 빌드와 검사를 실행합니다.

## 공개 자료의 범위

화면 이미지는 실제 콘솔 컴포넌트에 가상 데이터만 주입해 촬영했습니다. 운영 API, 환자 원본, 비공개 소스와 인증정보는 사이트에 포함하지 않습니다. UI는 협업 결과물이며 본인의 DB·백엔드 기여를 따로 표시합니다.

규모 수치는 2026년 10월 이력서의 기준과 집계 범위를 함께 표시했습니다. 교육용 DB는 스키마 설계·생성 검증까지 소개하며 실제 적재·성능 개선 완료로 표현하지 않습니다.

## 배포

main 브랜치에서 사이트 소스를 관리하고, 빌드·검사를 통과한 dist 내용만 gh-pages 브랜치에 반영합니다. GitHub Pages의 게시 소스는 gh-pages 브랜치의 루트입니다. 새 버전도 빌드와 검사를 마친 뒤 배포 브랜치를 갱신합니다. 과거 포트폴리오의 비공개 자료는 배포에 포함하지 않습니다.

기존 이력서의 주요 /portfolio/ 문서 주소는 대응하는 새 프로젝트로 이동하도록 별칭을 제공합니다.

## 자산

Pretendard 글꼴은 SIL Open Font License 1.1로 배포되며 라이선스는 public/assets/Pretendard-LICENSE.txt에 포함되어 있습니다. 화면과 도해의 공개 범위는 본문과 근거 문서를 따릅니다.
