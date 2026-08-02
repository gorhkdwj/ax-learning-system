# 검색 표현 선택 Probe

이 선택형 2시간 Probe는 “온톨로지 또는 그래프를 사용하면 RAG가 항상 더
좋아진다”는 결론을 전제하지 않습니다. 동일한 공개·합성 문서와 12개 골든 질문에
세 방식의 고정 검색 결과 snapshot을 적용해 질문 충족, 안전 Gate와 유지비를
비교합니다.

이 Probe는 `unit.data-analytics-ml.domain-concept-relationship-modeling@1.0.0`의
10시간 핵심 Unit과 연결하면 총 12시간 D2 경로의 마지막 블록이 됩니다. 기존 RAG
Set에서는 계속 선택 단계이므로 다른 학습 경로의 필수 단계를 변경하지 않습니다.

## 입력

- 공개·합성 문서
- `probe.json`의 골든 질문 12개
- 텍스트·벡터 검색 결과 snapshot
- 메타데이터 필터·관계형 조회 snapshot
- 구조화된 관계 질의 snapshot

snapshot은 검색 시스템을 실시간 호출하지 않는 고정 fixture입니다. 따라서 같은
입력으로 자동 점수를 재현할 수 있지만 실제 제품·데이터의 우수성을 증명하지는
않습니다.

## 2시간 진행

1. 20분: 12개 질문의 필수 사실, 최신성, ACL과 답변 보류 조건을 확인합니다.
2. 35분: 세 snapshot의 필수 사실 회수와 잘못된 근거 포함을 자동 채점합니다.
3. 25분: 최신 상태, ACL 제외와 source trace를 사람 검토로 교차확인합니다.
4. 25분: 질문 유형별 검색 방식 선택표와 유지비를 작성합니다.
5. 15분: 선택하지 않은 방식의 제외 이유와 재검토 조건을 결정 기록에 남깁니다.

다음 명령은 제공 예시를 채점합니다.

```powershell
python tools/evaluate_retrieval_probe.py sets/set.workflow.retrieval-grounded-generation/resources/representation-probe/probe.json sets/set.workflow.retrieval-grounded-generation/resources/representation-probe/decision.example.json
```

자동 점수는 다음 항목을 다룹니다.

- 필수 사실 회수
- 잘못된 근거 포함
- 최신 상태 처리
- ACL 제외
- 답변 근거 추적성
- 구현·운영 유지비 순위

자동 통과만으로 학습 완료로 표시하지 마십시오. 사용자는 `decision.example.json`을
복사해 실제 선택표, 제외 이유, 재검토 조건을 작성하고 snapshot의 표본을 직접
검토해야 합니다.

## 선택 Gate

모든 필수 질문과 최신성·ACL·추적성 Gate를 통과하는 방식 가운데 유지비가 가장
낮은 방식을 기준선으로 선택합니다. 그래프 방식은 다음 조건을 모두 만족할 때만
선택할 수 있습니다.

1. 다른 방식이 충족하지 못한 필수 관계 질문이 재현됩니다.
2. 그래프 snapshot이 그 질문을 해결합니다.
3. 그래프 snapshot도 ACL과 최신성 Gate를 통과합니다.
4. 별도 관계 스키마·동기화·질의·운영 유지비를 수용할 이유를 기록합니다.

Probe를 건너뛰면 기존 RAG Set의 필수 단계와 수용 기준에는 변화가 없습니다.
실제 문의 실패나 새 관계 수요가 누적되기 전에는 그래프 저장·추론 엔진을 도입하지
않습니다.
