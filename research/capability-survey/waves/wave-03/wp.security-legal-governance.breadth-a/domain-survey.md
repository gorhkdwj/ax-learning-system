# 도메인 조사: 보안·법무·거버넌스

## 결론

기존 정규 catalog와 교차검토한 결과, 이 패키지는 독립적인 9개 Unit 후보와 이를
조합하는 1개 Set 후보로 구성합니다. 기술 보안, 개인정보, 보안사고, 감사증거,
디지털 자산 권리, AI 보안·거버넌스를 포함하며 일반 소프트웨어 개발·플랫폼 운영·
Human-AI 승인 경험의 기존 소유권은 복제하지 않습니다.

| 후보 | 목적지 | 목표 | 독립 경계 |
|---|---|---|---|
| 보안 위험·요구·위협 모델·통제 검증 | Unit | D3 | 보안위험에서 검증 가능한 통제를 도출 |
| 접근 정책·권한 수명주기 | Unit | 제한 D3 | authorization 접근결정과 권한 수명주기 |
| 비밀·credential·암호키 수명주기 | Unit | 제한 D3 | synthetic canary·공개 test key만 사용 |
| 소프트웨어 공급망 무결성·취약점 거버넌스 | Unit | D3 | SBOM·provenance·취약점 예외 판정 |
| 개인정보 공학·영향평가·데이터 권리 수명주기 | Unit | D2 | privacy 영향·권리·전문검토 이관 |
| 보안사고 증거보존·신고의무 검토 이관 | Unit | D2 | 기존 플랫폼 사고대응을 입력으로 받는 evidence·qualified routing |
| 보안통제 보증·감사증거·예외 거버넌스 | Unit | D3 | 통제–증거–예외 평가 |
| 디지털 자산 저작권·라이선스 출처 추적·검토 이관 | Unit | D2 | 권리 provenance와 법률검토 이관 |
| AI 시스템 보안위협 평가 | Unit | 제한 D3 | AI 고유 위협·안전통제 회귀 |
| AI 시스템 위험·영향 거버넌스 보증 | Set | D3 | 기존 AI·Human-AI Unit과 위 후보를 조합 |

## 근거와 버전 판단

- 보안공학·통제는 NIST SP 800-160 Vol. 1 Rev. 1, CSF 2.0, SP 800-53/53A
  Release 5.2.0과 OWASP ASVS 5.0.0을 사용합니다.
- digital identity는 2025년 최종 NIST SP 800-63-4, ABAC는 SP 800-162,
  OAuth 보안은 RFC 9700을 사용합니다.
- 공급망은 최종 SSDF 1.1, SLSA 1.2, SPDX 3.0.1을 사용하며 draft를 정본으로
  취급하지 않습니다. 암호키는 최종 NIST SP 800-57 Part 1 Rev. 5를 사용합니다.
- privacy는 최종 NIST Privacy Framework 1.0과 GDPR 1차 법령, W3C DPV 2.0을
  사용하되 DPV가 W3C 표준이 아닌 Final Community Group Report임을 명시하고
  관할별 적용성은 qualified review 대상으로 둡니다.
- 보안사고는 NIST SP 800-61 Rev. 3과 SP 800-86을 사용하며 실제 신고·증거능력
  판단은 학습 범위에서 제외합니다.
- 감사증거는 NIST SP 800-53/53A Release 5.2.0과 OSCAL 1.2.2를, 권리
  provenance는 SPDX 3.0.1, OpenChain ISO/IEC 5230:2020, W3C PROV-DM과
  ODRL 2.2를 사용하며 법적 유효성 판단을 보증하지 않습니다.
- AI는 NIST AI RMF 1.0, AI 600-1, AI 100-2 E2025, SP 800-218A와 OWASP
  LLM Top 10 2025를 사용하고 개정 진행·errata·비인증 기준이라는 한계를 기록합니다.
  EU AI Act는 원 제정법 2024/1689와 2026-07-27 발효된 개정법 2026/1744를
  함께 확인하며 단계적 적용일과 실제 관할·분류는 qualified review로 이관합니다.

## 중복·누락 레드팀

- secure coding은 보안 요구·통제 후보와 기존 layered verification에 연결합니다.
- zero trust는 identity·접근정책 수명주기에 포함합니다.
- vulnerability disclosure는 공급망 remediation과 보안사고 routing에 연결합니다.
- cross-border transfer, 아동·생체정보·분야별 규제, 계약·SCC·eDiscovery,
  특허·상표·영업비밀은 관할 adapter·전문가 Set 또는 Resource 후보로 보류합니다.
- AI fairness·투명성·인간감독은 기존 기반·Human-AI·모델평가 Unit을 Set에서
  조합하며 같은 정의·실습을 새 Unit으로 복제하지 않습니다.
- 독립 발견 감사의 마지막 누락 점검에서 추가 고우선 후보는 0개였습니다.
- authentication·session·federation 보안 검증과 security detection
  engineering·alert triage는 10개 상한과 독립 산출물 근거 때문에 이번에는
  `defer`로 기록하고 후속 보안 engineering 조사에서 재검토합니다.
- 제3자·vendor·SaaS 보안/privacy assurance와 비개인 민감정보의 분류·취급
  수명주기도 이번 상한에서는 `defer`로 기록하고 조직·도입 조사 및 후속
  security governance package에서 재검토합니다.

## 안전 경계

모든 평가는 합성 fixture, fake identity, synthetic secret canary, 공개 test key,
loopback·일회성 sandbox만 사용합니다. 실제 개인정보·비밀·운영 권한·외부 target
scan·exploit·통지·신고·법률 결론은 수행하지 않습니다. 법률·규제·위험수용의 최종
판단은 `needs_qualified_review`로 중단·이관합니다.
