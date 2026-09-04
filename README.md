# 곰국 테트리스 — Read or Reject

**라이브: https://stack.saju.blog**

원고의 글자 하나하나가 테트로미노 블록이 되는 강제 완독 게임.
가로줄을 완성해 지우면 그 글자들은 '기독(旣讀)' 처리된다.
완독 100% = **Accept**, 원고가 천장(마감선)에 닿으면 **Reject**.

## 실행

단일 HTML 파일(`index.html`) — 브라우저에서 바로 열리면 끝.
외부 의존성은 웹폰트(Google Fonts)와 PDF 업로드용 pdf.js(CDN)뿐이고,
오프라인에서도 폴백 폰트로 플레이 가능.

## 기능

- 원고 입력: 직접 붙여넣기 / .txt / .pdf(pdf.js 텍스트 추출)
- **KCI·SSCI 상용구 모드**: 서론→방법→결과→논의 상용구로 논문 한 편 조립, 완성 문장 수집 로그
- 논문 단계 시스템: 줄을 지울수록 Ⅰ.서론 → Ⅴ.논의 → 게재확정 대기(승격 간격은 원고 분량에 비례)
- 판정: 교정됨/인용됨/게재예정/게재확정(TETRIS), combo, 신기록
- 생성 BGM(WebAudio, 파일 없음 — 단계별 고조), 효과음
- 키보드(←→↑↓/Space/C/P/B/M/Enter) + 모바일 터치(탭 회전·스와이프)
- 탭 이탈 자동 일시정지, 결과 클립보드 복사, localStorage 최고 기록(초기화 메뉴 있음)

## 개발·검증

URL에 `#dev` 를 붙이면 디버그 훅(`window.__pt`: 상태 조회, `forceClear()`,
에러 수집)이 활성화된다. 배포판 기본 주소에서는 노출되지 않는다.
경고 로그는 `console.warn("paper-tetris:", ...)` 접두사로 통일.

## 배포

**현재 운영 중**: AWS Lightsail(43.201.117.119) Apache —
문서루트 `/var/www/stack.saju.blog`, 가상호스트 `sites-available/stack.saju.blog.conf`,
Let's Encrypt 인증서(certbot 자동갱신), HTTP→HTTPS 리다이렉트, 보안 헤더 6종.
DNS(Spaceship): `stack` CNAME → `saju.blog`.

갱신 절차: `index.html` 수정 → 서버에 업로드(scp) → 끝(정적 파일이라 재시작 불필요):

```bash
scp index.html admin@43.201.117.119:/tmp/
ssh admin@43.201.117.119 "sudo mv /tmp/index.html /var/www/stack.saju.blog/ && sudo chown www-data:www-data /var/www/stack.saju.blog/index.html"
```

브랜드 에셋(파비콘·OG)은 `python make_assets.py`로 재생성(결과가 프로젝트 루트에도 복사됨).

Vercel 대안(참고): `npx vercel --prod` 또는 vercel.com/new에서 폴더 import.

## 디자인

klim.co.nz(Klim Type Foundry) 실측 문법 — 블랙 #0a0a0a · 아이보리 #f4f0e6 ·
시그니처 레드 #D33C03, 대형 세리프 디스플레이 + 소문자 와이드 트래킹 모노 라벨,
보드는 글리프만 렌더(적층=아이보리 이탤릭, 낙하=레드 이탤릭).

## 저작권 메모

DBpia "텍스트 테트리스"(paper-tetris-eight.vercel.app)는 컨셉 참고만 했고
코드·디자인·문구는 전부 별도 제작. 공유된 것은 "글자=블록, 줄=읽음"이라는
아이디어뿐이다.
