# 하드웨어 보안 모듈

!!! spec "규격 · 세대"
    Android **StrongBox KeyMint**(StrongBox는 Android 9에서 도입) · GlobalPlatform Secure Element 규격 · Common Criteria(보안 칩은 흔히 높은 공격 저항 등급 AVA_VAN.5 목표) · FIPS 140 계열 · GSMA eSIM(eUICC·iUICC)
    Apple Secure Enclave(A7, 2013) → Google Titan M(Pixel 3, 2018) → Titan M2(Pixel 6, 2021) · Samsung Knox Vault(Galaxy S21, 2021) · Qualcomm SPU(Snapdragon 845, 2017년 12월 발표)

!!! basic "한눈에 보기"
    TrustZone의 보안 세계는 일반 세계와 **같은 CPU를 시간을 나눠** 씁니다. 하드웨어 보안 모듈은 한 걸음 더 나아가, **아예 다른 프로세서와 메모리**를 둡니다.

    1. **전용 프로세서** — 자기만의 작은 CPU, ROM, RAM, 암호 엔진을 가집니다.
    2. **좁은 통로** — 메인 프로세서와는 메시지를 주고받는 통로 하나로만 대화합니다.
    3. **물리 공격 대비** — 전압·온도·빛 센서와 차폐로 칩을 뜯거나 흔드는 공격에 저항합니다.

    은행 금고실(TrustZone) 안에 있는 개인 금고(보안 모듈)를 떠올리면 됩니다. 금고실이 뚫려도, 금고는 따로 잠겨 있습니다.

## 종류와 배치 { .l2 }

| 구분 | 위치 | 예 | 장점 | 한계 |
|---|---|---|---|---|
| TEE (비교 기준) | 메인 CPU의 보안 세계 | QTEE, Trusty, TEEGRIS | 빠름, 추가 칩 없음 | CPU·캐시·DRAM 공유로 부채널·버그 영향 |
| eSE (embedded SE) | SoC 밖 별도 보안 칩 | Titan M2, 기기 제조사 탑재 eSE | 물리적으로 분리, 높은 인증 등급 | 느린 버스(SPI 등), 부품·면적 추가 |
| iSE (integrated SE) | SoC 다이 안 별도 보안 서브시스템 | Qualcomm SPU, Apple Secure Enclave | 칩 하나로 해결, 빠른 내부 연결 | SoC 공정·전원과 일부 공유, 인증 난도 |

Android에서는 이런 칩을 **StrongBox**로 노출합니다. 앱이 키를 만들 때 `setIsStrongBoxBacked(true)`를 지정하면 키가 TEE가 아니라 보안 칩 안에서 생성·사용됩니다. StrongBox는 TEE보다 느리고 지원 알고리즘이 적은 대신(예: RSA-2048, ECDSA P-256, AES, HMAC 중심), 키가 더 강하게 격리됩니다.

## 주요 구현 { .l2 }

| 구현 | 형태 | 주요 역할 |
|---|---|---|
| Apple Secure Enclave | SoC 안 별도 코어·전용 OS(sepOS) | Face ID·Touch ID 데이터 보호, 데이터 보호 키 계층, 전용 AES 엔진·난수 생성기 |
| Google Titan M2 | 별도 칩 (RISC-V 기반으로 발표) | StrongBox, 부트 검증 보조, Weaver(비밀번호 시도 제한), 펌웨어 롤백 보호 |
| Samsung Knox Vault | 보안 프로세서 + 전용 보안 메모리 | 비밀번호·생체 정보·키·블록체인 지갑 키 보관 |
| Qualcomm SPU | Snapdragon 다이 안 보안 서브시스템 | StrongBox 성격의 키 저장, 사용자 인증, 통합 SIM 등 |
| eSE (NFC·결제용) | NFC 컨트롤러 옆 별도 칩인 경우가 많음 | 결제 애플릿, 교통카드, 디지털 키 |

