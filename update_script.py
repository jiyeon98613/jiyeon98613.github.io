import requests
import xml.etree.ElementTree as ET
import os
from datetime import datetime

# API 키 가져오기
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
    
    # API 응답 결과 확인을 위해 출력 (Actions 로그에서 볼 수 있음)
    print(f"API Response Status: {response.status_code}")
    
    root = ET.fromstring(response.content)
    items = root.findall('.//item')
    print(f"검색된 총 약국 수: {len(items)}") # 로그 확인용
    
    pharm_list = []
    for item in items:
        name = item.findtext('dutyName')
        tel = item.findtext('dutyTel1')
        addr = item.findtext('dutyAddr')
        lat = item.findtext('wgs84Lat')
        lon = item.findtext('wgs84Lon')
        
        # 임시로 '모든 약국'을 다 가져오게 수정 (테스트용)
        # 나중에 설날 데이터가 확실히 확인되면 조건을 다시 넣으세요.
        pharm_list.append({
            'name': name,
            'address': addr,
            'tel': tel,
            'lat': lat,
            'lon': lon
        })
    return pharm_list

def write_markdown(pharm_list):
    today = datetime.now().strftime('%Y-%m-%d')
    filename = f"_posts/{today}-bucheon-pharmacy-list.md"
    
    # 파일이 생성되는지 확인하기 위한 로그
    print(f"파일 생성 시도: {filename}")
    
    content = f"""---
layout: post
title: "부천시 약국 운영 현황 (테스트)"
date: {today}
---

## 부천시 약국 리스트
데이터 추출 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

| 약국명 | 주소 | 전화번호 | 좌표 |
| :--- | :--- | :--- | :--- |
"""
    if not pharm_list:
        content += "| 데이터가 없습니다 | - | - | - |\n"
    else:
        for p in pharm_list[:50]: # 너무 많으면 블로그가 무거워지니 일단 50개만
            content += f"| {p['name']} | {p['address']} | {p['tel']} | {p['lat']},{p['lon']} |\n"
        
    # _posts 폴더가 없을 경우를 대비
    if not os.path.exists('_posts'):
        os.makedirs('_posts')
        
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print("파일 쓰기 완료!")

# 실행
data = get_data()
write_markdown(data)
if pharm_data:
    print(f"약국명: {pharm_data[0]['name']}")
    print(f"좌표: {pharm_data[0]['lat']}, {pharm_data[0]['lon']}")
