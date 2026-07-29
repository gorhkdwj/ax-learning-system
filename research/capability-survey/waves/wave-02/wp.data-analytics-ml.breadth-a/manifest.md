# Work Package Manifest: wp.data-analytics-ml.breadth-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-02` |
| 상태 | `approved` |
| 범위 승인일 | `2026-07-28` |
| 범위 승인 근거 | 사용자가 Codex의 전문 판단에 따른 다음 순차 Wave 2 패키지 진행을 승인함 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.5.0` (`provisional`) |
| 최대 후보 | `10` |
| 이번 판정 | 신규 Candidate 9개 + 기존 Candidate 재사용 1개 |
| 동시 작업 패키지 | `1` |
| 표시명 규칙 | 과목·후보명은 한국어 우선, node ID·영문 병기 허용 |

## 조사 계약

### 포함

- 데이터 원천·수집계약과 입력 fixture
- 재현 가능한 데이터 변환·파이프라인
- 분석 모델·지표 의미계약
- 탐색적·통계적 분석과 불확실성 해석
- 사용목적별 데이터 품질 검증·관측
- 데이터 카탈로그·계보·책임 메타데이터
- 통제 실험·영향평가
- 예측 ML 문제정의·비ML 기준선
- 예측 ML 모델 검증·의사결정 임계값
- ML 생명주기 재현성·모니터링

### 제외

- 애플리케이션 관계형 스키마·migration과 일반 HTTP API 계약
- SaaS·MCP 커넥터, 업무자동화와 범용 orchestration
- LLM·agent trajectory·grader·stochastic regression 평가
- 플랫폼 배포·SLO·incident·클러스터·서빙 인프라 운영
- 개인정보·IAM·법적 보존기간과 전문 보안 통제 결정
- 특정 데이터·BI·ML 제품의 사용법
- 고급 알고리즘 연구와 D3 이상 전문 통계·인과추론
- 상세 교재·실습·HUB 구축과 정규 Unit·Set 승격

## 중복 방지 판정

- `candidate.ax-strategy-value.pilot-impact-evaluation@1.0.0`은 새 후보로
  복제하지 않고 이 패키지의 열 번째 조사 결과로 재사용합니다.
- `candidate.ax-strategy-value.measurement-contract@1.0.0`은 무엇을
  성공·가드레일로 측정할지 소유하며, 새 분석 모델 후보는 선택된 지표를
  일관되게 계산하는 grain·dimension·measure 의미를 소유합니다.
- 애플리케이션 DB는
  `unit.software.relational-data-model-schema-evolution@1.0.0`, 일반 API는
  `unit.software.api-contract-compatibility@1.0.0`이 소유합니다.
- LLM·agent 평가는 `unit.ai.system-evaluation-regression-design@1.0.0`이,
  새 ML 검증 후보는 지도학습 모델의 분할·누수·calibration·threshold를
  소유합니다.
- 제품별 도구 사용법은 정규 역량이 아니라 후속 Resource·Adapter로 라우팅합니다.

## 실행 구조

1. 읽기 전용 발견 조사자가 기존 Candidate·Unit·Set·Signal과 공식·1차 근거를
   대조해 후보를 제안했습니다.
2. Codex 메인 세션이 중복·소유권 경계와 D0·D2 평가 가능성을 판정해 신규 후보
   9개를 작성하고 기존 후보 1개를 재사용했습니다.
3. 발견과 분리된 근거·taxonomy·실용성 감사자가 후보 10개를 독립 검토합니다.
4. Codex 메인 세션이 P0·P1을 반영하고 재감사·Checkpoint·전체 검증을 완료합니다.

## 최종 판정

- 신규 Candidate 9개는 모두 `accepted`입니다.
- 기존 `candidate.ax-strategy-value.pilot-impact-evaluation@1.0.0`은 최초 ID와
  내용을 변경하지 않고 열 번째 조사 결과로 재사용합니다.
- 독립 근거·taxonomy·실용성 재감사 결과는 모두 P0 0건, P1 0건입니다.
- 비차단 P2는 정규 Resource 승격과 상세 평가 fixture 설계 때 추적합니다.
- 이번 승인에는 정규 Unit 승격, 상세 교재·실습·파일럿이 포함되지 않습니다.

## 임시 Gate

- 신규 Candidate는 9개이고 기존 재사용 1개를 합쳐 상한 10개를 넘지 않습니다.
- 모든 신규 후보에 D0와 D2의 관찰 가능한 행동·산출물이 있습니다.
- 모든 신규 후보에 독립적인 공식·표준·1차 근거가 2개 이상 있습니다.
- Unit·Set·Resource·Adapter와 인접 렌즈 경계를 명시합니다.
- 기존 최초 발견 ID와 정규 ID를 변경하거나 복제하지 않습니다.
- 감사 P0 0건과 P1 반영·재확인 후에만 `accepted`로 전환합니다.
- 카탈로그·공개 경계·스키마·단위 테스트와 `git diff --check`를 통과해야 합니다.

## 자동 중단조건

- 필수 근거가 없거나 제목·출처의 주장 범위가 실제 문서보다 넓습니다.
- 새 후보가 기존 후보·Unit과 같은 D2 산출물·Gate를 가집니다.
- 특정 제품 사용법 없이 독립적인 D2 결과를 평가할 수 없습니다.
- 개인정보·보안·플랫폼 운영의 전문 통제를 이 패키지가 임의로 확정해야 합니다.
- 기존 정규 ID 변경, schema 변경 또는 대분류 신설이 필요합니다.
- 공개 경계·검증·감사가 실패합니다.
