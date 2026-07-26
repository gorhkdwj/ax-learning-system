# Trend Signal 연구 인입 거버넌스

## 1. 목적과 위치

Trend Signal은 하네스 엔지니어링, 루프 엔지니어링, LLM Wiki처럼 빠르게
등장하는 용어·개념·패턴을 정규 학습과정에 넣기 전에 조사하는 연구 인입
레코드입니다.

Trend Signal은 다섯 번째 학습 계층이 아닙니다. 사용자가 직접 이수하는
Learning Unit도 아닙니다. 검증을 통과한 결과만 다음 중 적합한 위치로
이동하거나 연결합니다.

- 전사 AX 역량지도 항목
- 기존 Unit의 Resource 또는 기술 Adapter
- 새 Learning Unit
- 비교 실험용 Probe Learning Set
- 정규 Learning Set
- 관찰·중복·기각·보관

따라서 신흥 용어를 발견했다는 이유만으로 `probe` Unit을 만들지 않습니다.
용어의 존재, 안정된 정의, 효과와 실무가치는 서로 다른 주장으로 관리합니다.

## 2. 정본과 파일

- 스키마: `schemas/trend-signal.schema.json`
- 작성 템플릿: `templates/metadata/trend-signal.template.json`
- 실제 레코드: `research/signals/<signal-id>/signal.json`
- 구조 및 교차 참조 검증: `python tools/validate_catalog.py`

Signal의 본문과 근거를 생성 HTML 안에 삽입하지 않습니다. 향후 HUB는 정본 JSON과
문서를 읽어 색인을 증분 갱신하며, 화면은 검색 결과와 원문 링크만 렌더링합니다.

## 3. 조사 단위

각 Signal은 최소한 다음을 분리하여 기록합니다.

- `definition`: 잠정 정의, 포함·제외 범위, 기반 원리와 실제 차이
- `claims`: 정의·효과·채택·한계·위험에 관한 검증 가능한 주장
- `evidence`: 출처 유형, URL, 발행일, 확인일과 그 출처로 확인한 범위
- `maturity`: 용어 성숙도, 정의 신뢰도, 효과 신뢰도, 구현 안정성과 변동성
- `relevance`: 업무 연결성, 선수역량, 필수 통제 또는 전략적 옵션가치
- `disambiguation`: 같은 이름으로 유통되는 서로 다른 해석
- `candidate_mapping`: 조사 후 이동할 목적지와 예상 학습성과
- `review`: 재검토 주기, 변화 감지 조건과 과장 방지 문구

주장과 근거는 `claim → evidence` 참조로 연결합니다. 발견용 커뮤니티 자료는
Signal 수집에는 사용할 수 있지만, 정의나 효과를 확정하는 유일한 근거로
사용하지 않습니다.

## 4. 상태와 전이

기본 흐름은 다음과 같습니다.

`captured → triaged → researching → substantiated → promoted`

필요에 따라 `watching`, `duplicate`, `rejected`, `archived`로 이동합니다.

| 상태 | 의미 |
|---|---|
| `captured` | 용어 또는 현상을 발견해 원출처와 발견 이유를 기록했습니다. |
| `triaged` | 조사 가치, 중복 가능성과 우선순위를 1차 판정했습니다. |
| `researching` | 정의·경계·효과 또는 실무가치에 핵심 미확인 사항이 있습니다. |
| `substantiated` | 핵심 정의와 업무 관련성을 1차·공식 근거로 방어할 수 있습니다. 효과 검증 완료를 뜻하지 않습니다. |
| `watching` | 당장 상세화하지 않고 변화 조건을 감시합니다. |
| `promoted` | 실제 Unit·Set·Resource의 정확한 ID와 버전으로 반영했습니다. |
| `duplicate` | 같은 대상을 가리키는 정규 Signal을 직접 참조합니다. |
| `rejected` | 현재 학습 범위로 발전시키지 않는 이유를 남겼습니다. |
| `archived` | 더 이상 활성 조사하지 않으며 이력만 보존합니다. |

`substantiated` 또는 `promoted`에는 다음 조건이 필요합니다.

- `relevance.status`가 `eligible`입니다.
- 검증 신뢰도가 `medium` 이상입니다.
- 핵심 identity 또는 definition claim이 지원됩니다.
- 미해결 핵심 claim이 없습니다.
- 표준·공식 문서·공식 소스·1차 연구·원 실무자 자료 중 하나 이상이 있습니다.
- 중의성이 `clear`로 해소되었습니다.

효과 주장이 아직 불확실하면 그 claim은 비핵심·미검증 상태로 유지하고,
정의만 `substantiated`할 수 있습니다. 이 경우 효과는 Probe에서 별도로 검증합니다.

## 5. 승격 게이트

아래 게이트는 새 기술을 막기 위한 승인 장벽이 아니라, 무엇을 알고 무엇을
모르는지 보존하기 위한 최소 검증 계약입니다.

