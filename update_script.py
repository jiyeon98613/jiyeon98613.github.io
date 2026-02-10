import requests
import xml.etree.ElementTree as ET
import os
from datetime import datetime
import urllib.parse

NAT_KEY = os.environ.get('NAT_API_KEY')
GG_KEY = os.environ.get('GG_API_KEY')

def get_gg_status():
    url = f"https://openapi.gg.go.kr/Pharmst?KEY={GG_KEY}&Type=json&SIGUN_NM=%EB%B6%80%EC%B2%9C%EC%8B%9C"
    try:
        res = requests.get(url)
        data = res.json()
        rows = data['Pharmst'][1]['row']
        return {row['BIZPLC_NM']: row['BSN_STATE_NM'] for row in rows}
    except:
        return {}

def get_nat_data():
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
    filename = f"_posts/{today}-bucheon-seol-perfect.md"
    
    schedule_config = [
        {"label": "2/14(토)", "code": "6", "is_holiday": False},
        {"label": "2/15(일)", "code": "7", "is_holiday": False},
        {"label": "2/16(월)", "code": "1", "is_holiday": False},
        {"label": "2/17(화)", "code": "2", "is_holiday": True},
        {"label": "2/18(수)", "code": "3", "is_holiday": True},
        {"label": "2/19(목)", "code": "4", "is_holiday": True},
        {"label": "2/20(금)", "code": "5", "is_holiday": False}
    ]

    groups = {i: [] for i in range(8)} 
    markers = ""

    for item in nat_items:
        name = item.findtext('dutyName')
        if name in gg_status and gg_status[name] != '영업': continue

        addr = item.findtext('dutyAddr')
        tel = item.findtext('dutyTel1')
        lat = item.findtext('wgs84Lat')
        lon = item.findtext('wgs84Lon')
        
        # 검색용 쿼리 인코딩 (네이버, 구글용)
        encoded_name = urllib.parse.quote(f"부천 {name}")
        naver_url = f"https://search.naver.com/search.naver?query={encoded_name}"
        google_url = f"https://www.google.com/maps/search/{encoded_name}"

        times = []
        open_count = 0
        
        for day in schedule_config:
            s = item.findtext('dutyTime8s') if day["is_holiday"] else None
            e = item.findtext('dutyTime8e') if day["is_holiday"] else None
            
            if not s: s = item.findtext(f'dutyTime{day["code"]}s')
            if not e: e = item.findtext(f'dutyTime{day["code"]}e')
            
            f_s = format_time(s)
            f_e = format_time(e)
            
            if f_s:
                # 종료시간이 없으면 ??:?? 대신 '정보확인' 텍스트와 구글링크 암시
                display_time = f"{f_s} ~ {f_e if f_e else '시간확인'}"
                times.append(display_time)
                open_count += 1
            else:
                times.append("휴무")

        if lat and lon:
            markers += f'L.marker([{lat}, {lon}]).addTo(map).bindPopup("<b>{name}</b><br><a href=\'{naver_url}\' target=\'_blank\'>네이버 확인</a> | <a href=\'{google_url}\' target=\'_blank\'>구글 확인</a>");\n        '
            groups[open_count].append({"name": name, "tel": tel, "addr": addr, "times": times, "n_url": naver_url, "g_url": google_url})

    # 마크다운 내용 구성 (바로가기 메뉴 및 표)
    labels = {i: f"{i}일 운영" for i in range(1, 8)}
    labels[7] = "7일 모두 운영(연중무휴)"
    
    menu_html = '<div style="background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 30px; text-align: center; border: 1px solid #eee;">'
    for i in range(7, 0, -1):
        if groups[i]:
            menu_html += f'<a href="#group-{i}" style="margin: 0 8px; text-decoration: none; color: #007bff; font-weight: bold; font-size: 14px;">[{labels[i]}]</a> '
    menu_html += '</div>'

# update_script.py 파일 내의 content 생성 부분을 이렇게 바꿔보세요
    content = f"""---
layout: post
title: "부천시 설 연휴(2/14~2/20) 약국 운영시간 안내"
author: june
date: {today}
categories: [ 약국정보 ]
featured: true
---

부천시 내 약국의 설 연휴 운영 정보를 운영 일수별로 정리했습니다. 
**마감 시간이 '시간확인'으로 표시된 곳은 아래 버튼을 눌러 정확한 시간을 확인해 보세요.**

### 📍 약국 위치 지도
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<div id="map" style="height: 400px; border-radius: 12px; margin-bottom: 20px; border: 1px solid #ddd;"></div>
<script>
    var map = L.map('map').setView([37.503, 126.766], 13);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png').addTo(map);
    {markers}
</script>

### ⚡ 빠른 이동
{menu_html}

"""
    for i in range(7, 0, -1):
        if not groups[i]: continue
        content += f'\n<h2 id="group-{i}" style="padding-top: 60px; margin-top: -30px; border-bottom: 2px solid #007bff; display: inline-block;">🏥 {labels[i]} ({len(groups[i])}곳)</h2>\n'
        for pharm in groups[i]:
            table_html = f"""
<table style="width:100%; border: 1px solid #ddd; border-collapse: collapse; margin-bottom: 25px; font-size: 12px; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
  <tr style="background: #f8f9fa;">
    <td style="width: 25%; padding: 10px; border: 1px solid #ddd; font-weight: bold; font-size: 14px;">
        {pharm['name']}
        <div style="margin-top: 5px;">
            <a href="{pharm['n_url']}" target="_blank" style="display: inline-block; padding: 2px 5px; background: #03cf5d; color: white; border-radius: 3px; text-decoration: none; font-size: 10px;">N 플레이스</a>
            <a href="{pharm['g_url']}" target="_blank" style="display: inline-block; padding: 2px 5px; background: #4285f4; color: white; border-radius: 3px; text-decoration: none; font-size: 10px;">G 지도</a>
        </div>
    </td>
    {"".join([f'<td style="width: 10.7%; padding: 5px; border: 1px solid #ddd; text-align: center; font-weight: bold; background: {"#e7f3ff" if d["is_holiday"] else "#fff"};">{d["label"]}</td>' for d in schedule_config])}
  </tr>
  <tr>
    <td style="padding: 10px; border: 1px solid #ddd; font-weight: bold; color: #e67e22;">📞 {pharm['tel']}</td>
    {"".join([f'<td rowspan="2" style="text-align: center; border: 1px solid #ddd; color: {"#d35400" if "시간확인" in t else "#2c3e50"};">{t}</td>' for t in pharm['times']])}
  </tr>
  <tr>
    <td style="padding: 10px; border: 1px solid #ddd; color: #7f8c8d;">📍 {pharm['addr']}</td>
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
