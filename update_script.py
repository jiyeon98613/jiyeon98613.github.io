import requests
import xml.etree.ElementTree as ET
import os
from datetime import datetime

NAT_KEY = os.environ.get('NAT_API_KEY')

def get_data():
    url = "http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire"
    params = {'serviceKey': NAT_KEY, 'Q0': '경기도', 'Q1': '부천시', 'numOfRows': '500'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        return root.findall('.//item')
    return []

def format_time(t_str):
    if not t_str or len(t_str) < 4: return None
    return f"{t_str[:2]}:{t_str[2:4]}"

def write_markdown(items):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"_posts/{today}-bucheon-seol-weekly.md"
    
    # 설정: 2/14(토) ~ 2/20(금)
    # code_map은 해당 날짜가 평소 무슨 요일인지(1~7) 알려줍니다.
    schedule_config = [
        {"label": "2/14(토)", "code": "6", "is_holiday": False},
        {"label": "2/15(일)", "code": "7", "is_holiday": False},
        {"label": "2/16(월)", "code": "1", "is_holiday": False},
        {"label": "2/17(화)", "code": "2", "is_holiday": True}, # 설연휴
        {"label": "2/18(수)", "code": "3", "is_holiday": True}, # 설연휴
        {"label": "2/19(목)", "code": "4", "is_holiday": True}, # 설연휴
        {"label": "2/20(금)", "code": "5", "is_holiday": False}
    ]

    # 운영 일수별 그룹 저장소
    groups = {i: [] for i in range(8)} 
    markers = ""

    for item in items:
        name = item.findtext('dutyName')
        addr = item.findtext('dutyAddr')
        tel = item.findtext('dutyTel1')
        lat = item.findtext('wgs84Lat')
        lon = item.findtext('wgs84Lon')
        
        times = []
        open_count = 0
        
        for day in schedule_config:
            # 1. 해당 날짜가 공휴일(설날)인 경우 8번 데이터 우선 확인
            s = None
            e = None
            if day["is_holiday"]:
                s = item.findtext('dutyTime8s')
                e = item.findtext('dutyTime8e')
            
            # 2. 공휴일 데이터가 없으면 평소 해당 요일 데이터 사용
            if not s:
                s = item.findtext(f'dutyTime{day["code"]}s')
            if not e:
                e = item.findtext(f'dutyTime{day["code"]}e')
            
            # 3. 가공 및 판정 (시작시간이 있으면 무조건 운영하는 것으로 간주)
            f_s = format_time(s)
            f_e = format_time(e)
            
            if f_s:
                # 시작은 있는데 종료가 없으면 평일 종료시간이나 18:00으로 임시 보완 (데이터 유실 대비)
                display_time = f"{f_s} ~ {f_e if f_e else '18:00'}"
                times.append(display_time)
                open_count += 1
            else:
                times.append("휴무")

        if lat and lon:
            markers += f'L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{name}</b>");\n        '
            groups[open_count].append({"name": name, "tel": tel, "addr": addr, "times": times})

    # 마크다운 생성
    content = f"""---
layout: post
title: "부천시 설 연휴(2/14~2/20) 운영 일수별 약국 안내"
date: {today}
categories: [ 약국정보 ]
featured: true
author: sal
---

부천시 약국들의 **설 연휴 포함 7일간 운영 정보**입니다. 운영 일수가 많은 순서대로 정리하였습니다.

### 📍 약국 위치 지도
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<div id="map" style="height: 400px; border-radius: 10px; margin-bottom: 30px; border: 1px solid #ccc;"></div>
<script>
    var map = L.map('map').setView([37.503, 126.766], 13);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
    {markers}
</script>
"""

    # 그룹별로 표 생성 (7일부터 1일까지 역순)
    labels = ["휴무 없음 (7일 모두 운영)", "6일 운영", "5일 운영", "4일 운영", "3일 운영", "2일 운영", "1일 운영", "운영 안함"]
    for i in range(7, 0, -1):
        if not groups[i]: continue
        
        content += f"\n## 🏥 {labels[7-i]} ({len(groups[i])}곳)\n"
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
    data = get_data()
    if data: write_markdown(data)
