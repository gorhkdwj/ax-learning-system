# 근거 독립 감사: wp.independent-qa.stratified-a

## 범위

- 고위험·D3·논쟁 Candidate 30개와 evidence 99건 전수
- 일반 층화표본 Candidate 26개의 핵심 정의·학습성과
- Wave 5 승격 Unit 7개·Reference 7개·Set 1개의 근거 추적성

감사자는 파일을 수정하지 않았고 메인 세션만 교정을 반영했습니다.

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 4개 교정 범주 |
| P2 | 2개 메타데이터 범주 |

다음을 교정했습니다.

1. 2026-07-29 폐기된 Orange Book Annex를 현행 Orange Book 원문으로 바꾸고
   제목·버전·확인일·claim 범위를 Candidate·Unit·Reference에서 동기화했습니다.
2. Arazzo 1.1.0 정식 버전 URL의 누락된 `v`를 6곳에서 교정했습니다.
3. 이전된 RPA Program Playbook을 공식 Digital.gov 자산 URL로 6곳에서
   교정했습니다.
4. Wave 5 승격 산출물 15개에 원 Candidate의 `evidence`를
   `extensions.evidence_claims`로 exact deep-copy하여 claim 한계를 보존했습니다.

## 최종 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2개 비차단 메타데이터 범주 |

`source_version`이 비어 있는 15개 Candidate·25개 evidence와 Wave 5 projection의
일부 `source_type`·`source_version` 차이는 스키마상 허용되지만 재현성을 낮추는
메타데이터 부채입니다. 값은 추정해 채우지 않고 Wave 7 잔여위험으로 라우팅합니다.

## 결론

고위험 30개와 일반 26개의 핵심 claim에서 과장이나 정체성 오류는 발견하지
못했습니다. 승격 산출물 15개의 evidence claim은 Candidate와 exact하고 폐기 URL
발생은 0건입니다. 근거 기준으로 Wave 7 진행을 승인합니다.
