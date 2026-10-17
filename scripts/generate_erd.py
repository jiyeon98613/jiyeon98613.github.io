"""Render the existing 15-table education design as a source-controlled SVG."""
from html import escape
from pathlib import Path

NODES = {
    'REFERENCE_SOURCE_TYPE': (45, 100, ['PK code', 'label', 'is_active']),
    'REFERENCE': (45, 420, ['PK reference_id', 'FK source_type', 'title / license / trust_score']),
    'LOAD_BATCH': (45, 740, ['PK load_id', 'source / script_git_sha', 'status / loaded_at']),
    'PROBLEM_TEMPLATE': (455, 100, ['PK problem_template_id', 'FK load_id', 'template_detail / grade']),
    'PROBLEM_INSTANCE': (865, 100, ['PK problem_instance_id', 'FK template / reference / load', 'source_data_name / answer']),
    'DIFFICULTY_ASSESSMENT': (1275, 100, ['PK assessment_id', 'FK problem_template_id', 'assessor / difficulty / method']),
    'SOLUTION': (455, 420, ['PK solution_id', 'FK template / reference / load', 'approach_type']),
    'SOLUTION_STEP_MAP': (865, 420, ['PK, FK solution_id', 'PK, FK solution_step_id', 'sequence']),
    'SOLUTION_STEP': (1275, 420, ['PK solution_step_id', 'FK load_id', 'step_text']),
    'TEMPLATE_STANDARD': (455, 740, ['PK, FK problem_template_id', 'PK, FK achievement_standard_id']),
    'ACHIEVEMENT_STANDARD': (865, 740, ['PK achievement_standard_id', 'code / revision_year', 'description']),
    'STEP_STANDARD': (1275, 740, ['PK, FK solution_step_id', 'PK, FK achievement_standard_id']),
    'STEP_CONCEPT': (455, 1060, ['PK, FK solution_step_id', 'PK, FK core_concept_id']),
    'STANDARD_MAP': (865, 1060, ['PK, FK from_standard_id', 'PK, FK to_standard_id', 'relation_type']),
    'CORE_CONCEPT': (1275, 1060, ['PK core_concept_id', 'title / concept_definition']),
}
EDGES = [
    ('REFERENCE_SOURCE_TYPE','REFERENCE'), ('REFERENCE','PROBLEM_INSTANCE'),
    ('REFERENCE','SOLUTION'), ('PROBLEM_TEMPLATE','PROBLEM_INSTANCE'),
    ('PROBLEM_TEMPLATE','DIFFICULTY_ASSESSMENT'), ('PROBLEM_TEMPLATE','SOLUTION'),
    ('PROBLEM_TEMPLATE','TEMPLATE_STANDARD'), ('SOLUTION','SOLUTION_STEP_MAP'),
    ('SOLUTION_STEP','SOLUTION_STEP_MAP'), ('SOLUTION_STEP','STEP_STANDARD'),
    ('SOLUTION_STEP','STEP_CONCEPT'), ('CORE_CONCEPT','STEP_CONCEPT'),
    ('ACHIEVEMENT_STANDARD','TEMPLATE_STANDARD'), ('ACHIEVEMENT_STANDARD','STEP_STANDARD'),
    ('ACHIEVEMENT_STANDARD','STANDARD_MAP'), ('ACHIEVEMENT_STANDARD','STANDARD_MAP'),
    ('LOAD_BATCH','PROBLEM_TEMPLATE'), ('LOAD_BATCH','PROBLEM_INSTANCE'),
    ('LOAD_BATCH','SOLUTION'), ('LOAD_BATCH','SOLUTION_STEP'),
]

def main():
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1325" role="img" aria-labelledby="title desc">',
             '<title id="title">Education database ERD: 15 tables and 20 foreign keys</title>',
             '<desc id="desc">Templates, instances, solutions, steps, standards, concepts, references and load batches. Dashed lines identify load batch references. Two standard map foreign keys reference the same standard table.</desc>',
             '<defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto"><path d="M0 0 L6 3 L0 6" fill="none" stroke="#789382" stroke-width="1.2"/></marker></defs>',
             '<rect width="1600" height="1325" rx="20" fill="#f0f4ed"/>',
             '<text x="45" y="48" font-family="Arial,sans-serif" font-size="18" fill="#486f56" letter-spacing="2">EDUCATION DATABASE / 15 TABLES · 20 FOREIGN KEYS</text>']
    for index,(a,b) in enumerate(EDGES):
        x,y,_ = NODES[a];tx,ty,_=NODES[b];dash=a=='LOAD_BATCH'
        if abs(tx-x) < 10:
            sx=x+145;sy=y+155;ex=tx+145;ey=ty
        elif tx>x:
            sx=x+280;sy=y+77;ex=tx;ey=ty+77
        else:
            sx=x;sy=y+77;ex=tx+280;ey=ty+77
        if a=='ACHIEVEMENT_STANDARD' and b=='STANDARD_MAP':
            offset=25 if index%2 else -25;sx+=offset;ex+=offset
        mx=(sx+ex)/2
        path=f'M {sx} {sy} C {mx} {sy}, {mx} {ey}, {ex} {ey}'
        dash_attr = 'stroke-dasharray="6 6"' if dash else ''
        parts.append(f'<path d="{path}" fill="none" stroke="{"#acbba5" if dash else "#789382"}" stroke-width="1.7" opacity="{"0.65" if dash else "0.85"}" {dash_attr} marker-end="url(#arrow)"/>')
    for name,(x,y,fields) in NODES.items():
        dark=name=='PROBLEM_TEMPLATE'
        parts.extend([f'<g id="{name}"><rect x="{x}" y="{y}" width="280" height="155" rx="10" fill="{"#234f3d" if dark else "#fff"}" stroke="{"#234f3d" if dark else "#bccfb5"}"/>',
                      f'<text x="{x+16}" y="{y+31}" font-family="Arial,sans-serif" font-size="14" font-weight="700" fill="{"#edf4e9" if dark else "#315a3f"}">{name}</text>',
                      f'<line x1="{x+15}" x2="{x+265}" y1="{y+47}" y2="{y+47}" stroke="{"#ffffff35" if dark else "#dce6d5"}"/>'])
        for i,field in enumerate(fields):
            parts.append(f'<text x="{x+16}" y="{y+76+i*23}" font-family="monospace" font-size="12" fill="{"#c8ddbf" if dark else "#6c7e65"}">{escape(field)}</text>')
        parts.append('</g>')
    parts.extend(['<text x="45" y="1280" font-family="Arial,sans-serif" font-size="14" fill="#71846a">Solid: entity reference · Dashed: load batch reference · Common timestamps omitted</text>',
                  '<text x="45" y="1303" font-family="Arial,sans-serif" font-size="12" fill="#8b9b85">Based on the July 2026 schema design. Structure verification only; no ingestion claim.</text></svg>'])
    path=Path(__file__).resolve().parents[1]/'public/assets/education-erd.svg'
    path.write_text('\n'.join(parts))
    print('Generated education-erd.svg: 15 tables / 20 FK relationships')

if __name__ == '__main__':
    main()
