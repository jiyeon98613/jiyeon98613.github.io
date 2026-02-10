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

def write_markdown(items):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"_posts/{today}-bucheon-pharmacy-list.md"
    
    # 지도 마커 데이터 생성
    markers = ""
    table_rows = ""
    
    for item in items:
        name = item.findtext('dutyName')
        addr = item.findtext('dutyAddr')
        tel = item.findtext('dutyTel1')
        lat = item.findtext('wgs84Lat')
        lon = item.findtext('wgs84Lon')
        
        # 운영시간 (설날/공휴일은 보통 dutyTime8s 또는 당일 요일 확인)
        # 여기서는 기본적으로 월요일(1)부터 일요일(7), 공휴일(8) 중 공휴일 시간 우선 추출
        time = item.findtext('dutyTime8s') or item.findtext('dutyTime1s') or "정보없음"
        if time != "정보없음" and len(time) > 4:
            time = f"{time[:2]}:{time[2:4]} ~ {time[4:6]}:{time[6:8]}"

        if lat and lon:
            # 지도 마커 코드
            markers += f'L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{name}</b><br>{time}");\n        '
            # 표 내용 (좌표 제외)
            table_rows += f"| {name} | {addr} | {tel} | {time} |\n"

    content = f"""---
layout: post
title: "[{today}] 부천시 설날 운영 약국 지도 안내"
date: {today}
categories: [ 약국정보 ]
featured: true
---

### 📍 부천시 약국 위치 지도
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<div id="map" style="height: 450px; border-radius: 10px; margin-bottom: 20px;"></div>
<script>
    var map = L.map('map').setView([37.503, 126.766], 13);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        attribution: '&copy; OpenStreetMap'
    }}).addTo(map);
    {markers}
</script>

### 📋 상세 리스트 (운영시간 포함)

| 약국명 | 주소 | 전화번호 | 운영시간 |
| :--- | :--- | :--- | :--- |
{table_rows}
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    data = get_data()
    if data:
        write_markdown(data)
        print(f"성공: {len(data)}개 약국 지도 및 표 생성 완료")
