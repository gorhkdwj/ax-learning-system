# 근거 감사: wp.ax-strategy-value.pilot

## 범위와 방법

- 대상: Candidate 8개, evidence 27건, 고유 URL 21개 전수
- 검사: URL 접근성, 제목·발행주체·날짜·버전, `claim_scope`와 원문 일치,
  `supports` 과대표기, 확인된 사실과 효과 가설 분리
- 수행: 읽기 전용 `ax-evidence-auditor`
- 날짜: 2026-07-26

## 최초 판정

최초 16개 evidence 감사에서는 pass 2개, revise 6개, block 0개
Candidate 판정이 나왔습니다. 주된 문제는 다음과 같았습니다.

- 페이지 갱신일을 원문 발행일로 기록
- 원문이 직접 지지하지 않는 `learning_outcome`·`business_hypothesis`
- 공공부문 지침을 민간 AX 효과로 일반화할 위험
- 전체 후보 행동에 비해 근거 범위가 좁음
- 접근되지 않는 ILO 원 URL과 GSA PDF

## 반영

- ILO는 공식 연구저장소 URL로, GSA RPA Playbook은 공식 Digital.gov
  v1.1 PDF로 교체했습니다.
- Green Book·Magenta Book의 갱신일을 `source_version`으로 이동했습니다.
- NIST, GOV.UK와 Microsoft 자료의 `supports`·`claim_scope`를 원문 범위로
  축소했습니다.
- 현행 분석에는 GOV.UK 경험조사 방법을, 과업 배분에는 NASA Human
  Integration Design Handbook을, 측정계약에는 Canada 성과측정 지침을
  추가했습니다.
- 수작업 현행 분석의 학습성과를 실행기록·경험자료에 추적되는 지도와
  관측 기준선 수준으로 축소했습니다.
- 확인되지 않은 민간 전이와 효과 크기는 `business_hypotheses` 또는
  `known_unknowns`로 유지했습니다.

## 최종 재감사

| 검사 | 결과 |
|---|---|
| 남은 P0 | 0 |
| 후보 전수 | 8/8 |
| evidence 전수 | 27/27 |
| 고유 URL | 21 |
| 미확인 원문 | 0 |
| 근거 없는 효과 수치 | 발견되지 않음 |
| accepted/high-confidence 승격 | 없음 |

직접 PDF 열기 제한은 2건이었습니다. RPA Playbook은 동일 공식 Digital.gov
페이지와 PDF로, NASA HIDH는 공식 색인·현재 PDF·검색 가능한 원문으로
교차 확인했습니다.

## 잔여 제한

- 공식 문서의 공공부문 비중이 높으므로 민간·비영리 전이는 아직 가설입니다.
- 실제 Unit 수용 전에는 비공공 맥락의 전이 검증 또는 표준·1차 연구 보강이
  필요합니다.
- 업무별 성과 크기와 정량 임계값은 이 조사에서 확정하지 않았습니다.

파일은 감사자가 수정하지 않았으며 교정은 Codex 메인 세션이 수행했습니다.

## 신규 전략 후보 독립 감사

- 대상: 신규 Candidate 2개, evidence 8건, URL 8개 전수
- 수행: 읽기 전용 `orca-claude-evidence-auditor`
- 날짜: 2026-07-27
- 원문 확인: HTML 7건과 OECD 공개 PDF 1건으로 8/8 확인
- 최초 판정: 두 Candidate 모두 `revise`, P0 2건

### 발견한 P0

1. 포트폴리오 후보의 Orange Book에 존재하지 않는 `2026 edition`을
   기록했습니다. 실제 Orange Book 본문은 May 2023판이며 2026-06-03 페이지
   갱신은 다른 첨부파일에 적용된 변경이었습니다.
2. 로드맵 후보의 NDA group strategy 원문에는 AI·artificial intelligence·
   machine learning이 없는데 AI 실행 연결 사례와 D2 학습성과를 지지한다고
   과대 표기했습니다.

### Codex 반영과 재검토

- Orange Book 본문 evidence를 포트폴리오 선택·우선순위·재균형을 직접 다루는
  May 2023 `Portfolio Risk Management Guidance — Orange Book Annex`로
  교체했습니다.
- Green Book은 단일 제안 내부의 대안평가만 지지하도록 `claim_scope`를
  축소하고 `learning_outcome` 지원 표기를 제거했습니다.
- APM과 AI Playbook에 확인 가능한 판본 문맥을 추가했습니다.
- NDA evidence는 삭제했습니다.
- 접근되지 않던 OECD HTML은 공개 PDF 정본으로 교체하고 Chapter 4의
  기반 역량·범정부 실행 범위로 `claim_scope`를 보강했습니다.
- ISO/IEC 42001은 공식 카탈로그 URL·정식 명칭·공개 초록만 열람했다는
  검증 한계를, NIST AI RMF는 개정 진행 중이라는 재확인 트리거를 기록했습니다.

| 검사 | 최종 결과 |
|---|---|
| 신규 후보 남은 P0 | 0 |
| 신규 후보 남은 P1 | 0 |
| 신규 후보 원문 확인 | 2/2 |
| 전체 Candidate | 10 |
| 전체 evidence | 34 |
| 전체 고유 URL | 25 |
| 근거 없는 효과 수치 | 발견되지 않음 |

공공부문 근거의 민간·비영리 전이, ISO 유료 규범 본문 미열람과 향후 NIST
개정판은 `known_unknowns`와 `source_version`에 남겼습니다. 독립 감사자는
파일을 수정하지 않았고 교정과 최종 판정은 Codex 메인 세션이 수행했습니다.
