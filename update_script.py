import requests
import xml.etree.ElementTree as ET
import os

# API 키 설정 (깃허브 Secrets에 등록한 이름과 맞춰주세요)
NAT_KEY = os.environ.get('NAT_API_KEY')

def get_bucheon_seol_pharmacies():
    # 전국 약국 API 사용 (부천시 필터링 + 위도/경도 포함됨)
    url = "http://apis.data.go.kr/B552657/ErmctInsttInfoInqireService/getParmacyListInfoInqire"
    params = {
        'serviceKey': NAT_KEY,
        'Q0': '경기도',
        'Q1': '부천시',
        'numOfRows': '500' # 부천시 전체 약국을 넉넉히 가져옴
    }
    
    response = requests.get(url, params=params)
    root = ET.fromstring(response.content)
    
    seol_pharmacies = []
    
    for item in root.findall('.//item'):
        # 1. 설날(공휴일) 운영 여부 확인 (dutyTime8s: 공휴일 시작시간)
        seol_start = item.findtext('dutyTime8s')
        seol_end = item.findtext('dutyTime8e')
        
        # 2. 설날에 운영 계획이 있는 곳만 추출
        if seol_start and seol_end:
            name = item.findtext('dutyName')
            tel = item.findtext('dutyTel1')
            addr = item.findtext('dutyAddr')
            
            # 3. 위도(wgs84Lat) 및 경도(wgs84Lon) 좌표 추출
            lat = item.findtext('wgs84Lat')
            lon = item.findtext('wgs84Lon')
            
            seol_pharmacies.append({
                'name': name,
                'address': addr,
                'tel': tel,
                'time': f"{seol_start[:2]}:{seol_start[2:]}~{seol_end[:2]}:{seol_end[2:]}",
                'lat': lat,
                'lon': lon
            })
            
    return seol_pharmacies

# 데이터 확인용 출력
pharm_data = get_bucheon_seol_pharmacies()
print(f"부천시 설날 운영 약국 총 {len(pharm_data)}곳 발견!")

# 예시: 첫 번째 약국의 위도/경도 확인
if pharm_data:
    print(f"약국명: {pharm_data[0]['name']}")
    print(f"좌표: {pharm_data[0]['lat']}, {pharm_data[0]['lon']}")
