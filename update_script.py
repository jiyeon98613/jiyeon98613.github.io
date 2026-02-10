import requests
import xml.etree.ElementTree as ET
import os
from datetime import datetime

# API 키 설정
NAT_KEY = os.environ.get('NAT_API_KEY')
GG_KEY = os.environ.get('GG_API_KEY')

def get_gg_status():
    """경기도 API에서 부천시 약국들의 현재 영업 상태(영업/폐업) 가져오기"""
    url = f"https://openapi.gg.go.kr/Pharmst?KEY={GG_KEY}&Type=json&SIGUN_NM=%EB%B6%80%EC%B2%9C%EC%8B%9C"
    try:
        res = requests.get(url)
        rows = res.json()['Pharmst'][1]['row']
        # 영업 상태가 '영업'인 곳의 이름만 세트로 저장
        return {row['BIZPLC_NM']: row['BSN_STATE_NM'] for row in rows}
    except:
        return {}

def get_nat_data():
    """전국 API에서 상세 운영 정보 가져오기"""
    url = "http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire"
    params = {'serviceKey': NAT_KEY, 'Q0': '경기도', 'Q1': '부천시', 'numOfRows': '500'}
    res = requests.get(url, params=params)
    if res.status_code == 200:
        root = ET.fromstring(res.content)
        return root.findall('.//item')
    return []

def format_time(t_str):
    if not t_str or len(t_str) < 4: return None
    return f"{t_str[:2]}:{t_str[2:4]}"

def write_markdown(nat_items, gg_status):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"_posts/{today}-bucheon-seol-final.md"
    
    schedule_config = [
        {"label": "2/14(토)", "code": "6", "is_holiday": False},
        {"label": "2/15(일)", "code": "7", "is_holiday": False},
        {"label": "2/16(월)", "code": "1", "is_holiday": False},
        {"label": "2/17(화)", "code": "2", "is_holiday": True}, # 설연휴
        {"label": "2/18(수)", "code": "3", "is_holiday": True}, # 설연휴
        {"label": "2/19(목)", "code": "4", "is_holiday": True}, # 설연휴
        {"label": "2/20(금)", "code": "5", "is_holiday": False}
    ]

    groups = {i: [] for i in range(8)} 
    markers = ""

    for item in nat_items:
        name = item.findtext('dutyName')
        # 경기도 API 대조: 영업 중이 아니면 제외
        if name in gg_status and gg_status[name] != '영업':
            continue

        addr = item.findtext('dutyAddr')
        tel = item.findtext('dutyTel1')
        lat = item.findtext('wgs84Lat')
        lon = item.findtext('wgs84Lon')
        
        times = []
        open_count = 0
        
        for day in schedule_config:
            s, e = None, None
            # 두 API 대조 로직: 공휴일(8) 우선 확인 후 평일 요일 대조
            if day["is_holiday"]:
                s = item.findtext('dutyTime8s')
                e = item.findtext('dutyTime8e')
            
            # 하나라도 휴무 여부가 드러나면(시작시간이 아예 없으면) 휴무 확정
            if not s:
                s = item.findtext(f'dutyTime{day["code"]}s')
            if not e:
                e = item.findtext(f'dutyTime{day["code"]}e')
            
            f_s = format_time(s)
            f_e = format_time(e)
            
            if f_s:
                # 시작은 있는데 끝이 없으면 ??:?? 로 표시
                display_time = f"{f_s} ~ {f_e if f_e else '??:??'}"
                times.append(display_time)
                open_count += 1
            else:
                times.append("휴무")

        if lat and lon:
            markers += f'L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{name}</b>");\n        '
            groups[open_count].append({"name": name, "tel": tel, "addr": addr, "times": times})

    # 바로가기 메뉴 생성
    labels = {7: "7일 모두 운영", 6: "6일 운영", 5: "5일 운영", 4: "4일 운영", 3: "3일 운영", 2: "2일 운영", 1: "1일 운영"}
    menu_html = '<div style="background: #f0f0f0; padding: 15px; border-radius: 8px; margin-bottom: 30px; text-align: center;">'
    for i in range(7, 0, -1):
        if groups[i]:
            menu_html += f'<a href="#group-{i}" style="margin: 0 10px; text-decoration: none; color: #007bff; font-weight: bold;">[{labels[i]}]</a> '
    menu_html += '</div>'

    content = f"""---
layout: post
title: "부천시 설 연휴(2/14~2/20) 영업 약국 최종 안내"
date: {today}
categories: [ 약국정보 ]
featured: true
author: sal
---

경기도 인허가 정보와 전국 약국 정보를 대조한 가장 정확한 리스트입니다.

### 📍 약국 위치 지도
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<div id="map" style="height: 400px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #ccc;"></div>
<script>
    var map = L.map('map').setView([37.503, 126.766], 13);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
    {markers}
</script>

### ⚡ 바로가기 메뉴
{menu_html}

"""
    for i in range(7, 0, -1):
        if not groups[i]: continue
        content += f'\n<h2 id="group-{i}" style="padding-top: 60px; margin-top: -40px;">🏥 {labels[i]} ({len(groups[i])}곳)</h2>\n'
        for pharm in groups[i]:
            table_html = f"""
<table style="width:100%; border: 1px solid #ddd; border-collapse: collapse; margin-bottom: 20px; font-size: 12px;">
  <tr style="background: #f8f9fa;">
    <td style="width: 25%; padding: 8px; border: 1px solid #ddd; font-weight: bold;">{pharm['name']}</td>
    {"".join([f'<td style="width: 10.7%; padding: 5px; border: 1px solid #ddd; text-align: center; font-weight: bold;">{d["label"]}</td>' for d in schedule_config])}
  </tr>
  <tr>
    <td style="padding: 8px; border: 1px solid #ddd;">📞 {pharm['tel']}</td>
    {"".join([f'<td rowspan="2" style="text-align: center; border: 1px solid #ddd;">{t}</td>' for t in pharm['times']])}
  </tr>
  <tr>
    <td style="padding: 8px; border: 1px solid #ddd; color: #777;">📍 {pharm['addr']}</td>
  </tr>
</table>
"""
            content += table_html

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    gg_status = get_gg_status()
    nat_items = get_nat_data()
    if nat_items: write_markdown(nat_items, gg_status)
