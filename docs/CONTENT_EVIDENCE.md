# 콘텐츠 근거와 표현 범위

2026-10-17 작성. 공개할 설명의 근거와 한계를 관리하기 위한 문서입니다. 아래 경로는 비공개 원본 저장소의 근거 위치이며 이 저장소에 원본 코드를 복제하지 않습니다.

| 사이트의 주장 | 근거 | 표현 범위 |
| --- | --- | --- |
| 문서 유효성과 처방 대체 관계를 분리 | nhis-macro-core/core/models.py의 Prescription.is_valid·superseded_by_ps_id·superseded_date, 처방 supersession 서비스, 사용자 자소서 초안 | 설계와 구현 구조의 설명. 계약 초안에만 있는 세부 기능을 운영 완료로 확대하지 않음 |
| 과거 Claim의 처방 근거를 보존 | Claim.ps_id·ClaimDoc, docs/database/PS_VALIDITY_SUPERSESSION_AND_BILLING_EVIDENCE.md | 핵심 보존 원칙을 설명. 모든 과거 데이터의 운영 감사 완료를 주장하지 않음 |
| 월별 관리와 기간별 청구 분리 | PatientMonthlyBillingCycle·Claim·PatientMonthlyBillingCycleRecord·ClaimDoc, docs/BILLING_LOGIC.md | 1:N 관계와 근거·첨부의 책임 구분 |
| 청구 관련 실제 ERD 발췌 | nhis-macro-core/core/models.py의 patient_documents·prescriptions·patient_monthly_billing_cycles·patient_monthly_billing_cycle_records·claims·claim_docs | 현재 ORM의 실제 테이블·주요 컬럼·FK를 재구성. 공통 컬럼, 기존 호환 claim_id_1~3 및 일부 참조 대상을 생략 |
| OCR 접근 변경 | docs/plans/PLAN_VLM_OCR_SPIKE.md, docs/handoff/HANDOFF_GPT54_CLINICAL_OCR.md, 마스킹 서비스, 사용자 자소서 초안 | 관찰한 실패와 역할 변경을 정성 설명. 전 양식 정확도·일반 성능 보장 없음 |
| 관리자 콘솔 화면 | carebot-admin/web-ui/src의 실제 컴포넌트와 가상 API 응답을 사용한 로컬 렌더링 | 실제 UI·가상 데이터. 운영 환자 조회 없음. UI는 협업 결과물 |
| 역할·업체 확인과 제한 함수 | DB 역할·함수·권한 관련 migration과 소비자 API, 관련 계약 검사 | 명시한 경로의 접근 통제와 본인의 DB·백엔드 기여. 전체 시스템 보안 완성 주장 없음 |
| 61개 애플리케이션 테이블·9월분 청구 110건·2인 협업 | 사용자가 제공한 2026년 10월 이력서와 이전 검토 세션 | 해당 기준일·집계 범위 그대로 표시. 청구 업무 활용을 전체 제출 성공으로 바꾸지 않음 |
| 교육용 DB 15개 테이블·FK 20개·UNIQUE 3개·CHECK 9개 | 사용자의 기존 교육용 DB 설계 문서 6장 | 당시 스키마 생성·카탈로그 확인 기록. 실제 적재·거부 테스트·성능 검증은 미완료로 명시 |
| 학력·경력·SQLD | 사용자가 제공한 이력서 | 미졸업 상태와 잔여 학점, MVP·PostgreSQL 전환 시기를 구분 |

## 변경 시 확인

기능 상태와 수치가 바뀌면 해당 기준일·설명·화면을 함께 검토합니다. 과거 스냅샷과 현재 구조를 같은 기준으로 표시하지 않습니다. 생성한 도해는 전체 운영 스키마가 아니라 설명에 필요한 관계의 요약입니다.

운영 실습 저장소와 관련 실습 내용은 사용자의 요청에 따라 이 사이트 범위에서 제외했습니다.
