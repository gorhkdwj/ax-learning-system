# Phase 2 AX 최종 역량지도

## 1. 지도 상태

이 문서는 조사 결과의 탐색 projection입니다. 정규 분류 정본은
`taxonomy/taxonomy.json`, 학습 메타데이터 정본은 `catalog/`와 `sets/`, 발견·
판정 provenance 정본은 각 Candidate입니다.

| 층 | 현재 결과 | 의미 |
|---|---:|---|
| Canonical domain | 10 | 전사 AX 역량의 정규 대분류 |
| Canonical subdomain | 97 | 근거와 승인·승격 경계를 가진 정규 중분류 |
| Provisional subdomain | 3 | 근거 보강·경계 검토가 필요한 보류 분류 |
| Active role view | 8 | Wave 4 역할 관점의 기계 판독형 탐색 projection |
| Planned 세부 role view | 3 | 기존 ID를 보존한 엔지니어링 세부 보기 후보 |
| Candidate | 96 | 조사·감사 provenance이며 현재 학습 배정이 아님 |

## 2. Canonical domain 지도

| Domain | 소유하는 핵심 판정 |
|---|---|
| `ax-strategy-value` | 기회·가치, 현행·미래 업무, 과업배분, 해법·포트폴리오·측정·로드맵 |
| `ai-literacy-trust` | AI 기본 한계, 과업 프레이밍, 출력 검토, 신뢰·책임·영향·투명성 |
| `ai-systems-agents` | LLM 응용, context·RAG·구조화 출력·도구·상태·agent workflow·평가 |
| `software-product-engineering` | 요구·설계·변경·API·DB·UI·테스트·디버깅·빌드 |
| `data-analytics-ml` | 데이터 계약·변환·품질·계보·분석·영향평가·예측 ML 수명주기 |
| `integration-automation` | API·event·workflow·부작용·규칙·결과판정·UI 자동화·protocol |
| `human-ai-experience` | 기대형성·설명·통제·승인·복구·접근성·경험평가 |
| `platform-quality-operations` | 릴리스·환경·telemetry·SLO·사고·복구·용량·비용·복원력·준비도 |
| `security-legal-governance` | 위험·권한·비밀·공급망·privacy·사고·감사·권리·AI 보안·거버넌스 |
| `organization-adoption` | 변화·운영모델·역량전환·학습전이·포용·지원·성과·확산·조달·수명주기 |

## 3. 역할별 탐색 보기

| 코드 | Active view | 결합 domain 수 |
|---|---|---:|
| EX | `view.role.executive-strategy-portfolio` | 6 |
| WK | `view.role.work-process-service` | 10 |
| PX | `view.role.product-ux-customer-support` | 10 |
| EN | `view.role.software-ai-integration-engineering` | 9 |
| DA | `view.role.data-analytics-ml` | 9 |
| OP | `view.role.platform-quality-operations` | 10 |
| RK | `view.role.security-legal-audit-procurement` | 8 |
| OR | `view.role.organization-people-learning-change` | 2 |

Role view는 중복 Unit을 만들지 않고 canonical domain을 조합합니다. `active`는
탐색 가능하다는 뜻이며 개인별 필수과정, 직무기술서, 역할별 학습순서나 실제
조직 적합성을 뜻하지 않습니다. `node_refs`는 Wave 4 역할표의 `S`(직접 조사)
domain 집합과 정확히 일치합니다. `G`는 역할과 무관하다는 뜻이 아니라 인접
domain이 전문 소유권을 갖는 라우팅이며 관계 메타데이터와 공백 표에서 추적합니다.

## 4. 관계 흐름

```text
AI 리터러시·근거 검토
        ↓
AX 기회·현행 업무·과업·해법·측정 설계
        ↓
AI 시스템 ─ 소프트웨어 ─ 데이터 ─ 통합 ─ Human-AI 경험
        ↓                         ↓
플랫폼 운영 ─────────────── 보안·법무·거버넌스
        ↓                         ↓
조직 도입·확산·학습전이 ─ 측정·영향평가 재검토
```

