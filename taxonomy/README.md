# AX 역량 분류 레지스트리

`taxonomy.json`은 조사 렌즈, 잠정·정규 대분류와 중분류, 외부 교차검증
참고체계와 역할·업무 탐색 보기를 관리하는 정본입니다.

## 핵심 원칙

- `research_lens`는 전수조사 누락을 막는 범위이며 정규 대분류가 아닙니다.
- Candidate의 `discovery.lens_id`는 최초 발견 경로를 보존합니다.
- Candidate와 Unit의 `taxonomy.major_domain`·`subdomains`는 이 레지스트리의
  활성 노드만 참조합니다.
- 직무·업무 보기는 정규 분류를 복제하지 않고 여러 노드를 조합합니다.
- 외부 프레임워크 매핑은 동등성 선언이 아니라 누락·경계 교차검증입니다.
- 새 대분류, ID 변경, 병합과 폐기는 사용자 승인 후 수행합니다.

## 상태

- `research_lens`: 조사 계약에서만 승인된 누락 방지 렌즈
- `provisional`: 후보 조사로 발견했으나 정규화 전인 분류
- `canonical`: 사용자 승인과 정규화 Gate를 통과한 분류
- `deprecated`: 새 항목에서 참조할 수 없는 분류

Wave 5 정규화에서 Coverage와 승인·승격 근거가 있는 10개 domain과 97개
subdomain을 canonical로 확정했습니다. 최초 조사 렌즈 ID는 변경하지 않고
Candidate의 `discovery.lens_id`와 provenance에 발견 이력을 보존합니다.
`operational-value`, `benefits-realization`, `personalization-memory-user-control`은
deferred 근거만 있어 provisional로 유지합니다.

## 변경 순서

1. 새 분류의 정의, 포함·제외, 부모와 관련 노드를 제안합니다.
2. 기존 노드에 두었을 때의 탐색·소유권 비용과 분리 필요성을 비교합니다.
3. 외부 참고체계와 Candidate 근거를 연결하되 동등성을 추정하지 않습니다.
4. 새 대분류 또는 기존 ID 변경이면 Checkpoint와 변경 영향을 사용자에게
   제출하고 승인을 받습니다.
5. `taxonomy.json`과 Candidate·Unit 참조를 수정합니다.
6. 다음 명령으로 스키마, 활성 참조, 계층 순환과 alias 충돌을 검사합니다.

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

프론트엔드·백엔드·데이터 엔지니어링은 현재 `planned` 역할 보기입니다.
Wave 2·3 조사 결과에 따라 정규 대분류, 중분류 또는 역할 보기 중 적합한
목적지를 결정합니다.
