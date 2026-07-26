# Trend Signal 레지스트리

신흥 용어·개념·패턴을 Learning Unit에 편입하기 전에 조사하는 인입
레지스트리입니다. 운영 규칙은 `docs/research/trend-signal-governance.md`,
필드 정본은 `schemas/trend-signal.schema.json`을 따릅니다.

| Signal | 현재 상태 | 정의 신뢰도 | 효과 신뢰도 | 후보 목적지 | 다음 검토 |
|---|---|---|---|---|---|
| Agent harness | `substantiated` | high | medium | `probe_set` | 2026-10-26 |
| Agent execution control loop / Loop Engineering | `researching` | medium | low | `observe` | 2026-08-26 |
| Karpathy-style LLM Wiki | `substantiated` | high | low | `probe_set` | 2026-08-26 |

이 표는 탐색용 요약이며 정본이 아닙니다. 상태나 날짜를 바꿀 때에는 각
`signal.json`을 먼저 수정하고 표를 함께 갱신합니다. 향후 HUB에서는 이 요약을
직접 유지하지 않고 메타데이터에서 생성합니다.

전체 검증은 작업공간 루트에서 실행합니다.

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```
