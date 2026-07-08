# -*- coding: utf-8 -*-
"""자몽 사전예약 랜딩 페이지 빌드: 자몽이 이미지를 base64로 인라인해 단일 index.html 생성."""
import base64
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MASCOT = HERE.parent / "dream-shorts" / "assets" / "mascot" / "jamongi.png"

# 출시 알림: 카카오톡 채널 추가
FORM_URL = "https://pf.kakao.com/_CswwX"

HTML = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>자몽 — 자면서 꾼 꿈해몽</title>
<meta name="description" content="내 꿈에 딱 맞는 AI 맞춤 해몽, 자몽. 출시 알림을 받아보세요.">
<style>
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    font-family:'Pretendard','Apple SD Gothic Neo','Malgun Gothic',sans-serif;
    background:linear-gradient(180deg,#121030 0%,#1d1440 55%,#34215a 100%);
    color:#fff; min-height:100vh; display:flex; flex-direction:column; align-items:center;
    overflow-x:hidden; position:relative;
  }
  .stars { position:fixed; inset:0; pointer-events:none; z-index:0; }
  .star { position:absolute; background:#fff; border-radius:50%; opacity:.7;
          animation:tw 3s infinite ease-in-out; }
  @keyframes tw { 0%,100%{opacity:.25} 50%{opacity:.9} }
  main { position:relative; z-index:1; max-width:430px; width:100%;
         padding:56px 24px 48px; text-align:center; }
  .mascot { width:130px; height:130px; animation:float 3.2s ease-in-out infinite; }
  @keyframes float { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
  .badge { display:inline-block; background:rgba(255,255,255,.12); border-radius:999px;
           padding:7px 16px; font-size:13px; margin-top:18px; letter-spacing:.3px; }
  h1 { font-size:34px; margin-top:14px; letter-spacing:-.5px; }
  h1 .accent { color:#ff9e80; }
  .sub { margin-top:10px; font-size:16px; line-height:1.6; color:#cfc6e8; }
  .features { margin-top:34px; display:flex; flex-direction:column; gap:12px; text-align:left; }
  .feat { background:rgba(255,255,255,.07); border:1px solid rgba(255,255,255,.09);
          border-radius:16px; padding:16px 18px; display:flex; gap:14px; align-items:center; }
  .feat .ico { font-size:24px; }
  .feat b { font-size:15px; display:block; }
  .feat span { font-size:13px; color:#bdb2dd; }
  .cta { display:block; margin-top:36px; background:#FEE500;
         color:#191919; font-weight:800; font-size:18px; text-decoration:none;
         padding:18px 20px; border-radius:16px; box-shadow:0 8px 28px rgba(254,229,0,.25); }
  .cta:active { transform:scale(.98); }
  .cta-sub { margin-top:12px; font-size:13px; color:#bdb2dd; }
  footer { margin-top:44px; font-size:12px; color:#8d82ad; line-height:1.7; }
</style>
</head>
<body>
<div class="stars" id="stars"></div>
<main>
  <img class="mascot" src="data:image/png;base64,%%MASCOT_B64%%" alt="자몽이">
  <div class="badge">🌙 AI 꿈해몽 앱 · 출시 준비 중</div>
  <h1>자몽<span class="accent">.</span></h1>
  <p class="sub">자면서 꾼 꿈, 무슨 뜻일까?<br>
  키워드 사전이 아니라 <b>내 꿈 상황 전체</b>를 읽는<br>AI 맞춤 해몽</p>

  <div class="features">
    <div class="feat"><div class="ico">🎙️</div>
      <div><b>일어나자마자 말로 기록</b><span>꿈은 5분이면 잊혀요. 음성으로 바로 남기세요</span></div></div>
    <div class="feat"><div class="ico">🔮</div>
      <div><b>내 꿈에 딱 맞는 풀이</b><span>같은 뱀꿈이라도 상황 따라 해석이 달라져요</span></div></div>
    <div class="feat"><div class="ico">📅</div>
      <div><b>꿈 일기 아카이브</b><span>해몽 기록이 달력에 자동으로 쌓여요</span></div></div>
  </div>

  <a class="cta" href="%%FORM_URL%%">💬 카카오톡 채널 추가하고 알림 받기</a>
  <p class="cta-sub">버튼 한 번이면 출시 소식을 가장 먼저 받아요</p>

  <footer>
    * 자몽의 해몽은 재미로 보는 AI 콘텐츠입니다.<br>
    ⓒ 2026 자몽 — 자면서 꾼 꿈해몽
  </footer>
</main>
<script>
  const box = document.getElementById('stars');
  for (let i = 0; i < 70; i++) {
    const s = document.createElement('div');
    s.className = 'star';
    const size = Math.random() * 2.5 + 1;
    s.style.cssText = `width:${size}px;height:${size}px;left:${Math.random()*100}%;` +
      `top:${Math.random()*100}%;animation-delay:${Math.random()*3}s`;
    box.appendChild(s);
  }
</script>
</body>
</html>
"""


def main() -> None:
    b64 = base64.b64encode(MASCOT.read_bytes()).decode()
    html = HTML.replace("%%MASCOT_B64%%", b64).replace("%%FORM_URL%%", FORM_URL)
    out = HERE / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"저장: {out} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    sys.exit(main())
