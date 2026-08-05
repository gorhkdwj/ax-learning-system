# Studies: 자료 단위 학습 기록

이 디렉터리는 아티클·영상·팟캐스트·비공개 문서 등 **자료 한 편**을 단위로
학습 기록을 보관하는 자리입니다. 상세 설계는
`docs/plans/study-layer-design.md`를 따릅니다.

## 지위

Study는 다섯 번째 학습 계층이 아니라 네 학습 계층 옆의 학습 기록입니다.

- 이수 대상이 아니며 숙련도 D0–D4를 부여하지 않습니다.
- 선수관계 DAG에 참여하지 않습니다.
- 자료 소비량은 숙련도 주장이 되지 않습니다. 숙련도 완료 주장에는 별도의
  독립 실행과 전이평가 증거가 필요합니다.

용어·개념 하나를 조사하는 기록은 Trend Signal(`research/signals/`)이며,
자료를 보다 새 용어를 발견한 경우에만 Signal을 별도로 만들고
`discovered_signal_refs`로 연결합니다.

## 상태 모델

```text
read -> applied -> archived
```

| 상태 | 의미 | 필수 조건 |
|---|---|---|
| `read` | 자료를 보고 요약과 적용 판정을 남겼습니다. | `takeaways` 1건 이상, `applicability` |
| `applied` | 실제 업무나 산출물에 반영했습니다. | 위 조건과 `application`, `human_confirmed` 이상 takeaway 1건 이상 |
| `archived` | 더 이상 활성 참조하지 않으며 이력만 보존합니다. | 없음 |

`applied`로 올릴 때 사람 확인을 요구하는 이유는 자동 자막과 Whisper의
오인식·환각, 프레임 해석 오류가 실재하기 때문입니다. AI가 정리한 요약만
근거로 업무 반영을 표시하지 않습니다.

## 작성 절차

1. `templates/metadata/learning-study.template.json`을 복사하여
   `studies/study.<이름>/study.json`으로 저장합니다.
2. 자리표시자를 실제 값으로 바꿉니다. `taxonomy_refs`는 활성 Taxonomy
   Registry의 node ID를 사용하며, 맞는 분류가 없으면 `taxonomy_gap`에
   메모를 남깁니다.
3. `source`에는 공개 URL 또는 Vault의 불투명한 `private_source_ref` 중
   최소 하나를 기록합니다. Vault의 실제 파일명·경로는 넣지 않습니다.
4. 영상·팟캐스트 자료에는 `media`에 `transcript_source`를 기록하고,
   화면 표기로 확정한 정정은 `media.corrections`에 남깁니다.
5. `takeaways`의 각 항목에 근거 유형과 검증 상태를 기록합니다.
   `cross_checked`에는 공식 출처 `source_url`이 필요합니다.
6. `outcome_coverage`는 작성 시점에 비워 두고, 해당 분야 Unit 학습을
   시작할 때 기존 Study를 훑으며 채웁니다.

## 검증

작업공간 루트에서 다음을 실행합니다.

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

검증기는 스키마 정합성과 함께 분류 node 실재, 원천 존재, `applied` 승격
조건, `contradicts` 표시의 공식 근거, Unit·학습성과·Signal 참조 실재를
검사합니다.
