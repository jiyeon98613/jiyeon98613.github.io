"""Draw the selected billing tables from the current PostgreSQL ORM model.

Source: nhis-macro-core/core/models.py (2026-10-17).
Only selected columns and FK relations are shown; no application data is used.
"""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1440, 720
TABLES = [
    ('patient_documents', '환자 문서', 44, 60, 368, [
        ('PK', 'doc_id', 'uuid'),
        ('FK*', 'pat_id', 'uuid'),
        ('', 'doc_type', 'varchar'),
        ('', 'file_status', 'varchar'),
    ]),
    ('prescriptions', '처방전', 44, 366, 368, [
        ('PK', 'ps_id', 'uuid'),
        ('FK·UQ', 'doc_id', 'uuid'),
        ('', 'is_valid', 'boolean'),
        ('FK', 'superseded_by_ps_id', 'uuid'),
        ('', 'superseded_date', 'date'),
        ('', 'start_date / end_date', 'date'),
    ]),
    ('patient_monthly_billing_cycle_records', '월별 업무·계산 근거', 520, 60, 420, [
        ('PK', 'record_id', 'uuid'),
        ('FK', 'billing_cycle_id', 'uuid'),
        ('FK', 'doc_id', 'uuid'),
        ('FK*', 'assigned_history_id', 'uuid'),
        ('FK*', 'travel_id', 'uuid'),
        ('FK*', 'billing_charge_item_id', 'uuid'),
    ]),
    ('patient_monthly_billing_cycles', '환자별 월 관리', 520, 366, 420, [
        ('PK', 'billing_cycle_id', 'uuid'),
        ('FK*', 'pat_id', 'uuid'),
        ('', 'billing_month', 'varchar'),
        ('', 'status', 'varchar'),
    ]),
    ('claim_docs', '청구별 요구·첨부 문서', 1030, 60, 366, [
        ('PK', 'claim_doc_id', 'uuid'),
        ('FK', 'claim_id', 'uuid'),
        ('FK', 'doc_id', 'uuid'),
        ('', 'requirement_key', 'varchar'),
        ('', 'attachment_role', 'varchar'),
    ]),
    ('claims', '기간별 청구', 1030, 366, 366, [
        ('PK', 'claim_id', 'uuid'),
        ('FK', 'billing_cycle_id', 'uuid'),
        ('FK', 'ps_id', 'uuid'),
        ('', 'segment_index', 'integer'),
        ('', 'period_start', 'date'),
        ('', 'period_end', 'date'),
        ('', 'billing_rate', 'integer'),
    ]),
]

def text(x, y, value, cls='column', anchor=None):
    extra = f' text-anchor="{anchor}"' if anchor else ''
    return f'<text x="{x}" y="{y}" class="{cls}"{extra}>{escape(value)}</text>'

def label(x, y, value, width):
    return f'<rect x="{x - 5}" y="{y - 13}" width="{width}" height="20" fill="white"/>' + text(x, y, value, 'edge-label')

def main():
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" aria-labelledby="title desc">
<title id="title">건강보험 청구 시스템 ERD</title>
<desc id="desc">실제 runtime 스키마의 6개 테이블 발췌. 화살표는 외래키에서 참조 대상으로 향합니다. 처방전의 자기참조, 월별 관리와 기간별 청구, 월별 근거와 청구별 첨부 관계를 표시합니다.</desc>
<defs><marker id="fk-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10" fill="none" stroke="#71839a" stroke-width="1.5"/></marker></defs>
<style>text{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;fill:#344256}}.table-name{{font-size:13px;font-weight:600;letter-spacing:-.3px}}.table-note{{font-family:Pretendard,'Noto Sans KR',sans-serif;font-size:11px;fill:#77818e}}.column{{font-size:12px}}.key{{font-size:10px;fill:#52749d}}.type{{font-size:10px;fill:#929aa5}}.edge-label{{font-size:10px;fill:#65788e}}.legend{{font-family:Pretendard,'Noto Sans KR',sans-serif;font-size:11px;fill:#78828f}}.edge{{fill:none;stroke:#8394a8;stroke-width:1.2;marker-end:url(#fk-arrow)}}</style>
<rect width="100%" height="100%" fill="white"/>
''']
    # Each arrow starts at a child table and ends at its referenced table.
    for path in [
        'M520 181 H412',                            # record.doc_id -> document
        'M730 292 V366',                            # record.billing_cycle_id -> cycle
        'M208 366 V238',                            # prescription.doc_id -> document
        'M1030 455 H940',                           # claim.billing_cycle_id -> cycle
        'M1213 265 V366',                           # claim_doc.claim_id -> claim
        'M1260 60 V24 H252 V60',                     # claim_doc.doc_id -> document
        'M1220 625 V668 H234 V598',                  # claim.ps_id -> prescription
        'M44 512 H16 V445 H44',                      # prescription supersession self FK
    ]:
        parts.append(f'<path class="edge" d="{path}"/>')
    for item in [
        (436, 174, 'doc_id', 53),
        (744, 335, 'billing_cycle_id', 111),
        (223, 309, 'doc_id · UQ', 84),
        (950, 447, 'N : 1', 55),
        (1225, 322, 'claim_id', 70),
        (703, 24, 'doc_id', 58),
        (716, 668, 'ps_id', 51),
    ]:
        parts.append(label(*item))
    for name, note, x, y, w, fields in TABLES:
        h = 52 + len(fields) * 27 + 18
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="white" stroke="#ccd4de"/>')
        parts.append(f'<path d="M{x} {y + 52} H{x + w}" stroke="#dce2e9"/>')
        parts.append(text(x + 15, y + 22, name, 'table-name'))
        parts.append(text(x + 15, y + 40, note, 'table-note'))
        for i, (key, column, typ) in enumerate(fields):
            row_y = y + 76 + i * 27
            parts.append(text(x + 13, row_y, key, 'key'))
            parts.append(text(x + 63, row_y, column))
            parts.append(text(x + w - 14, row_y, typ, 'type', 'end'))
    parts.append(text(44, 706, 'runtime 스키마 · 주요 컬럼 발췌 · 화살표: FK → 참조 대상 · UQ: 유일성 제약 · FK*: 참조 테이블 생략', 'legend'))
    parts.append('</svg>')
    target = ROOT / 'public/assets/nhis-billing-erd.svg'
    target.write_text('\n'.join(parts) + '\n')
    print('Generated billing ERD: 6 actual tables, 8 FK relations')

if __name__ == '__main__':
    main()
