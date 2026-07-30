# 근거 독립 감사: wp.security-legal-governance.breadth-a

## 범위

- Candidate 10개 전수
- 공식 표준·법령·사양의 URL·버전·문서 지위·현재성과 claim 한계
- 기존 catalog와의 근거 중복 및 전체 누락 레드팀

감사자는 파일을 수정하지 않고 메인 세션만 교정을 반영했습니다.

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 5개 교정군 |

P1은 다음과 같이 처리했습니다.

1. DPV 2.0을 공식 Final Community Group Report URL·발행 주체·비표준 지위로
   교정했습니다.
2. OSCAL Assessment Results를 최신 1.2.2로 갱신했습니다.
3. 디지털 자산 권리 표현에 W3C ODRL 2.2를 추가하고 법적 유효성 보증이
   아니라는 한계를 고정했습니다.
4. authorization의 SoD·emergency account·least privilege Gate에 NIST
   SP 800-53 Release 5.2.0 AC-2·AC-5·AC-6 근거를 연결했습니다.
5. EU AI Act 2024/1689에 2026-07-27 발효된 2026/1744 개정법과 단계적
   적용 한계를 추가하고 GDPR 사고 근거를 personal data breach 분기로
   좁혔습니다.

## 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |

- 30개 고유 evidence ID와 28개 고유 URL을 전수 확인했고 URL은 모두
  HTTP 200이었습니다.
- authentication·session·federation, detection engineering·alert triage,
  vendor·SaaS assurance와 비개인 민감정보 취급은 후속 조사 대상으로
  `defer`했습니다.

## 결론

최종 P0·P1은 0건이며 Candidate 10개 모두 승격 가능합니다. 이 판정은 실제
조직·관할·제품 적합성이나 법률·규제 결론을 뜻하지 않습니다.