이는 탐색 흐름이지 모든 Unit의 단일 선행순서가 아닙니다. 실행 가능한 exact DAG는
각 Unit `relations`와 Set `steps.depends_on`이 정본이며 자동검증 대상입니다.

## 5. 상세 교재와 metadata-first 구분

| 분류 | Candidate | 처리 |
|---|---:|---|
| `unit_candidate` | 80 | Phase 3 우선순위 평가 대상; 현재는 cataloged 메타데이터 |
| `set_candidate` | 8 | Phase 3 조합·전이 평가 대상; 현재는 cataloged 메타데이터 |
| `resource_only` | 4 | 소유 Unit의 보조 근거·경계 Resource로 유지 |
| `technology_adapter` | 1 | stable core를 대체하지 않는 metadata-first Adapter로 유지 |
| `merge_existing` | 1 | 기존 근거 검증 Unit에 병합하고 새 ID를 만들지 않음 |
| `defer` | 2 | 근거·경계 재개 조건 충족 전 승격하지 않음 |
| **합계** | **96** | |

따라서 상세 교재 후보는 Unit 80개와 Set 8개이나, 모두를 즉시 제작한다는 뜻은
아닙니다. Phase 3에서 역할·가치·선행관계·안전·유지비를 평가한 뒤 소수부터
활성화합니다. 정규 catalog에는 Adapter를 포함한 Unit 81개, Resource 85개,
Set 8개가 있으며 검증기는 예제 Unit 2개·Resource 4개·Set 1개를 포함해 각각
83·89·9개를 검사합니다.

## 6. 상태 구분

- `Candidate accepted`: 정의·경계·근거와 목적지 판정이 감사를 통과했습니다.
- `cataloged`: 정규 메타데이터로 등록되었습니다.
- role view `active`: 정규 node를 역할 관점에서 탐색할 수 있습니다.
- 상세 학습 `active`: fixture·runner·교재와 평가 Gate가 구현된 별도 상태입니다.
- `validated`: 학습효과·업무효과와 실제 맥락 전이가 검증된 상태입니다.

현재 Phase 2가 확정하는 것은 앞의 세 층까지입니다. 상세 학습 활성화와 효과
검증은 Phase 3 이후의 별도 Gate입니다.

## 7. 보류·공백·불확실성

| 항목 | 현재 상태 | 재개 조건 |
|---|---|---|
| 개인화·장기 memory 사용자 통제 | Candidate·node deferred/provisional | 장기 memory lifecycle 직접 근거와 삭제·철회·전이 평가계약 |
| 편익 실현·가치 추적 | needs_review·provisional | 일반 편익관리와 AX 전용 Resource 경계 및 완전원가 검증 |
| `operational-value` node | provisional | 직접 승격 근거 또는 명시적 canonical 소유권 확보 |
| 내부 플랫폼 제품 운영 | Candidate 미생성 | 실제 내부 사용자 조사와 operating model 근거 |
| 인증·session·federation·탐지 engineering | 후속 조사 | 고위험 파일럿 또는 별도 보안 engineering 패키지 승인 |
| vendor assurance·비개인 민감정보 | 후속 조사 | 실제 조달·보안 사용례와 qualified owner 확보 |
| 조직문화·보상·채용·노사·전문 조달 | 전문 범위 보류 | 실제 적용 필요와 전문 검토자 확보 |
| 근거 버전 메타데이터 | 비차단 P2 | 15 Candidate·25 evidence의 원문 버전을 추정 없이 확인 |
| Wave 5 source projection 차이 | 비차단 P2 | source type 5건·version 7건의 정규화 정책 확정 |
| 세부 엔지니어링 role view 3개 | planned | 실제 사용례·영향분석과 사용자 승인 |

## 8. 완료 경계

Candidate 판정은 accepted 93·merged 1·deferred 1·needs_review 1로 96개와
일치합니다. Wave 4에서 라우팅 없는 신규 고우선 공백은 0개였고 Wave 6의
독립 QA는 P0·P1 0건입니다. 이 결과는 Phase 2 지도 조립의 완료 근거이지만,
상기 보류항목 삭제나 실제 학습·업무효과 확인을 뜻하지 않습니다.