??? expert "전문가 노트 — Weaver와 시도 제한, iSE의 비휘발 저장, 키 증명의 신뢰 근거"
    **Weaver와 시도 제한.** Android의 Weaver HAL은 보안 칩 안에 "키 슬롯 + 비밀값 + 실패 카운터"를 둡니다. 화면 잠금 비밀번호에서 유도한 값이 맞아야 슬롯의 비밀값이 나오고, 이 비밀값이 사용자 데이터 암호화 키를 푸는 데 필요합니다. 실패 카운터와 대기 시간이 보안 칩 안에서 강제되므로, AP 쪽 TEE가 뚫려도 무차별 대입 속도는 칩이 허용하는 만큼으로 묶입니다.

    **iSE의 비휘발 저장.** SoC 다이에는 보통 플래시 메모리를 넣지 않으므로, 다이 안 보안 서브시스템은 상태(카운터, 키)를 밖에 저장해야 합니다. 일반적인 방법은 칩 고유 키로 암호화·인증한 데이터를 외부 저장장치에 두고, 되돌리기(replay) 공격을 막기 위해 RPMB나 전용 외부 보안 메모리를 함께 쓰는 것입니다. Apple은 Secure Enclave 전용 보안 저장 부품(Secure Storage Component)을 따로 두고, Samsung Knox Vault도 전용 보안 메모리를 둔다고 발표했습니다.

    **eSIM과 iSE.** 통신사 프로파일을 담는 eUICC는 전통적으로 별도 칩이지만, SoC 안 보안 서브시스템에서 SIM 기능을 돌리는 **iUICC(통합 SIM)** 방식도 표준화·상용화가 진행 중입니다. 이 경우 보안 서브시스템은 통신 사업자 요구 인증까지 통과해야 하므로, 설계와 인증 비용이 크게 늘어납니다([모뎀의 통합](../connectivity/modem.md)).

    **키 증명의 신뢰 근거.** KeyMint 키 증명 인증서 체인은 기기 제조 시 주입된 증명 키에서 시작하며, Google은 이를 원격 키 프로비저닝(RKP)으로 바꾸는 중입니다. 서버 입장에서는 "이 키가 정말 StrongBox 안에 있다"는 주장을 인증서 체인으로만 확인할 수 있으므로, 증명 키 유출은 해당 모델 전체의 신뢰를 떨어뜨립니다. 증명 키를 기기별·짧은 수명으로 바꾸는 흐름은 이 위험을 줄이기 위한 것입니다.

## 칩셋 비교

| 항목 | Snapdragon | Exynos (Galaxy) | Dimensity | Tensor (Pixel) | Apple |
|---|---|---|---|---|---|
| 하드웨어 보안 모듈 | SPU (다이 안) | Knox Vault (기기 기능) | 기기 제조사 선택 (eSE 등) | Titan M2 (별도 칩) | Secure Enclave (다이 안) |
| 형태 | iSE | 보안 프로세서 + 전용 메모리 | 대개 eSE | eSE | iSE |
| Android 노출 | StrongBox | StrongBox | StrongBox (탑재 시) | StrongBox, Weaver | 해당 없음 (Keychain·CryptoKit) |

> 같은 SoC라도 기기마다 보안 칩 구성이 다를 수 있으므로, 세대별 정보는 [칩셋 세대 인덱스](../reference/chipset-index.md)에 기준 시점과 함께 모읍니다.

## 관련 페이지
- [TrustZone과 TEE](trustzone.md) — 보안 모듈과 TEE의 역할 분담
- [암호 가속과 키 관리](crypto.md) — 보안 모듈이 지키는 키 계층
- [하드웨어 공격과 대응](attacks.md) — 보안 칩이 막으려는 물리 공격
- [모뎀의 통합](../connectivity/modem.md) — 통합 SIM과 모뎀 서브시스템
