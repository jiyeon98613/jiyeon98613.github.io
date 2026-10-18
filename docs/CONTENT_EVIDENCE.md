# 콘텐츠 근거와 표현 범위

2026-10-17 작성. 공개할 설명의 근거와 한계를 관리하기 위한 문서입니다. 아래 경로는 비공개 원본 저장소의 근거 위치이며 이 저장소에 원본 코드를 복제하지 않습니다.

| 사이트의 주장 | 근거 | 표현 범위 |
| --- | --- | --- |
| 문서 유효성과 처방 대체 관계를 분리 | nhis-macro-core/core/models.py의 Prescription.is_valid·superseded_by_ps_id·superseded_date, 처방 supersession 서비스, 사용자 자소서 초안 | 설계와 구현 구조의 설명. 계약 초안에만 있는 세부 기능을 운영 완료로 확대하지 않음 |
| 과거 Claim의 처방 근거를 보존 | Claim.ps_id·ClaimDoc, docs/database/PS_VALIDITY_SUPERSESSION_AND_BILLING_EVIDENCE.md | 핵심 보존 원칙을 설명. 모든 과거 데이터의 운영 감사 완료를 주장하지 않음 |
| 월별 관리와 기간별 청구 분리 | PatientMonthlyBillingCycle·Claim·PatientMonthlyBillingCycleRecord·ClaimDoc, docs/BILLING_LOGIC.md | 1:N 관계와 근거·첨부의 책임 구분 |
| 청구 관련 실제 ERD 발췌 | nhis-macro-core/core/models.py의 patient_documents·prescriptions·patient_monthly_billing_cycles·patient_monthly_billing_cycle_records·claims·claim_docs | 현재 ORM의 실제 테이블·주요 컬럼·FK를 재구성. 공통 컬럼, 기존 호환 claim_id_1~3 및 일부 참조 대상을 생략 |
| 동일 기간 중복 처방 정리와 후속 등록 경로 개선 | 당시 관리자 CLI 검토 대화와 운영 검증 기록, ps_history_review 서비스, 처방 입력 경로 통합 기록 | 무효 처리 절차와 후속 오류 해소 확인. 개별 중복 행의 출처를 각각 Excel·OCR로 단정하거나 일괄 삭제 건수를 제시하지 않음 |
| GPT API 사용에 대한 고객사 검토·동의와 관리자 마스킹 검토 | 사용자가 확인한 고객사 검토·동의, 기존 마스킹·전송 승인·결과 검토 절차 | 외부 API 사용 동의와 문서별 관리자 검토를 구분하고, 식별정보를 제외한 이미지 영역의 전송과 추출값 반환을 설명 |
| OCR 접근 변경 | docs/plans/PLAN_VLM_OCR_SPIKE.md, docs/handoff/HANDOFF_GPT54_CLINICAL_OCR.md, 마스킹 서비스, 사용자 자소서 초안 | 관찰한 실패와 역할 변경을 정성 설명. 전 양식 정확도·일반 성능 보장 없음 |
| 관리자 콘솔 화면 | carebot-admin/web-ui/src의 실제 컴포넌트와 가상 API 응답을 사용한 로컬 렌더링 | 실제 UI·가상 데이터. 운영 환자 조회 없음. UI는 협업 결과물 |
| 역할·업체 확인과 제한 함수 | DB 역할·함수·권한 관련 migration과 소비자 API, 관련 계약 검사 | 명시한 경로의 접근 통제와 본인의 DB·백엔드 기여. 전체 시스템 보안 완성 주장 없음 |
| 61개 애플리케이션 테이블·9월분 청구 110건·2인 협업 | 사용자가 제공한 2026년 10월 이력서와 이전 검토 세션 | 해당 기준일·집계 범위 그대로 표시. 청구 업무 활용을 전체 제출 성공으로 바꾸지 않음 |
| 교육용 DB 15개 테이블·FK 20개·UNIQUE 3개·CHECK 9개 | 사용자의 기존 교육용 DB 설계 문서 6장 | 당시 스키마 생성·카탈로그 확인 기록. 실제 적재·거부 테스트·성능 검증은 미완료로 명시 |
| 학력·경력·SQLD | 사용자가 제공한 최신 이력서와 학력 확인 내용 | SCC 재학·Honors College·수학부서 장학금·GPA·President’s List, USC 편입과 잔여 1과목·2학점, 고객사명·고용 형태, MVP·PostgreSQL 전환 시기를 구분 |

## 변경 시 확인

기능 상태와 수치가 바뀌면 해당 기준일·설명·화면을 함께 검토합니다. 과거 스냅샷과 현재 구조를 같은 기준으로 표시하지 않습니다. 생성한 도해는 전체 운영 스키마가 아니라 설명에 필요한 관계의 요약입니다.

## 2026-10-18 청구 시스템의 판단·검증 근거 보강

이 변경은 기존 비공개 기록의 공개용 요약과 가상 데이터로 재현한 예시입니다. 새로운 운영 DB 검사·OCR 측정·외부 API 호출을 수행한 결과로 표시하지 않습니다.

