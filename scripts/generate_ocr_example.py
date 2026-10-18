"""Generate an explicitly fictional before/after illustration, never patient data."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def text(x, y, value, cls='body'):
    return f'<text x="{x}" y="{y}" class="{cls}">{escape(value)}</text>'


def document(x, *, masked):
    parts = [f'<rect x="{x}" y="100" width="640" height="650" rx="4" fill="white" stroke="#ccd4de"/>']
    parts += [text(x + 26, 142, '가상 양압기 처방전'), text(x + 26, 167, '설명용 가상 서식 · 실제 환자 원본 아님', 'small')]
    if masked:
        parts.append(f'<rect x="{x + 1}" y="187" width="638" height="128" fill="#202631"/>')
        parts += [text(x + 26, 242, '환자 신원 영역 마스킹', 'masked'), text(x + 26, 274, '이미지에서 식별정보를 가린 뒤 관리자 확인', 'masked-small')]
    else:
        for y, value in [(223, '성명: 가상 환자 A'), (258, '주민번호: XXXXXX-XXXXXXX'), (293, '전화: 010-XXXX-XXXX')]:
            parts.append(text(x + 26, y, value))
    parts += [text(x + 26, 353, '진료과목 · 처방 항목', 'heading')]
    for y, value in [(397, '기기 종류: □ CPAP   ■ APAP'), (435, '설정 압력: 최소 6 / 최대 12'), (473, '처방기간: 2026-10-01 ~ 2026-10-31'), (511, '순응 구분: □ 중   ■ 후')]:
        parts.append(text(x + 26, y, value))
    parts += [f'<line x1="{x + 26}" y1="544" x2="{x + 614}" y2="544" stroke="#dce2e9"/>', text(x + 26, 575, '교부일로부터 사용기간 내에 대여', 'small')]
    if masked:
        parts.append(f'<rect x="{x + 1}" y="595" width="638" height="154" fill="#202631"/>')
        parts += [text(x + 26, 653, '의료기관 · 의사 · 발행일 영역 마스킹', 'masked')]
    else:
        for y, value in [(632, '의료기관: 예시 의료기관'), (668, '담당 의사: 예시 의사'), (704, '발행일: 2026-09-30')]:
            parts.append(text(x + 26, y, value))
    return '\n'.join(parts)


def main():
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="850" viewBox="0 0 1440 850" role="img" aria-labelledby="title desc">
<title id="title">가상 처방전의 마스킹 전후</title><desc id="desc">왼쪽은 가상 신원정보와 처방 항목을 넣은 설명용 문서, 오른쪽은 상단 신원과 하단 의료기관·발행일 영역을 가린 예시입니다. 실제 원본이나 실행 결과가 아닙니다.</desc>
<style>text{font-family:Pretendard,'Noto Sans KR',sans-serif;fill:#344256}.heading{font-size:22px;font-weight:600}.body{font-size:21px}.small{font-size:16px;fill:#6b7685}.masked{font-size:20px;fill:white}.masked-small{font-size:16px;fill:#dbe3ef}.label{font-size:23px;font-weight:600}.caption{font-size:17px;fill:#6b7685}</style><rect width="1440" height="850" fill="#fafbfc"/>
'''
    svg += text(52, 56, '전 · 로컬에서 원본 판독', 'label')
    svg += text(748, 56, '후 · 관리자 확인용 마스킹 이미지', 'label')
    svg += document(52, masked=False) + document(748, masked=True)
    svg += text(52, 797, '모든 값은 가상입니다. 마스킹 위치와 정보 분담을 설명하기 위해 서식을 간략화했습니다.', 'caption')
    svg += text(52, 825, '실제 처리에서는 기준 문구를 찾지 못하면 외부 전송을 중단합니다.', 'caption')
    svg += '</svg>\n'
    (ROOT / 'public/assets/ocr-masking-example.svg').write_text(svg)
    print('Generated fictional OCR masking illustration')


if __name__ == '__main__':
    main()