| 게이트 | 질문 | 실패 시 기본 처리 |
|---|---|---|
| G0 정의 | 한 문장 정의와 포함·제외 범위를 출처로 방어할 수 있습니까? | `researching` |
| G1 비중복 | 기존 Unit·Signal의 재명명이나 부분집합이 아닙니까? | 병합 또는 관계 연결 |
| G2 근거 | 핵심 claim마다 범위가 명시된 1차·공식 근거가 있습니까? | 추가 조사 |
| G3 역량가치 | 업무 연결, 선수효과, 필수 통제 또는 옵션가치가 있습니까? | 관찰 또는 기각 |
| G4 비교 Probe | 기존 방식과 비교할 입력·지표·중단조건을 정의할 수 있습니까? | `observe` |
| G5 교육가능성 | 전이 가능한 학습성과와 검증 증거를 설계할 수 있습니까? | Resource만 연결 |
| G6 목적지 | Unit·Adapter·Resource·Probe Set·Set 중 정규 위치가 명확합니까? | `researching` |
| G7 운영안전 | 권한·보안·비용·관측·중단·복구 경계를 다룰 수 있습니까? | 운영 심화 보류 |
| G8 생명주기 | 소유자, 재검토일과 변화 감지 조건이 있습니까? | 승격 보류 |

승격은 Signal을 삭제하는 작업이 아닙니다. Signal의 `promotion.targets`에 실제
카탈로그 대상의 종류, ID, 정확한 버전과 수행한 작업을 기록하고 조사 이력을
남깁니다.

## 6. 명칭과 중복 관리

- `canonical_name`은 현재 조사 대상을 가장 좁고 안정적으로 표현합니다.
- 별칭은 동의어, 번역, 약어, 철자, 과거명, 관련어와 중의어를 구분합니다.
- 대소문자, Unicode 호환문자, 하이픈·밑줄 차이는 정규화하여 비교합니다.
- 이름이 같다고 자동 병합하지 않습니다. 활성 Signal 간 충돌은 경고 후 사람이
  정의와 범위를 비교합니다.
- 계층 관계인 `broader_than`, `narrower_than`, `split_into`는 순환할 수 없습니다.
- 중복 레코드는 또 다른 중복 레코드가 아니라 최종 정규 Signal을 직접 참조합니다.

## 7. 최초 등록 사례

### Agent harness

OpenAI의 [Harness engineering](https://openai.com/index/harness-engineering/),
Anthropic의 [Effective harnesses for long-running agents](https://www.anthropic.com/engineering/harness-design-long-running-apps),
관련 [AI Harness Engineering 연구](https://arxiv.org/abs/2605.13357)를 근거로
정의는 `substantiated`로 두었습니다. 보편적 업무효과는 확정하지 않고,
동일 과제를 최소·구조화 하네스로 비교하는 `probe_set` 후보로 두었습니다.

### Agent execution control loop / Loop Engineering

에이전트 실행 루프 자체는 OpenAI Agents SDK의
[Running agents](https://openai.github.io/openai-agents-python/running_agents/)와
Anthropic의 [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents)
등에서 확인할 수 있습니다. 그러나 “Loop Engineering”을 독립된 공학 분야로 보는
경계는 [용어 제안 글](https://loopengineering.run/blog/what-is-loop-engineering)과
[IBM 설명](https://www.ibm.com/think/topics/loop-engineering) 사이에서도 더
검토가 필요하므로 `researching`·`observe`로 유지합니다.

### Karpathy-style LLM Wiki

Karpathy의 [원 제안](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f),
[LLM Wiki 연구](https://arxiv.org/abs/2605.25480),
[공개 구현](https://github.com/Astro-Han/karpathy-llm-wiki)을 근거로 패턴 정의는
`substantiated`로 두었습니다. 정확도·최신성·인간 검토시간·유지비용 개선은
미검증 효과 claim으로 남기고, 기존 파일 검색 또는 RAG 기준선과 비교하는
`probe_set` 후보로 두었습니다.

## 8. 과장 방지

다음 표현은 비교 증거 없이 학습자료에 사용하지 않습니다.

- 생산성이 항상 몇 배 향상된다는 보편적 수치
- 프롬프트 또는 컨텍스트 엔지니어링을 대체한다는 주장
- 반복만 하면 정답에 도달한다는 주장
- RAG가 사라졌거나 항상 대체된다는 주장
- 자동 유지 지식이 원천 확인 없이 진실과 최신성을 보장한다는 주장
- 에이전트 자기평가가 인간 승인과 외부 상태 검증을 대체한다는 주장

## 9. 운영 절차

1. 원문 또는 최초 출처와 함께 Signal을 `captured`로 만듭니다.
2. 기존 Signal과 Unit을 검색하여 명칭·범위 중복을 판정합니다.
3. 중요한 문장을 claim으로 쪼개고 각 evidence의 지지·반박·맥락 역할을 연결합니다.
4. 정의 신뢰도와 효과 신뢰도를 별도로 평가합니다.
5. G0–G8과 비즈니스 임팩트 가설을 검토하여 목적지를 정합니다.
6. 구조검증과 회귀검사를 통과시킵니다.
7. 승격 전에는 Probe의 기준선·성공지표·중단조건·안전경계를 먼저 확정합니다.
8. 변화 감지 조건 또는 `review_due_at` 도래 시 다시 조사합니다.