| 추가한 내용 | 근거와 시점 | 공개 표현의 범위 |
| --- | --- | --- |
| 처방전 수정 전후 표 | PS 유효성 계약, 2026-09-05 PS 이력 검토 기록, Prescription.is_valid·superseded_by_ps_id·Claim.ps_id | PS-A/PS-B는 가상 식별자. 과거 운영 행을 그대로 재현했다고 주장하지 않음. 단일 후보 판정과 청구 전 검증을 구분 |
| 부분 수정 저장과 잔존 오류 | nhis-macro #9 코멘트 1848, PR #67, migration a4d9c72e1f60, ps_history_review.py | APPLIED_WITH_BLOCKERS 반환과 승인형 부분 저장의 구현 기록. 저장을 청구 가능 완료로 세지 않음 |
| 월별 근거 연결 구조 선택 | docs/plans/PLAN_ASSET_MODEL.md §8.5, 2026-06-15 결정 | 초기 SQLite 모델의 실제 단일 FK와 검토 초안인 doc_kind+ref_id를 구분. 현재 PostgreSQL 연결 구조와 동일 시점으로 설명하지 않음 |
| 3건을 넘는 기간별 Claim | nhis-macro #33 코멘트 1587·1662, Claim.billing_cycle_id·segment_index, active cycle/segment unique index | 월별 관리와 1:N 청구·호환 필드의 역할. 모든 복합 NHIS 실화면 케이스의 검증 완료로 확대하지 않음 |
| 원천 변경 후 발행본 보존 예시 | docs/database/PATIENT_BILLING_STATEMENT_API.md, nhis-macro #89 코멘트 2324·2358, PatientBillingStatement.source_hash·payload_snapshot·revision_no | 17,800/20,800원과 H₁/H₂는 고정 가상 예시. 과거 실제 PostgreSQL의 stale 발행 거부·재시도·스냅샷 보존 검증과 웹의 설명용 동작을 구분 |
| 로컬 VLM 60.3% → 88.9% | docs/plans/PLAN_VLM_OCR_SPIKE.md §6·7, 2026-06-23~24 | 정답표를 준비한 7장·핵심 9필드의 과거 집계값. 임상 체크박스나 GPT·운영 전체·양식별 정확도 수치로 사용하지 않음. 원본 정답표·개별 결과는 공개하지 않음 |
| 체크박스 확대·잉크 비율 접근의 한계 | PLAN_VLM_OCR_SPIKE.md의 체크박스 크롭·CV 보류 기록 | 관찰한 한계와 접근 전환을 설명. 새로운 비교 실험이나 전체 방법의 보편적 성능 판단으로 표현하지 않음 |
| 마스킹 전후 이미지와 전송 차단 예시 | HANDOFF_GPT54_CLINICAL_OCR.md의 2026-06-24 검토 기록, pii_masker.mask_identity_bands, test_pii_masker.test_mask_identity_bands_fail_closed | 공개 SVG는 가상 문서이며 실제 원본·실행 결과가 아님. 기준 문구 누락 시 마스킹 파일 미생성·전송 차단과 관리자 확인·승인을 구분. 웹 예시에서 API 호출 없음 |

당시 실험 문서는 목적 결정·정답표 작성·Windows 실행·결과 확인을 본인의 역할로, 스크립트 구현을 Cursor의 역할로 명시합니다. 구현을 모두 수작업으로 독립 작성했다는 표현을 추가하지 않습니다.

## PostgreSQL 운영 실습

공개 근거는 [postgres-ops-lab](https://github.com/jiyeon98613/postgres-ops-lab)의 실습별 README와 결과 파일입니다. 검증일은 2026-10-17이며, 아래 수치는 해당 실행 결과에 한정합니다.

| 사이트의 주장 | 근거 | 표현 범위 |
| --- | --- | --- |
| 운영 PostgreSQL 일일 백업 구축 | 기존 정기 백업 설정 확인과 사용자 구축 이력 확인 | 일일 논리 백업 설정. 운영 PITR·외부 백업 보관·자동 복구 완료로 확대하지 않음 |
| 실제 백업의 복원·성능 검증 장소 | 기존 실행 환경 확인과 최신 이력서의 실습 범위 | 고객사 서버 내 별도 PostgreSQL 인스턴스와 비공개 작업 디렉터리. 로컬 Kubernetes는 별도 확인용 데이터 사용 |
| 62개 테이블·32,117행 복구와 삭제 후 재검증 | results/restore.json, results/drop-restore.json | 애플리케이션 테이블 61개와 버전 관리 1개. 계정 소유권·ACL·외부 문서 복구 제외 |
| 기존 인덱스 유무에 따른 실행 시간 | results/tuning.json, results/tuning-masked.json, results/source-context.json | 원본 복원본의 4라운드 평균 실행 시간 중앙값. 운영 지연 개선·느린 쿼리 순위로 표현하지 않음 |
| 로그인·권한 검사 17개 | results/roles.json | 격리된 실습 계정의 허용·거부 검사. 운영 권한 전체 감사로 확대하지 않음 |
| replica 중단 후 1,000행 반영·목표 시점 복구 | results/physical.json | 동일 호스트의 별도 인스턴스. 운영 복제·PITR 구축 완료를 주장하지 않음 |
| primary Pod 삭제 후 4초에 쓰기 확인·replica 재합류 | results/cloudnativepg/failover.json, results/cloudnativepg/post-recovery.json | 단일 kind 노드의 관측값. 운영 RTO·모든 장애의 무손실 보장 제외 |
| 스키마 이름 충돌과 PITR 조회 잠금 수정 | labs/02-query-tuning/README.md, labs/04-replication-pitr/README.md와 관련 검증 코드 | 실제 기록된 실습 중 오류. 운영 장애 대응 사례로 바꾸지 않음 |

사이트에는 실행 절차와 검토한 수치만 소개합니다. 원본 백업·행 값·SQL 매개변수·접속 정보는 복제하지 않습니다.
