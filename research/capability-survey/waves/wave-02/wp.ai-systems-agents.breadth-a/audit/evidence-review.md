# 근거 감사: wp.ai-systems-agents.breadth-a

## 범위와 방법

- 대상: Candidate 8개와 evidence 레코드
- 감사 역할: 발견 조사자와 분리된 읽기 전용 독립 근거 감사자
- 확인: URL·제목·발행일·버전, `source_type`, `claim_scope`, `supports`,
  초안·공급자 자료·1차 연구의 일반화 제한
- 감사일: `2026-07-28`

## 최초 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 수정 묶음 | 8 |
| P2 개선 묶음 | 3 |

모든 핵심 URL은 접근 가능하거나 공식 경로로 확인되었습니다. 초안·현재 revision·
공급자 실무자료를 최종 표준이나 보편적 효과로 직접 오인한 P0는 없었습니다.

## P1 교정

| 대상 | 지적 | 반영 |
|---|---|---|
| AI 시스템 평가 | NIST AI 800-2 제목이 원문과 다름 | `Practices for Automated Benchmark Evaluations of Language Models`로 교정 |
| 시스템 컨텍스트 | Lost in the Middle의 Crossref 기탁일 사용 | 실제 발행일 `2024-02-23`으로 교정 |
| 상태·메모리·인계 | MemGPT v2 날짜 누락 | `2024-02-12`와 v2를 함께 기록 |
| 상태·메모리·인계 | A2A 1.0.0인데 `/latest/` URL 사용 | `/v1.0.0/specification/` 고정 URL로 교체 |
| RAG·ReAct·ARES | 학회 시작일을 논문 발행일로 기록 | 일 단위 근거가 없는 `published_at` 제거 |
| RAG | `publisher: NAACL` | `Association for Computational Linguistics`로 교정 |
| NIST AI 600-1 | Profile을 `official_spec`으로 분류 | `official_source`로 교정 |
| 여러 후보 | `supports: learning_outcome`이 claim보다 넓음 | 연결을 축소하고 claim 범위와 맞춤 |
| LLM 응용 계약 | 시간초과·fallback·외부 변경 D2의 직접 근거 부족 | D2를 잘못된 출력·모델 변경·검증 전 외부 변경으로 좁히고 MCP 검증·인간 확인 근거 추가 |
| 토폴로지 | 비교·한도·회복성 D2의 직접 근거 부족 | Set으로 라우팅하고 runner 구현을 제외했으며 NIST 비교평가 근거 추가 |

## 최신성·범위 판정

- NIST AI 800-2는 2026년 1월 Initial Public Draft입니다. 정확한 일자를 임의로
  기록하지 않았으며 최종 표준으로 부르지 않습니다.
- A2A 1.0.0은 재현 가능한 고정 URL로 사용하며 최신 패치라고 주장하지 않습니다.
- MCP 2025-11-25는 현재 revision이지만 final로 간주하지 않는다고
  `claim_scope`에 기록했습니다.
- OpenAPI 3.2.0, JSON Schema Draft 2020-12와 Anthropic 문서의 제목·날짜는
  공식 원문과 일치합니다.
- Anthropic 문서는 `practitioner_primary`로 분류하고 단일 공급자 실무자료라는
  일반화 한계를 유지했습니다.

## P2 추적

- NIST AI 800-2 최종본과 이후 agent 평가 지침 발행 시 후보를 재검토합니다.
- MCP·A2A의 새 revision·patch는 범용 학습성과가 아니라 Adapter·Resource 갱신
  트리거로 둡니다.
- RAG·메모리·trajectory 평가의 benchmark-현장 전이와 자동 grader 타당성은
  파일럿에서 별도 검증합니다.

## 결론

P1 반영 후 같은 독립 감사자가 현재 파일을 재확인했습니다. 최종 P0 0건,
P1 0건이며 taxonomy 0.3.0과 후보 8개의 참조도 유효합니다.
