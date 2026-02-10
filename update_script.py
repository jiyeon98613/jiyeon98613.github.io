import requests
import xml.etree.ElementTree as ET
import os
from datetime import datetime

NAT_KEY = os.environ.get('NAT_API_KEY')

def get_data():
    url = "http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire"
    params = {
        'serviceKey': NAT_KEY,
        'Q0': '경기도',
        'Q1': '부천시',
        'numOfRows': '500'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        return root.findall('.//item')
    return []

def format_time(t_str):
    if not t_str or len(t_str) < 4: return "휴무"
    return f"{t_str[:2]}:{t_str[2:4]}"

def write_markdown(items):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"_posts/{today}-bucheon-seol-weekly.md"
    
    # 날짜와 해당 날짜의 요일/공휴일 속성 정의 (2/14 토 ~ 2/20 금)
    # 8번은 공휴일(설 연휴), 나머지는 요일 번호
    schedule_config = [
        {"label": "2/14(토)", "code": "6"},
        {"label": "2/15(일)", "code": "7"},
        {"label": "2/16(월)", "code": "1"},
        {"label": "2/17(화)", "code": "8"}, # 설 연휴 (공휴일)
        {"label": "2/18(수)", "code": "8"}, # 설 연휴 (공휴일)
        {"label": "2/19(목)", "code": "8"}, # 설 연휴 (공휴일)
        {"label": "2/20(금)", "code": "5"}
    ]
    
    markers = ""
    table_html = ""
    
    for item in items:
        name = item.findtext('dutyName')
        addr = item.findtext('dutyAddr')
        tel = item.findtext('dutyTel1')
        lat = item.findtext('wgs84Lat')
        lon = item.findtext('wgs84Lon')
        
        times = []
        for day in schedule_config:
            code = day["code"]
            s = item.findtext(f'dutyTime{code}s')
            e = item.findtext(f'dutyTime{code}e')
            times.append(f"{format_time(s)} ~ {format_time(e)}")

        if lat and lon:
            markers += f'L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{name}</b><br>전화: {tel}");\n        '
            
            # HTML 표 구조 (왼쪽 3단 정보 / 오른쪽 7단 시간)
            table_html += f"""
<table style="width:100%; border: 1px solid #ddd; border-collapse: collapse; margin-bottom: 25px; font-size: 13px;">
  <tr style="background: #f4f4f4;">
    <td style="width: 25%; padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #2c3e50;">{name}</td>
    {"".join([f'<td style="width: 10.7%; padding: 5px; border: 1px solid #ddd; text-align: center; font-weight: bold;">{d["label"]}</td>' for d in schedule_config])}
  </tr>
  <tr>
    <td style="padding: 10px; border: 1px solid #ddd; color: #34495e;">📞 {tel}</td>
    {"".join([f'<td rowspan="2" style="text-align: center; border: 1px solid #ddd; font-size: 11px;">{t}</td>' for t in times])}
  </tr>
  <tr>
    <td style="padding: 10px; border: 1px solid #ddd; font-size: 11px; color: #7f8c8d;">📍 {addr}</td>
  </tr>
</table>
"""

    content = f"""---
layout: post
title: "부천시 설 연휴 주간(2/14~2/20) 약국 운영 안내"
date: {today}
categories: [ 약국정보 ]
featured: true
author: sal
---

2026년 설 연휴 기간 동안 부천시 내 약국 운영 시간입니다. 
**공휴일 특성상 운영 시간이 변동될 수 있으니, 방문 전 반드시 전화로 확인하시기 바랍니다.**

### 📍 약국 위치 지도
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<div id="map" style="height: 400px; border-radius: 10px; margin-bottom: 30px; border: 1px solid #ccc;"></div>
<script>
    var map = L.map('map').setView([37.503, 126.766], 13);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
    {markers}
</script>

### 📋 약국별 상세 운영 시간
{table_html}
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    data = get_data()
    if data: write_markdown(data)
    if data:
        write_markdown(data)
        print(f"성공: {len(data)}개 약국 지도 및 표 생성 완료")
