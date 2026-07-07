import streamlit as st

st.set_page_config(
    page_title="10만원으로 내집마련 — 미국 주식 주간 리포트",
    page_icon="📈",
    layout="wide",
)

# Streamlit 기본 여백/헤더를 최대한 숨겨서 HTML이 전체 화면을 쓰도록 함
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container {
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
        }
        iframe {
            width: 100%;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# index.html 내용을 그대로 포함 (별도 파일 불필요)
HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>10만원으로 내집마련 — 미국 주식 주간 리포트</title>
  <meta name="description" content="매주 미국 주식 섹터 분석, 이슈 정리, 주목할 종목까지. 미국 주식 주린이를 위한 주간 투자 리포트." />

  <style>
    /* ============ 디자인 토큰 ============ */
    :root {
      --bg:        #0e1117;
      --surface:   #161b22;
      --surface-2: #1c2230;
      --ink:       #ffffff;
      --ink-soft:  #cfd6e0;
      --line:      #232b36;

      --up:        #ef3e3e;   /* 상승 = 빨강 (국내 관습) */
      --up-soft:   rgba(239, 62, 62, 0.14);
      --down:      #2f81f7;   /* 하락 = 파랑 */
      --down-soft: rgba(47, 129, 247, 0.14);
      --accent:    #ff4d4d;

      --radius:    16px;
      --shadow:    0 12px 40px -16px rgba(0,0,0,0.6);
      --maxw:      1080px;
      --font:      'Pretendard', 'Apple SD Gothic Neo', 'Segoe UI', system-ui, -apple-system, sans-serif;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      font-family: var(--font);
      color: var(--ink);
      background: var(--bg);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }
    a { color: inherit; text-decoration: none; }
    .wrap { width: 100%; max-width: var(--maxw); margin: 0 auto; padding: 0 20px; }

    /* ============ 헤더 ============ */
    header {
      position: sticky; top: 0; z-index: 50;
      background: rgba(14, 17, 23, 0.82);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--line);
    }
    .nav { display: flex; align-items: center; justify-content: space-between; height: 64px; }
    .logo { display: flex; align-items: center; gap: 10px; font-weight: 800; font-size: 1.12rem; letter-spacing: -0.02em; }
    .logo .dot {
      width: 30px; height: 30px; border-radius: 9px;
      background: linear-gradient(135deg, var(--accent), #b81414);
      display: grid; place-items: center; color: #fff; font-size: 0.95rem;
    }
    .nav-links { display: flex; align-items: center; gap: 26px; }
    .nav-links a { color: var(--ink-soft); font-weight: 500; font-size: 0.92rem; transition: color .15s; }
    .nav-links a:hover { color: var(--ink); }
    .week-pill {
      font-size: 0.78rem; font-weight: 600; color: var(--accent);
      background: var(--up-soft); border: 1px solid rgba(239,62,62,0.25);
      padding: 5px 12px; border-radius: 999px;
    }

    /* ============ API 키 바 ============ */
    .apibar { background: var(--surface); border-bottom: 1px solid var(--line); }
    .apibar.ok { background: rgba(3,199,90,0.08); border-color: rgba(3,199,90,0.3); }
    .apibar-in { display: flex; align-items: center; justify-content: space-between; gap: 14px; padding: 10px 20px; flex-wrap: wrap; }
    .apibar-msg { font-size: 0.85rem; color: var(--ink-soft); }
    .apibar-msg a { color: var(--accent); font-weight: 700; }
    .apibar.ok .apibar-msg { color: #29c46a; font-weight: 600; }
    .apibar-form { display: flex; gap: 8px; }
    .apibar-form input {
      background: var(--surface-2); border: 1px solid var(--line); border-radius: 8px;
      padding: 8px 12px; color: var(--ink); font-family: inherit; font-size: 0.85rem; width: 240px; max-width: 46vw;
    }
    .apibar-form input:focus { outline: none; border-color: var(--accent); }
    .apibar-form button {
      background: var(--accent); color: #fff; border: none; border-radius: 8px;
      padding: 8px 14px; font-weight: 700; font-family: inherit; font-size: 0.85rem; cursor: pointer;
    }
    .apibar-form #apiClear { background: var(--surface-2); color: var(--ink-soft); border: 1px solid var(--line); }

    /* ============ 히어로 ============ */
    .hero { padding: 40px 0 20px; }
    .hero .eyebrow { color: var(--accent); font-weight: 700; font-size: 0.85rem; letter-spacing: .04em; }
    .hero h1 { font-size: clamp(1.7rem, 4.5vw, 2.5rem); font-weight: 800; letter-spacing: -0.03em; line-height: 1.2; margin: 8px 0 10px; }
    .hero p { color: var(--ink-soft); font-size: 1rem; max-width: 620px; }

    /* 지수 요약 스트립 */
    .index-strip { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-top: 26px; }
    .idx {
      position: relative; text-align: left; font-family: inherit; cursor: pointer;
      background: var(--surface); border: 1px solid var(--line);
      border-radius: var(--radius); padding: 16px 18px;
      transition: transform .16s, border-color .16s;
    }
    .idx:hover { transform: translateY(-3px); border-color: rgba(239,62,62,0.45); }
    .idx .name { font-size: 0.82rem; color: var(--ink-soft); font-weight: 600; }
    .idx .val { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; margin-top: 4px; color: var(--ink); }
    .idx .chg { font-size: 0.85rem; font-weight: 700; margin-top: 2px; }
    .idx-hint {
      display: block; margin-top: 8px; font-size: 0.72rem; font-weight: 700; color: var(--ink-soft);
      opacity: 0; transform: translateX(-4px); transition: opacity .16s, transform .16s, color .16s;
    }
    .idx:hover .idx-hint { opacity: 1; transform: none; color: var(--accent); }

    /* ============ 차트 모달 ============ */
    .modal {
      position: fixed; inset: 0; z-index: 100;
      display: flex; align-items: center; justify-content: center; padding: 20px;
      background: rgba(6, 8, 12, 0.72); backdrop-filter: blur(6px);
      opacity: 0; pointer-events: none; transition: opacity .22s ease;
    }
    .modal.open { opacity: 1; pointer-events: auto; }
    .modal-panel {
      position: relative;
      width: 100%; max-width: 780px; background: var(--surface);
      border: 1px solid var(--line); border-radius: 20px; box-shadow: var(--shadow);
      padding: 24px; transform: translateY(16px) scale(.98); transition: transform .22s ease;
    }
    .modal.open .modal-panel { transform: none; }
    .modal-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
    .modal-head .m-name { font-size: 1.4rem; font-weight: 800; letter-spacing: -0.02em; }
    .modal-head .m-sub { color: var(--ink-soft); font-size: 0.85rem; }
    .modal-head .m-price { text-align: right; }
    .modal-head .m-price .m-val { font-size: 1.5rem; font-weight: 800; font-variant-numeric: tabular-nums; }
    .m-close {
      background: var(--surface-2); border: 1px solid var(--line); color: var(--ink);
      width: 38px; height: 38px; border-radius: 10px; font-size: 1.2rem; cursor: pointer;
      display: grid; place-items: center; transition: .15s; margin-left: 6px;
    }
    .m-close:hover { border-color: var(--accent); color: var(--accent); }
    .m-chart { width: 100%; height: 300px; display: block; margin: 18px 0 12px; overflow: visible; }
    .m-range { display: flex; gap: 8px; justify-content: flex-end; }
    .m-range button {
      background: var(--surface-2); border: 1px solid var(--line); color: var(--ink-soft);
      border-radius: 8px; padding: 6px 15px; font-size: 0.82rem; font-weight: 700;
      font-family: inherit; cursor: pointer; transition: .15s;
    }
    .m-range button.active { background: var(--up-soft); color: var(--accent); border-color: rgba(239,62,62,0.4); }
    .up   { color: var(--up); }
    .down { color: var(--down); }

    /* ============ 섹션 공통 ============ */
    section.block { padding: 40px 0; }
    .sec-head { display: flex; align-items: baseline; justify-content: space-between; gap: 12px; margin-bottom: 22px; flex-wrap: wrap; }
    .sec-head h2 { font-size: clamp(1.25rem, 3vw, 1.6rem); font-weight: 800; letter-spacing: -0.02em; }
    .sec-head .sub { color: var(--ink-soft); font-size: 0.88rem; }

    .card {
      background: var(--surface); border: 1px solid var(--line);
      border-radius: var(--radius); box-shadow: var(--shadow);
    }

    /* ============ 종목 검색 ============ */
    .search-card { padding: 22px; }
    .search-form { display: flex; gap: 10px; }
    .search-input {
      flex: 1; min-width: 0;
      background: var(--surface-2); border: 1px solid var(--line);
      border-radius: 12px; padding: 14px 16px; color: var(--ink);
      font-size: 1rem; font-family: inherit; outline: none;
      transition: border-color .15s, box-shadow .15s;
    }
    .search-input::placeholder { color: var(--ink-soft); }
    .search-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px var(--up-soft); }
    .search-btn {
      background: linear-gradient(135deg, var(--accent), #b81414); color: #fff;
      border: none; border-radius: 12px; padding: 0 24px; font-size: 0.98rem;
      font-weight: 700; font-family: inherit; cursor: pointer; white-space: nowrap;
      transition: transform .15s, filter .15s;
    }
    .search-btn:hover { transform: translateY(-2px); filter: brightness(1.08); }

    .quick-tickers { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 14px; }
    .quick-tickers .q-label { font-size: 0.8rem; color: var(--ink-soft); font-weight: 600; margin-right: 2px; }
    .quick-tickers button {
      background: var(--surface-2); border: 1px solid var(--line); color: var(--ink-soft);
      border-radius: 999px; padding: 6px 13px; font-size: 0.82rem; font-weight: 600;
      font-family: inherit; cursor: pointer; transition: color .15s, border-color .15s;
    }
    .quick-tickers button:hover { color: var(--accent); border-color: rgba(239,62,62,0.4); }

    .chart-result { position: relative; margin-top: 22px; border-top: 1px solid var(--line); padding-top: 20px; }
    .cr-stats { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 16px; }
    .cr-stat { background: var(--surface-2); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; }
    .cr-stat .k { font-size: 0.78rem; color: var(--ink-soft); font-weight: 600; }
    .cr-stat .v { font-size: 1.05rem; font-weight: 800; margin-top: 3px; font-variant-numeric: tabular-nums; }
    .cr-stat .v.hi { color: var(--up); } .cr-stat .v.lo { color: var(--down); }
    .cr-note { color: var(--ink-soft); font-size: 0.9rem; grid-column: 1 / -1; }
    .cr-link {
      grid-column: 1 / -1; display: block; text-align: center; margin-top: 4px;
      background: var(--surface-2); border: 1px solid var(--line); border-radius: 10px;
      padding: 12px; font-weight: 700; font-size: 0.9rem; color: var(--accent); transition: .15s;
    }
    .cr-link:hover { border-color: var(--accent); }
    @media (max-width: 560px) { .cr-stats { grid-template-columns: repeat(2, 1fr); } }

    /* 예시 데이터 안내 배너 */
    .demo-note {
      background: rgba(245, 180, 69, 0.14); border-bottom: 1px solid rgba(245,180,69,0.35);
      color: #f5b445; font-size: 0.85rem; font-weight: 600; text-align: center; padding: 9px 20px;
    }
    .demo-note b { color: #ffcf7a; }

    /* API 키 필요 안내 */
    .need-key { padding: 22px; text-align: center; color: var(--ink-soft); font-size: 0.92rem; line-height: 1.6; }
    .need-key b { color: var(--ink); }
    .idx-sub { font-size: 0.72rem; color: var(--ink-soft); font-weight: 600; }

    /* 실시간 뉴스 피드 */
    .newsfeed { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
    .news-card {
      display: flex; flex-direction: column; gap: 8px; padding: 18px 18px;
      background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius);
      box-shadow: var(--shadow); transition: transform .16s, border-color .16s;
    }
    .news-card:hover { transform: translateY(-3px); border-color: rgba(239,62,62,0.4); }
    .news-src { font-size: 0.78rem; color: var(--ink-soft); font-weight: 600; }
    .news-h { font-size: 1rem; font-weight: 700; line-height: 1.45; }
    .news-sum { font-size: 0.88rem; color: var(--ink-soft); line-height: 1.55; }
    .news-arrow { font-size: 0.82rem; font-weight: 700; color: var(--accent); margin-top: auto; }
    @media (max-width: 720px) { .newsfeed { grid-template-columns: 1fr; } }

    /* 주목 종목 실시간 가격 */
    .pick-price { font-size: 1.15rem; font-weight: 800; margin: 6px 0 2px; font-variant-numeric: tabular-nums; }
    .pick .chg { font-size: 0.95rem; font-weight: 800; }
    .pick .chg.up { color: var(--up); } .pick .chg.down { color: var(--down); }
    .cr-head { display: flex; align-items: flex-end; justify-content: space-between; gap: 12px; flex-wrap: wrap; }
    .cr-info b { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; }
    .cr-info small { display: block; color: var(--ink-soft); font-size: 0.85rem; }
    .cr-price { text-align: right; }
    .cr-price #crPrice { font-size: 1.3rem; font-weight: 800; font-variant-numeric: tabular-nums; }
    .chg-tag { display: inline-block; margin-left: 8px; font-size: 0.9rem; font-weight: 700; padding: 3px 10px; border-radius: 8px; }
    .chg-tag.up   { background: var(--up-soft);   color: var(--up); }
    .chg-tag.down { background: var(--down-soft); color: var(--down); }
    .cr-chart { width: 100%; height: 220px; display: block; margin: 16px 0 10px; overflow: visible; cursor: crosshair; }
    .cr-cross { stroke: var(--ink-soft); stroke-width: 1; stroke-dasharray: 3 3; }
    .cr-dot { fill: #fff; stroke: var(--accent); stroke-width: 2; }
    .cr-tip {
      position: absolute; top: 54px; transform: translateX(-50%); z-index: 5; pointer-events: none;
      background: var(--surface-2); border: 1px solid var(--line); border-radius: 10px;
      padding: 9px 11px; font-size: 0.78rem; white-space: nowrap; box-shadow: 0 8px 24px -10px rgba(0,0,0,0.7);
    }
    .cr-tip-date { font-weight: 800; margin-bottom: 6px; font-size: 0.8rem; }
    .cr-row { display: flex; justify-content: space-between; gap: 16px; line-height: 1.7; }
    .cr-row span { color: var(--ink-soft); }
    .cr-row b { font-variant-numeric: tabular-nums; }
    .cr-row b.up { color: var(--up); } .cr-row b.down { color: var(--down); }
    .cr-range { display: flex; gap: 8px; justify-content: flex-end; }
    .cr-range button {
      background: var(--surface-2); border: 1px solid var(--line); color: var(--ink-soft);
      border-radius: 8px; padding: 5px 14px; font-size: 0.82rem; font-weight: 700;
      font-family: inherit; cursor: pointer; transition: .15s;
    }
    .cr-range button.active { background: var(--up-soft); color: var(--accent); border-color: rgba(239,62,62,0.4); }

    /* ============ 요소 1 · 섹터 상승률 차트 ============ */
    .sector-chart { padding: 24px 22px; }
    .bar-row { display: grid; grid-template-columns: 108px 1fr 64px; align-items: center; gap: 12px; padding: 9px 0; }
    .bar-row .label { font-size: 0.9rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .bar-track { position: relative; height: 22px; background: var(--surface-2); border-radius: 6px; }
    .bar-mid { position: absolute; left: 50%; top: -3px; bottom: -3px; width: 1px; background: var(--line); }
    .bar-fill {
      position: absolute; top: 0; height: 100%; border-radius: 6px;
      width: 0; transition: width 1.1s cubic-bezier(.2,.8,.2,1);
    }
    .bar-fill.pos { left: 50%; background: linear-gradient(90deg, rgba(239,62,62,.55), var(--up)); }
    .bar-fill.neg { right: 50%; background: linear-gradient(270deg, rgba(47,129,247,.55), var(--down)); }
    .bar-row .pct { text-align: right; font-size: 0.9rem; font-weight: 700; font-variant-numeric: tabular-nums; }
    .bar-row.clickable { cursor: pointer; border-radius: 8px; padding-left: 6px; padding-right: 6px; transition: background .14s; }
    .bar-row.clickable:hover { background: var(--surface-2); }
    .bar-row.clickable:hover .label { color: var(--accent); }

    /* 섹터 모달 · 대표 종목 */
    .sec-chart-info { display: flex; align-items: center; gap: 10px; margin: 4px 0 2px; flex-wrap: wrap; }
    .sec-chart-info b { font-size: 1.15rem; font-weight: 800; letter-spacing: -0.01em; }
    .sec-chart-info small { color: var(--ink-soft); font-size: 0.85rem; }
    .sec-stocklist { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 16px; }
    .stk {
      display: flex; align-items: center; gap: 10px; text-align: left; font-family: inherit; cursor: pointer;
      background: var(--surface-2); border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; transition: .14s;
    }
    .stk:hover { border-color: rgba(239,62,62,0.4); }
    .stk.active { border-color: var(--accent); background: var(--up-soft); }
    .stk-badge {
      font-size: 0.72rem; font-weight: 800; color: #fff; flex: none;
      background: linear-gradient(135deg, var(--accent), #8f1010); padding: 4px 7px; border-radius: 6px;
    }
    .stk-name { flex: 1; font-size: 0.9rem; font-weight: 600; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .stk-chg { font-size: 0.85rem; font-weight: 800; font-variant-numeric: tabular-nums; }
    .stk-chg.up { color: var(--up); } .stk-chg.down { color: var(--down); }

    /* 상세 모달 · 관련 기사 */
    .d-art-title { font-size: 0.95rem; font-weight: 800; margin: 20px 0 10px; }
    .art {
      display: flex; align-items: flex-start; gap: 12px; padding: 12px 14px; margin-bottom: 8px;
      border: 1px solid var(--line); border-radius: 10px; background: var(--surface-2); transition: .14s;
    }
    .art:hover { border-color: rgba(239,62,62,0.4); transform: translateY(-2px); }
    .art .art-body { flex: 1; min-width: 0; }
    .art .art-h { font-size: 0.92rem; font-weight: 700; line-height: 1.42; color: var(--ink); }
    .art .art-meta { font-size: 0.78rem; color: var(--ink-soft); margin-top: 3px; }
    .art .art-arrow { color: var(--ink-soft); font-size: 1.05rem; flex: none; }
    .art:hover .art-arrow { color: var(--accent); }
    /* 클릭 가능한 이슈/종목 카드 */
    .event, .pick { cursor: pointer; }

    /* ============ 주식 마인드맵 ============ */
    .mm-card { padding: 18px; position: relative; }
    .mm-back {
      position: absolute; top: 14px; left: 14px; z-index: 2;
      background: var(--surface-2); border: 1px solid var(--line); color: var(--ink);
      font-family: inherit; font-weight: 700; font-size: 0.82rem;
      padding: 8px 14px; border-radius: 999px; cursor: pointer; transition: .15s;
    }
    .mm-back:hover { border-color: var(--accent); color: var(--accent); }
    .mm-wrap { overflow-x: auto; -webkit-overflow-scrolling: touch; perspective: 1500px; perspective-origin: 50% 42%; }
    .mm-stage { animation: mmpop .5s cubic-bezier(.22,.9,.28,1) both; transform-origin: 410px 370px; }
    .mm-stage.mm-out { animation: mmout .22s ease forwards; }
    @keyframes mmpop { from { opacity: 0; transform: scale(.9); } to { opacity: 1; transform: scale(1); } }
    @keyframes mmout { from { opacity: 1; transform: scale(1); } to { opacity: 0; transform: scale(1.04); } }
    .mm-link { transition: opacity .3s ease; }
    .mm-rect3 { fill: url(#mmNodeG); stroke-width: 2; }
    .mm-rect3.up { stroke: var(--up); } .mm-rect3.down { stroke: var(--down); }
    .mm-name { fill: var(--ink-soft); font-size: 9px; font-weight: 600; text-anchor: middle; }
    .mm-svg { width: 100%; min-width: 600px; max-width: 820px; height: auto; display: block; margin: 0 auto;
              transform: rotateX(18deg); transform-style: preserve-3d; transition: transform .3s ease; will-change: transform; }
    .mm-svg text { font-family: var(--font); }
    .mm-link { stroke: var(--line); stroke-width: 1.5; }
    .mm-node { cursor: pointer; filter: url(#mmShadow); }
    .mm-node:hover .mm-rect, .mm-node:hover .mm-rect2, .mm-node:hover .mm-rect3 { filter: brightness(1.35); }
    .mm-rect  { fill: url(#mmNodeG); stroke-width: 2; }
    .mm-rect2 { fill: url(#mmNodeG); stroke-width: 1.5; }
    .mm-rect.up,  .mm-rect2.up   { stroke: var(--up); }
    .mm-rect.down, .mm-rect2.down { stroke: var(--down); }
    .mm-t  { fill: #fff; font-size: 13px; font-weight: 800; text-anchor: middle; }
    .mm-t2 { fill: #fff; font-size: 11px; font-weight: 800; text-anchor: middle; }
    .mm-sub { font-size: 10px; font-weight: 700; text-anchor: middle; }
    .mm-sub.up { fill: var(--up); } .mm-sub.down { fill: var(--down); }
    .mm-center { fill: url(#mmCenterG); }
    .mm-center-t { fill: #fff; font-size: 15px; font-weight: 800; text-anchor: middle; }
    .mm-hint { text-align: center; color: var(--ink-soft); font-size: 0.85rem; margin-top: 12px; }
    .mm-hint b { color: var(--ink); }

    /* ============ 애널리스트 리포트 ============ */
    .journals { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
    .journal { padding: 20px; display: flex; flex-direction: column; gap: 12px; transition: transform .18s, border-color .18s; }
    .journal:hover { transform: translateY(-3px); border-color: rgba(239,62,62,0.4); }
    .j-top { display: flex; align-items: center; gap: 12px; }
    .j-ava {
      width: 46px; height: 46px; border-radius: 50%; flex: none; font-size: 0.8rem;
      display: grid; place-items: center; font-weight: 800; color: #fff;
      background: #fff; overflow: hidden; border: 1px solid var(--line);
    }
    .j-ava img { width: 100%; height: 100%; object-fit: contain; padding: 7px; display: block; }
    /* 로고 로드 실패 시: 기존 티커 배지(빨간 그라데이션)로 폴백 */
    .j-ava.noimg { background: linear-gradient(135deg, var(--accent), #8f1010); border: none; }
    .j-who { flex: 1; min-width: 0; }
    .j-who b { font-size: 0.98rem; font-weight: 800; display: block; letter-spacing: -0.01em; }
    .j-who small { color: var(--ink-soft); font-size: 0.8rem; }
    .rating { font-size: 0.76rem; font-weight: 800; padding: 5px 11px; border-radius: 8px; white-space: nowrap; }
    .rating.buy  { background: var(--up-soft);   color: var(--up); }
    .rating.hold { background: var(--surface-2); color: var(--ink-soft); }
    .rating.sell { background: var(--down-soft); color: var(--down); }
    .j-target { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; }
    .j-target .tk { font-size: 0.95rem; font-weight: 800; }
    .j-target .tp { color: var(--ink-soft); font-size: 0.88rem; }
    .j-target .tp b { color: var(--up); font-weight: 800; }
    .journal p { color: var(--ink-soft); font-size: 0.9rem; flex: 1; }
    .j-link { font-size: 0.86rem; font-weight: 700; color: var(--accent); align-self: flex-start; }
    .j-link:hover { text-decoration: underline; }

    /* ============ 서울 집값 지도 ============ */
    .map-hero {
      position: relative; border-radius: var(--radius); overflow: hidden;
      margin-bottom: 26px; min-height: 260px; display: flex; align-items: flex-end;
      background: #0b1220 url('seoul-home.jpg') center 40% / cover no-repeat;
      box-shadow: var(--shadow); border: 1px solid var(--line);
    }
    .map-hero::after {
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(to top, rgba(8,10,15,0.94), rgba(8,10,15,0.3) 55%, rgba(8,10,15,0.08));
    }
    .map-hero-text { position: relative; z-index: 1; padding: 30px 28px; }
    .mh-eyebrow { color: var(--accent); font-weight: 800; font-size: 0.82rem; letter-spacing: .06em; }
    .map-hero h3 { font-size: clamp(1.35rem, 3.6vw, 2.05rem); font-weight: 800; letter-spacing: -0.02em; margin: 8px 0; color: #fff; }
    .map-hero p { color: rgba(255,255,255,0.84); font-size: 0.98rem; max-width: 580px; }
    @media (max-width: 560px) { .map-hero { min-height: 210px; } }

    /* 업로드 버튼 (배너 공용) */
    .mh-upload {
      position: absolute; top: 14px; right: 14px; z-index: 2; cursor: pointer;
      background: rgba(0,0,0,0.45); border: 1px solid rgba(255,255,255,0.35); color: #fff;
      font-family: inherit; font-weight: 700; font-size: 0.8rem; padding: 7px 12px; border-radius: 999px;
      backdrop-filter: blur(4px); transition: .15s;
    }
    .mh-upload:hover { background: rgba(0,0,0,0.68); border-color: #fff; }

    /* 주식 히어로 배너 (페이지 맨 위) */
    .stock-hero {
      position: relative; border-radius: var(--radius); overflow: hidden; margin-bottom: 26px;
      min-height: 220px; display: flex; align-items: flex-end;
      background: #0b1220 url('stock-top.jpg') center / cover no-repeat;
      border: 1px solid var(--line); box-shadow: var(--shadow);
    }
    .stock-hero::after {
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(to top, rgba(8,10,15,0.6), rgba(8,10,15,0.04) 60%);
    }
    .stock-hero .sh-cap {
      position: relative; z-index: 1; padding: 20px 22px; color: #fff; font-weight: 800;
      font-size: clamp(1.1rem, 3vw, 1.55rem); letter-spacing: -0.02em;
    }
    @media (max-width: 560px) { .stock-hero { min-height: 180px; } }

    .map-card { padding: 24px 22px; }
    .seoul-map {
      display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px;
      max-width: 540px; margin: 0 auto;
    }
    .gu-tile {
      aspect-ratio: 1 / 1; border: 1px solid rgba(255,255,255,0.08); border-radius: 9px;
      cursor: pointer; color: #fff; font-family: inherit;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
      text-align: center; font-size: 0.74rem; font-weight: 800; letter-spacing: -0.02em;
      padding: 2px; line-height: 1.1; transition: transform .12s, box-shadow .12s;
    }
    .gu-tile:hover { transform: scale(1.1); box-shadow: 0 0 0 2px #fff; z-index: 3; }
    .gu-tile small { font-size: 0.62rem; font-weight: 700; opacity: 0.9; margin-top: 2px; }
    .map-legend {
      display: flex; align-items: center; gap: 8px; justify-content: center;
      margin-top: 20px; font-size: 0.8rem; color: var(--ink-soft); flex-wrap: wrap;
    }
    .legend-bar {
      width: 120px; height: 10px; border-radius: 5px; display: inline-block;
      background: linear-gradient(90deg, rgba(239,62,62,0.18), rgba(239,62,62,0.92));
    }
    .legend-note { flex-basis: 100%; text-align: center; margin-top: 4px; }

    .gu-filters { display: flex; flex-wrap: wrap; gap: 8px; margin: 6px 0 16px; }
    .gu-chip {
      font-size: 0.8rem; font-weight: 600; color: var(--ink);
      background: var(--up-soft); border: 1px solid rgba(239,62,62,0.28);
      padding: 6px 12px; border-radius: 999px;
    }
    .gu-count { font-size: 0.85rem; color: var(--ink-soft); margin: -6px 0 16px; text-align: center; }
    .gu-count b { color: var(--accent); font-weight: 800; }
    .gu-stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 8px 0 12px; }
    .gu-stat { background: var(--surface-2); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; }
    .gu-stat .k { font-size: 0.8rem; color: var(--ink-soft); font-weight: 600; }
    .gu-stat .v { font-size: 1.35rem; font-weight: 800; letter-spacing: -0.02em; margin-top: 4px; font-variant-numeric: tabular-nums; }
    .gu-stat .v.hi { color: var(--up); }
    .gu-stat .v.lo { color: var(--down); }
    .gu-dong-title { font-size: 0.92rem; font-weight: 800; margin: 6px 0 10px; }
    .gu-dong-title span { color: var(--ink-soft); font-size: 0.8rem; font-weight: 600; }
    .gu-dongs { display: flex; flex-direction: column; gap: 8px; }
    .gu-dong {
      display: flex; align-items: center; gap: 12px; padding: 13px 14px;
      border: 1px solid var(--line); border-radius: 11px; background: var(--surface-2);
      cursor: pointer; font-family: inherit; text-align: left; transition: .14s;
    }
    .gu-dong:hover { border-color: rgba(3,199,90,0.5); transform: translateY(-2px); }
    .gu-dong .dn { flex: 1; font-size: 0.96rem; font-weight: 700; color: var(--ink); }
    .gu-dong .dp { font-size: 0.92rem; font-weight: 800; color: var(--up); font-variant-numeric: tabular-nums; }
    .gu-dong .da {
      font-size: 0.78rem; font-weight: 800; color: #fff; flex: none;
      background: linear-gradient(135deg, #03c75a, #02a548); padding: 5px 9px; border-radius: 7px;
    }
    @media (max-width: 480px) {
      .gu-tile { font-size: 0.62rem; border-radius: 7px; }
      .gu-tile small { font-size: 0.54rem; }
    }

    /* ============ 요소 2 · 이슈 달력 ============ */
    .tag {
      font-size: 0.72rem; font-weight: 700; padding: 3px 9px; border-radius: 6px;
      background: var(--surface-2); color: var(--ink-soft);
    }
    .tag.hot { background: var(--up-soft); color: var(--accent); }

    .calendar { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; align-items: start; }
    .day { display: flex; flex-direction: column; overflow: hidden; }
    .day-head {
      display: flex; align-items: baseline; justify-content: space-between;
      padding: 12px 14px; border-bottom: 1px solid var(--line); background: var(--surface-2);
    }
    .day-head .dow { font-size: 0.92rem; font-weight: 800; letter-spacing: -0.01em; }
    .day-head .date { font-size: 0.78rem; color: var(--ink-soft); font-weight: 600; }
    .day.today { border-color: rgba(239,62,62,0.5); }
    .day.today .day-head { background: var(--up-soft); }
    .day.today .dow { color: var(--accent); }
    .day.closed .day-head { background: var(--surface-2); }

    .day-body { padding: 10px; display: flex; flex-direction: column; gap: 10px; min-height: 96px; }
    .event {
      background: var(--surface-2); border: 1px solid var(--line); border-left: 3px solid var(--line);
      border-radius: 10px; padding: 11px 12px; display: flex; flex-direction: column; gap: 6px;
      transition: transform .16s, border-color .16s;
    }
    .event:hover { transform: translateY(-2px); border-color: rgba(239,62,62,0.4); }
    .event.up   { border-left-color: var(--up); }
    .event.down { border-left-color: var(--down); }
    .event .tags { display: flex; gap: 5px; flex-wrap: wrap; }
    .event h3 { font-size: 0.92rem; font-weight: 700; letter-spacing: -0.01em; line-height: 1.38; }
    .event p { color: var(--ink-soft); font-size: 0.82rem; line-height: 1.5; }
    .event .impact { font-size: 0.78rem; font-weight: 700; margin-top: 1px; }
    .day-empty { color: var(--ink-soft); font-size: 0.82rem; text-align: center; padding: 22px 6px; opacity: .7; }
    .day-empty.holiday { font-weight: 700; }

    /* ============ 요소 3 · 추천 종목 ============ */
    .picks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .pick { padding: 20px; transition: transform .18s, border-color .18s; }
    .pick:hover { transform: translateY(-4px); border-color: rgba(239,62,62,0.4); }
    .pick .top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .pick .ticker { display: flex; align-items: center; gap: 10px; }
    .pick .badge {
      width: 40px; height: 40px; border-radius: 11px; flex: none;
      display: grid; place-items: center; font-weight: 800; font-size: 0.82rem; color: #fff;
      background: linear-gradient(135deg, var(--accent), #8f1010);
    }
    .pick .ticker b { font-size: 1.05rem; font-weight: 800; letter-spacing: -0.01em; display: block; }
    .pick .ticker small { color: var(--ink-soft); font-size: 0.8rem; }
    .pick .chg { font-size: 0.95rem; font-weight: 800; }

    /* 미니 스파크라인 */
    .spark { width: 100%; height: 46px; display: block; margin: 6px 0 12px; }
    .pick .why { font-size: 0.86rem; color: var(--ink-soft); }
    .pick .sector-tag { display: inline-block; margin-top: 12px; font-size: 0.76rem; font-weight: 600; color: var(--accent); background: var(--up-soft); padding: 3px 10px; border-radius: 999px; }

    /* ============ 푸터 ============ */
    footer { border-top: 1px solid var(--line); padding: 28px 0 40px; margin-top: 20px; }
    .foot { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
    .foot .logo { font-size: 1rem; }
    .disclaimer { color: var(--ink-soft); font-size: 0.78rem; margin-top: 16px; line-height: 1.6; }

    /* 등장 애니메이션 */
    .reveal { opacity: 0; transform: translateY(20px); transition: opacity .55s ease, transform .55s ease; }
    .reveal.in { opacity: 1; transform: none; }

    /* ============ 모바일 ============ */
    @media (max-width: 820px) {
      .picks { grid-template-columns: 1fr; }
      /* 애널리스트 카드는 한 줄에 2개 유지 (한 눈에 보기) */
      .index-strip { grid-template-columns: repeat(2, 1fr); }
      /* 달력: 가로 스크롤로 5일 유지 */
      .calendar {
        grid-auto-flow: column; grid-template-columns: none;
        grid-auto-columns: 78%; overflow-x: auto; scroll-snap-type: x mandatory;
        padding-bottom: 8px; -webkit-overflow-scrolling: touch;
      }
      .day { scroll-snap-align: start; }
      .day-body { min-height: 0; }
    }
    @media (max-width: 560px) {
      .nav-links { display: none; }
      .bar-row { grid-template-columns: 88px 1fr 54px; gap: 8px; }
      .bar-row .label { font-size: 0.82rem; }
    }
    /* 애널리스트 카드는 항상 한 줄에 2개. 아주 좁은 화면(폰)에서만 1개 */
    @media (max-width: 380px) {
      .journals { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <!-- ============ 헤더 ============ -->
  <header>
    <div class="wrap nav">
      <a href="#" class="logo"><span class="dot">🏠</span> 10만원으로 내집마련</a>
      <nav class="nav-links">
        <a href="#sectors">섹터</a>
        <a href="#mindmap-sec">마인드맵</a>
        <a href="#issues">이번주 이슈</a>
        <a href="#picks">주목 종목</a>
        <a href="#journals">애널리스트</a>
        <a href="#map">집값 지도</a>
      </nav>
      <span class="week-pill">2026년 7월 2주차 · 7/6~7/10</span>
    </div>
  </header>

  <div class="demo-note" id="demoNote" hidden>
    ⚠️ 실시간 시세 연결에 실패해 일부 수치는 <b>예시(가상) 데이터</b>입니다 · 새로고침하면 실제 시세가 들어올 수 있어요
  </div>

  <!-- ============ 히어로 ============ -->
  <section class="hero">
    <div class="wrap reveal">
      <div class="stock-hero" id="stockHero">
        <span class="sh-cap">🇺🇸 미국 3대 지수, 이번 주도 우상향</span>
        <label class="mh-upload" title="배너 사진 넣기">🖼 사진 넣기
          <input type="file" id="stockFile" accept="image/*" hidden />
        </label>
      </div>
      <div class="eyebrow">WEEKLY US STOCK REPORT</div>
      <h1>이번 주 미국 시장,<br />한 눈에 정리해 드려요</h1>
      <p>매주 섹터 흐름과 주요 이슈, 주목할 종목까지. 복잡한 미국 주식, 주린이도 5분이면 흐름을 잡을 수 있어요.</p>

      <div class="index-strip" id="indexStrip"><!-- 실시간 데이터로 채워집니다 --></div>
    </div>
  </section>

  <!-- ============ 주식 차트 검색 ============ -->
  <section class="block" id="search">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>🔎 종목 차트 검색</h2>
        <span class="sub">티커 또는 종목명을 입력해 최근 주가 흐름을 확인하세요</span>
      </div>

      <div class="card search-card reveal">
        <form class="search-form" id="searchForm" autocomplete="off">
          <input type="text" id="searchInput" class="search-input"
                 placeholder="예: AAPL, TSLA, 엔비디아 …" aria-label="종목 검색" />
          <button type="submit" class="search-btn">검색</button>
        </form>
        <div class="quick-tickers" id="quickTickers">
          <span class="q-label">인기 종목</span>
          <button type="button" data-t="AAPL">AAPL</button>
          <button type="button" data-t="TSLA">TSLA</button>
          <button type="button" data-t="NVDA">NVDA</button>
          <button type="button" data-t="005930">삼성전자</button>
          <button type="button" data-t="000660">SK하이닉스</button>
        </div>

        <div class="chart-result" id="chartResult" hidden>
          <div class="cr-head">
            <div class="cr-info">
              <b id="crTicker">—</b>
              <small id="crName">—</small>
            </div>
            <div class="cr-price">
              <span id="crPrice">$0.00</span>
              <span id="crChg" class="chg-tag">0.00%</span>
            </div>
          </div>
          <div class="cr-tip" id="crTip" hidden></div>
          <svg id="crChart" class="cr-chart"></svg>
          <div class="cr-range" id="crRange">
            <button type="button" data-r="1mo">1개월</button>
            <button type="button" data-r="3mo">3개월</button>
            <button type="button" data-r="6mo" class="active">6개월</button>
            <button type="button" data-r="1y">1년</button>
          </div>
          <div class="cr-stats" id="crStats"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ 요소 1 · 섹터 상승률 ============ -->
  <section class="block" id="sectors">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>📊 섹터별 당일 등락률</h2>
        <span class="sub">섹터 대표 ETF(SMH·XLK·BITO·ITA·NLR·XAR·XBI·LIT) 당일 등락률 · Finnhub 실시간</span>
      </div>
      <div class="card sector-chart reveal" id="sectorChart">
        <!-- JS로 채워집니다 -->
      </div>
    </div>
  </section>

  <!-- ============ 주식 마인드맵 ============ -->
  <section class="block" id="mindmap-sec">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>🧠 주식 마인드맵</h2>
        <span class="sub">미국 시장 → 섹터 → 대표 종목 · 노드를 눌러보세요</span>
      </div>
      <div class="card mm-card reveal">
        <button id="mmBack" class="mm-back" hidden>← 전체 시장</button>
        <div class="mm-wrap">
          <svg class="mm-svg" id="mindmap" viewBox="0 0 820 740" preserveAspectRatio="xMidYMid meet"></svg>
        </div>
        <p class="mm-hint" id="mmHint">🟥 상승 · 🟦 하락 · <b>섹터</b>를 누르면 중앙으로 확장돼요</p>
      </div>
    </div>
  </section>

  <!-- ============ 요소 2 · 이번주 이슈 ============ -->
  <section class="block" id="issues">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>📰 이번 주 시장 요약</h2>
        <span class="sub">2026년 7월 1~2주차 핵심 이슈 요약 · 카드를 누르면 원문(출처)으로 이동</span>
      </div>

      <div class="newsfeed reveal" id="newsFeed"><!-- 실제 뉴스로 채워집니다 --></div>
    </div>
  </section>

  <!-- ============ 요소 3 · 주목 종목 ============ -->
  <section class="block" id="picks">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>🎯 주요 관심 종목</h2>
        <span class="sub">실시간 시세(Finnhub) · 카드를 누르면 당일 시세와 관련 실제 뉴스가 열려요</span>
      </div>
      <div class="picks">
        <article class="card pick reveal" data-sym="NVDA" data-detail="NVDA">
          <div class="top">
            <div class="ticker">
              <span class="badge">NVDA</span>
              <div><b>엔비디아</b><small>NVIDIA Corp.</small></div>
            </div>
            <span class="chg">…</span>
          </div>
          <div class="pick-price"></div>
          <p class="why">카드를 누르면 실시간 시세와 관련 실제 뉴스를 볼 수 있어요.</p>
          <span class="sector-tag">반도체 · AI</span>
        </article>

        <article class="card pick reveal" data-sym="COIN" data-detail="COIN">
          <div class="top">
            <div class="ticker">
              <span class="badge">COIN</span>
              <div><b>코인베이스</b><small>Coinbase Global</small></div>
            </div>
            <span class="chg">…</span>
          </div>
          <div class="pick-price"></div>
          <p class="why">카드를 누르면 실시간 시세와 관련 실제 뉴스를 볼 수 있어요.</p>
          <span class="sector-tag">코인 · 가상자산</span>
        </article>

        <article class="card pick reveal" data-sym="CEG" data-detail="CEG">
          <div class="top">
            <div class="ticker">
              <span class="badge">CEG</span>
              <div><b>컨스텔레이션</b><small>Constellation Energy</small></div>
            </div>
            <span class="chg">…</span>
          </div>
          <div class="pick-price"></div>
          <p class="why">카드를 누르면 실시간 시세와 관련 실제 뉴스를 볼 수 있어요.</p>
          <span class="sector-tag">원전 · 에너지</span>
        </article>
      </div>
    </div>
  </section>

  <!-- ============ 애널리스트 리포트 ============ -->
  <section class="block" id="journals">
    <div class="wrap">
      <div class="sec-head reveal">
        <h2>📑 애널리스트 투자의견</h2>
        <span class="sub">각 종목의 <b>실제</b> 월가 투자의견·목표주가 페이지로 연결돼요 (Yahoo Finance)</span>
      </div>

      <div class="journals" id="journals"><!-- 실제 링크 카드로 채워집니다 --></div>
    </div>
  </section>

  <!-- ============ 서울 구별 집값 지도 ============ -->
  <section class="block" id="map">
    <div class="wrap">
      <div class="map-hero reveal" id="mapHero">
        <div class="map-hero-text">
          <span class="mh-eyebrow">MY HOME</span>
          <h3>한강뷰 내집마련, 막연한 꿈이 아니에요</h3>
          <p>매주 투자로 차근차근. 서울 어디에 내 집을 마련할지, 지금 지도에서 확인해 보세요.</p>
        </div>
        <label class="mh-upload" title="배너 사진 넣기">🖼 사진 넣기
          <input type="file" id="heroFile" accept="image/*" hidden />
        </label>
      </div>
      <div class="sec-head reveal">
        <h2>🗺️ 서울 아파트 지도</h2>
        <span class="sub">구 → 동 선택 시, 조건(20~40평·700세대+·초품아·역세권)이 적용된 네이버 부동산 실제 매물로 이동</span>
      </div>
      <div class="card map-card reveal">
        <div class="seoul-map" id="seoulMap"></div>
        <div class="map-legend">
          <span>낮음</span><i class="legend-bar"></i><span>높음</span>
          <span class="legend-note">상대 가격대(자치구 평균 매매가 순위, KB·부동산원 기준) · 구를 클릭하면 동별 네이버 부동산 링크가 열려요</span>
        </div>
      </div>
    </div>
  </section>

  <!-- ============ 지수 차트 모달 ============ -->
  <div class="modal" id="idxModal" role="dialog" aria-modal="true" aria-label="지수 차트">
    <div class="modal-panel">
      <div class="modal-head">
        <div>
          <div class="m-name" id="mName">—</div>
          <div class="m-sub" id="mSub">최근 지수 흐름 (데모 데이터)</div>
        </div>
        <div style="display:flex; align-items:flex-start;">
          <div class="m-price">
            <div class="m-val" id="mVal">—</div>
            <span class="chg-tag" id="mChg">0.00%</span>
          </div>
          <button class="m-close" id="mClose" aria-label="닫기">✕</button>
        </div>
      </div>
      <div class="cr-tip" id="mTip" hidden></div>
      <svg class="m-chart" id="mChart" viewBox="0 0 760 300" preserveAspectRatio="none"></svg>
      <div class="m-range" id="mRange">
        <button type="button" data-r="30">1M</button>
        <button type="button" data-r="90" class="active">3M</button>
        <button type="button" data-r="180">6M</button>
        <button type="button" data-r="250">1Y</button>
      </div>
    </div>
  </div>

  <!-- ============ 섹터 대표주 모달 ============ -->
  <div class="modal" id="secModal" role="dialog" aria-modal="true" aria-label="섹터 대표 종목">
    <div class="modal-panel">
      <div class="modal-head">
        <div>
          <div class="m-name" id="secName">섹터</div>
          <div class="m-sub">대표 종목 · 주간 흐름 (데모 데이터)</div>
        </div>
        <div style="display:flex; align-items:flex-start;">
          <div class="m-price"><span class="chg-tag" id="secPct">0%</span></div>
          <button class="m-close" id="secClose" aria-label="닫기">✕</button>
        </div>
      </div>

      <div class="sec-chart-info">
        <b id="secStkTicker">—</b>
        <small id="secStkName">—</small>
        <span class="chg-tag" id="secStkChg"></span>
      </div>
      <div class="cr-tip" id="secTip" hidden></div>
      <svg class="m-chart" id="secChart" viewBox="0 0 760 300" preserveAspectRatio="none"></svg>

      <div class="sec-stocklist" id="secStockList"></div>
    </div>
  </div>

  <!-- ============ 이슈/종목 상세 모달 (차트 + 기사) ============ -->
  <div class="modal" id="detailModal" role="dialog" aria-modal="true" aria-label="상세 정보">
    <div class="modal-panel">
      <div class="modal-head">
        <div>
          <div class="m-name" id="dName">—</div>
          <div class="m-sub">관련 종목 차트 · 기사 (데모 데이터)</div>
        </div>
        <div style="display:flex; align-items:flex-start;">
          <div class="m-price">
            <div class="m-val" id="dVal">—</div>
            <span class="chg-tag" id="dChg"></span>
          </div>
          <button class="m-close" id="dClose" aria-label="닫기">✕</button>
        </div>
      </div>

      <div class="sec-chart-info">
        <b id="dTicker">—</b>
        <small id="dTname">—</small>
      </div>
      <div class="cr-tip" id="dTip" hidden></div>
      <svg class="m-chart" id="dChart" viewBox="0 0 760 300" preserveAspectRatio="none"></svg>

      <div id="dArticles"></div>
    </div>
  </div>

  <!-- ============ 구별 집값 모달 ============ -->
  <div class="modal" id="guModal" role="dialog" aria-modal="true" aria-label="구별 집값">
    <div class="modal-panel">
      <div class="modal-head">
        <div>
          <div class="m-name" id="guName">—</div>
          <div class="m-sub">동을 선택하면 네이버 부동산 실제 매물·시세로 이동합니다</div>
        </div>
        <button class="m-close" id="guClose" aria-label="닫기">✕</button>
      </div>
      <div class="gu-filters">
        <span class="gu-chip">📐 20~40평</span>
        <span class="gu-chip">🏢 700세대 이상</span>
        <span class="gu-chip">🏫 초등학교 도보 10분</span>
        <span class="gu-chip">🚇 지하철 도보 15분</span>
      </div>
      <div class="gu-stats" id="guStats"></div>
      <div class="gu-count" id="guCount"></div>
      <div class="gu-dong-title">🏘️ 동별 시세 <span>· 동을 누르면 네이버 부동산으로 이동</span></div>
      <div class="gu-dongs" id="guDongs"></div>
    </div>
  </div>

  <!-- ============ 푸터 ============ -->
  <footer>
    <div class="wrap">
      <div class="foot">
        <a href="#" class="logo"><span class="dot">🏠</span> 10만원으로 내집마련</a>
        <nav class="nav-links" style="display:flex;">
          <a href="#sectors">섹터</a>
          <a href="#issues">이슈</a>
          <a href="#picks">종목</a>
        </nav>
      </div>
      <p class="disclaimer">
        ※ 본 리포트는 정보 제공을 목적으로 하며, 특정 종목의 매수·매도를 권유하지 않습니다.
        모든 수치는 예시 데이터이며 실제 시장과 다를 수 있습니다. 투자에 대한 최종 책임은 투자자 본인에게 있습니다.<br />
        © 2026 10만원으로 내집마련. 미국 주식 주간 리포트.
      </p>
    </div>
  </footer>

  <script>
    /* =====================================================================
       실데이터 계층 — Finnhub 실시간 시세 (무료 플랜: 실시간 quote + 뉴스)
       ※ 지어낸 값 없음. 모든 숫자는 API 응답에서 옵니다.
       ===================================================================== */
    // 키 불필요 — 공개 CORS 프록시를 통해 야후 파이낸스 실시세를 가져옵니다.
    // (야후는 한국 주식 005930.KS, 지수 ^GSPC 등도 실제로 제공)
    const FH_KEY = true;                 // 게이트 호환용(키 개념 없음)
    const qCache = new Map();
    // 여러 공개 프록시에 "동시에" 요청 → 가장 빨리 온 응답 사용 (+8초 타임아웃)
    // 순차 대기가 없어져서 체감 속도가 크게 빨라집니다.
    function withTimeout(ms) { return new Promise((_, rej) => setTimeout(() => rej(new Error('t')), ms)); }
    async function proxyJson(url) {
      const enc = encodeURIComponent(url);
      const attempts = [
        fetch('https://api.allorigins.win/get?url=' + enc).then(r => r.json()).then(j => { if (j && j.contents) return JSON.parse(j.contents); throw 0; }),
        fetch('https://corsproxy.io/?url=' + enc).then(r => { if (!r.ok) throw 0; return r.json(); }),
        fetch('https://api.allorigins.win/raw?url=' + enc).then(r => { if (!r.ok) throw 0; return r.json(); }),
      ];
      try { return await Promise.race([Promise.any(attempts), withTimeout(8000)]); }
      catch (_) { return null; }
    }
    /* --- 실시간 실패 시 대체할 예시(가상) 데이터 --- */
    let DEMO_USED = false;
    function dSeed(str) { let h = 0; for (let i = 0; i < str.length; i++) h = (h * 31 + str.charCodeAt(i)) >>> 0; return h; }
    function dRng(seed) { let s = seed || 1; return () => { s = (s * 1103515245 + 12345) & 0x7fffffff; return s / 0x7fffffff; }; }
    function demoQuote(sym) {
      const isKR = /\.K[SQ]$/i.test(sym) || /^\d{6}/.test(sym) || /[가-힣]/.test(sym);
      const rng = dRng(dSeed(sym));
      const rnd = 2;
      const base = isKR ? Math.round((15000 + rng() * 285000) / 100) * 100 : +(30 + rng() * 570).toFixed(rnd);
      const dp = +((rng() - 0.45) * 5).toFixed(2);            // 대략 -2.25% ~ +2.75%
      const c = base;
      const pc = isKR ? Math.round(c / (1 + dp / 100)) : +(c / (1 + dp / 100)).toFixed(rnd);
      const o = isKR ? Math.round(pc * (1 + (rng() - 0.5) * 0.01)) : +(pc * (1 + (rng() - 0.5) * 0.01)).toFixed(rnd);
      const h = isKR ? Math.round(Math.max(c, o) * (1 + rng() * 0.015)) : +(Math.max(c, o) * (1 + rng() * 0.015)).toFixed(rnd);
      const l = isKR ? Math.round(Math.min(c, o) * (1 - rng() * 0.015)) : +(Math.min(c, o) * (1 - rng() * 0.015)).toFixed(rnd);
      return { c, pc, o, h, l, d: +(c - pc).toFixed(isKR ? 0 : rnd), dp, currency: isKR ? 'KRW' : 'USD', name: sym.replace(/\.K[SQ]$/i, ''), demo: true };
    }
    function showDemoNote() {
      DEMO_USED = true;
      const el = document.getElementById('demoNote');
      if (el) el.hidden = false;
    }

    // 과거 시세(라인 차트용). 실패하면 예시 시계열로 대체.
    const histCache = new Map();
    function demoHistory(sym, days) {
      const isKR = /\.K[SQ]$/i.test(sym) || /^\d{6}/.test(sym) || /[가-힣]/.test(sym);
      const rng = dRng(dSeed(sym) + days);
      const base = isKR ? Math.round((15000 + rng() * 285000) / 100) * 100 : +(30 + rng() * 570).toFixed(2);
      let price = base * (0.8 + rng() * 0.15); const out = []; const now = Date.now();
      for (let i = days - 1; i >= 0; i--) {
        price = Math.max(base * 0.3, price + (base - price) * 0.01 + (rng() - 0.5) * base * 0.03);
        const c = isKR ? Math.round(price) : +price.toFixed(2);
        const h = isKR ? Math.round(c * (1 + rng() * 0.02)) : +(c * (1 + rng() * 0.02)).toFixed(2);
        const l = isKR ? Math.round(c * (1 - rng() * 0.02)) : +(c * (1 - rng() * 0.02)).toFixed(2);
        out.push({ t: now - i * 86400000, o: c, h: Math.max(h, c), l: Math.min(l, c), c });
      }
      return out;
    }
    async function fhHistory(sym, range, interval) {
      range = range || '6mo'; interval = interval || '1d';
      const ck = sym + '|' + range;
      if (histCache.has(ck)) return histCache.get(ck);
      const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(sym)}?range=${range}&interval=${interval}`;
      const j = await proxyJson(url);
      const res = j && j.chart && j.chart.result && j.chart.result[0];
      const ts = res && res.timestamp;
      const ind = res && res.indicators && res.indicators.quote && res.indicators.quote[0];
      const meta = res && res.meta;
      let result;
      if (ts && ind && ind.close) {
        const out = [];
        for (let i = 0; i < ts.length; i++) {
          const c = ind.close[i]; if (c == null) continue;
          out.push({ t: ts[i] * 1000, o: ind.open[i] != null ? ind.open[i] : c, h: ind.high[i] != null ? ind.high[i] : c, l: ind.low[i] != null ? ind.low[i] : c, c });
        }
        if (out.length >= 2) result = { hist: out, currency: (meta && meta.currency) || 'USD', name: (meta && (meta.longName || meta.shortName)) || sym, demo: false };
      }
      if (!result) {
        showDemoNote();
        const isKR = /\.K[SQ]$/i.test(sym) || /^\d{6}/.test(sym) || /[가-힣]/.test(sym);
        const days = range === '1mo' ? 22 : range === '3mo' ? 66 : range === '1y' ? 252 : 126;
        result = { hist: demoHistory(sym, days), currency: isKR ? 'KRW' : 'USD', name: sym.replace(/\.K[SQ]$/i, ''), demo: true };
      }
      histCache.set(ck, result);
      return result;
    }

    // 라인 차트 그리기 (+ 선택적 호버 툴팁). tipEl 없으면 툴팁 생략.
    function renderLineChart(svg, tipEl, hist, currency) {
      const W = 640, H = 240, pad = 12;
      const closes = hist.map(d => d.c);
      const min = Math.min(...closes), max = Math.max(...closes), span = (max - min) || 1, n = hist.length;
      const X = i => pad + i / (n - 1) * (W - 2 * pad);
      const Y = v => pad + (1 - (v - min) / span) * (H - 2 * pad);
      const up = closes[n - 1] >= closes[0];
      const line = hist.map((d, i) => `${X(i).toFixed(1)},${Y(d.c).toFixed(1)}`).join(' ');
      const area = `${X(0).toFixed(1)},${H} ${line} ${X(n - 1).toFixed(1)},${H}`;
      const col = up ? 'var(--up)' : 'var(--down)', stop = up ? '239,62,62' : '47,129,247';
      const gid = 'cg' + Math.floor(X(0));
      svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
      svg.setAttribute('preserveAspectRatio', 'none');
      svg.innerHTML =
        `<defs><linearGradient id="${gid}" x1="0" y1="0" x2="0" y2="1">
           <stop offset="0%" stop-color="rgba(${stop},0.35)"/><stop offset="100%" stop-color="rgba(${stop},0)"/></linearGradient></defs>
         <polygon points="${area}" fill="url(#${gid})"/>
         <polyline points="${line}" fill="none" stroke="${col}" stroke-width="2.2" stroke-linejoin="round" stroke-linecap="round"/>
         <line class="cr-cross" x1="0" y1="0" x2="0" y2="${H}" style="display:none"/>
         <circle class="cr-dot" r="4" style="display:none"/>`;
      if (!tipEl) { svg.onmousemove = null; svg.onmouseleave = null; return; }
      const ln = svg.querySelector('.cr-cross'), dot = svg.querySelector('.cr-dot');
      svg.onmousemove = (e) => {
        const r = svg.getBoundingClientRect();
        let idx = Math.round((e.clientX - r.left) / r.width * (n - 1)); idx = Math.max(0, Math.min(n - 1, idx));
        const d = hist[idx], xx = X(idx), yy = Y(d.c);
        ln.setAttribute('x1', xx); ln.setAttribute('x2', xx); ln.style.display = '';
        dot.setAttribute('cx', xx); dot.setAttribute('cy', yy); dot.style.display = '';
        const dt = new Date(d.t);
        tipEl.innerHTML =
          `<div class="cr-tip-date">${dt.getFullYear()}.${String(dt.getMonth()+1).padStart(2,'0')}.${String(dt.getDate()).padStart(2,'0')}</div>
           <div class="cr-row"><span>고가</span><b class="up">${money(d.h, currency)}</b></div>
           <div class="cr-row"><span>저가</span><b class="down">${money(d.l, currency)}</b></div>
           <div class="cr-row"><span>종가</span><b>${money(d.c, currency)}</b></div>`;
        const pr = svg.parentElement.getBoundingClientRect();
        let left = e.clientX - pr.left; left = Math.max(70, Math.min(pr.width - 70, left));
        let top = e.clientY - pr.top - 76; if (top < 4) top = e.clientY - pr.top + 18;
        tipEl.style.left = left + 'px'; tipEl.style.top = top + 'px'; tipEl.hidden = false;
      };
      svg.onmouseleave = () => { tipEl.hidden = true; ln.style.display = 'none'; dot.style.display = 'none'; };
    }

    // 야후 차트 → 시세 {c,o,h,l,pc,d,dp,currency,name}. 실패하면 예시 데이터로 대체.
    async function fhQuote(sym) {
      if (qCache.has(sym)) return qCache.get(sym);
      const url = `https://query1.finance.yahoo.com/v8/finance/chart/${encodeURIComponent(sym)}?range=1d&interval=1d`;
      const j = await proxyJson(url);
      const res = j && j.chart && j.chart.result && j.chart.result[0];
      const m = res && res.meta;
      if (!m || typeof m.regularMarketPrice !== 'number') {
        const dq = demoQuote(sym); qCache.set(sym, dq); showDemoNote(); return dq;
      }
      // 당일 시가는 meta에 없어 indicators에서 보완
      const ind = res.indicators && res.indicators.quote && res.indicators.quote[0];
      const firstOf = arr => Array.isArray(arr) ? arr.find(v => typeof v === 'number') : null;
      const c = m.regularMarketPrice;
      const pc = (m.chartPreviousClose != null ? m.chartPreviousClose : (m.previousClose != null ? m.previousClose : c));
      const o = (ind && firstOf(ind.open) != null) ? firstOf(ind.open) : c;
      const h = (m.regularMarketDayHigh != null ? m.regularMarketDayHigh : (ind && firstOf(ind.high)) ) || c;
      const l = (m.regularMarketDayLow != null ? m.regularMarketDayLow : (ind && firstOf(ind.low)) ) || c;
      const q = {
        c, pc, o, h, l, d: c - pc, dp: pc ? (c - pc) / pc * 100 : 0,
        currency: (m.currency || 'USD'), name: (m.longName || m.shortName || sym),
      };
      qCache.set(sym, q); return q;
    }
    async function fhProfile(sym) { const q = await fhQuote(sym); return q ? { name: q.name, currency: q.currency } : null; }

    // 포맷 도우미
    const fmtUsd = v => '$' + v.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    const money = (v, cur) => cur === 'KRW' ? '₩' + Math.round(v).toLocaleString('ko-KR')
      : (cur && cur !== 'USD' ? v.toLocaleString('en-US', { maximumFractionDigits: 2 }) + ' ' + cur : fmtUsd(v));
    const pctTxt = dp => (dp >= 0 ? '▲ +' : '▼ ') + Math.abs(dp).toFixed(2) + '%';
    const keyNeeded = what => `<div class="need-key">${what} 데이터를 불러오는 중…</div>`;
    const quoteUrl = t => 'https://finance.yahoo.com/quote/' + encodeURIComponent(t);

    /* ============ 섹터 (실시간 ETF 등락률) ============ */
    const SECTORS = [
      { name: '반도체',    etf: 'SMH', stocks: [{t:'NVDA',n:'엔비디아'},{t:'AMD',n:'AMD'},{t:'AVGO',n:'브로드컴'},{t:'TSM',n:'TSMC'}] },
      { name: 'AI·빅테크', etf: 'XLK', stocks: [{t:'MSFT',n:'마이크로소프트'},{t:'META',n:'메타'},{t:'GOOGL',n:'알파벳'},{t:'PLTR',n:'팔란티어'}] },
      { name: '코인',      etf: 'BITO',stocks: [{t:'COIN',n:'코인베이스'},{t:'MSTR',n:'마이크로스트래티지'},{t:'MARA',n:'마라홀딩스'}] },
      { name: '우주·항공', etf: 'ITA', stocks: [{t:'RKLB',n:'로켓랩'},{t:'BA',n:'보잉'},{t:'LMT',n:'록히드마틴'}] },
      { name: '원전',      etf: 'NLR', stocks: [{t:'CEG',n:'컨스텔레이션'},{t:'SMR',n:'뉴스케일'},{t:'VST',n:'비스트라'}] },
      { name: '방산',      etf: 'XAR', stocks: [{t:'LMT',n:'록히드마틴'},{t:'RTX',n:'RTX'},{t:'NOC',n:'노스롭그루먼'}] },
      { name: '바이오',    etf: 'XBI', stocks: [{t:'LLY',n:'일라이릴리'},{t:'PFE',n:'화이자'},{t:'MRNA',n:'모더나'}] },
      { name: '2차전지',   etf: 'LIT', stocks: [{t:'TSLA',n:'테슬라'},{t:'ALB',n:'앨버말'},{t:'QS',n:'퀀텀스케이프'}] },
    ];
    // 실시간 값으로 채워짐: name → { etf, pct, stocks:[{t,n,chg}] }
    const SECTOR_STOCKS = {};
    SECTORS.forEach(s => { SECTOR_STOCKS[s.name] = { etf: s.etf, pct: null, stocks: s.stocks.map(x => ({ ...x, chg: null })) }; });

    const sectorChartEl = document.getElementById('sectorChart');
    function renderSectorBars() {
      // 8개 섹터 항상 표시 (데이터 없으면 '…', 있으면 값 큰 순으로 정렬)
      const rows = SECTORS.map(s => ({ name: s.name, pct: SECTOR_STOCKS[s.name].pct }));
      const known = rows.filter(r => r.pct != null);
      const maxAbs = Math.max(1, ...known.map(r => Math.abs(r.pct)));
      rows.sort((a, b) => (b.pct == null ? -1e9 : b.pct) - (a.pct == null ? -1e9 : a.pct));
      sectorChartEl.innerHTML = rows.map(r => {
        if (r.pct == null) {
          return `<div class="bar-row clickable" data-sector="${r.name}" title="${r.name} 대표 종목 보기">
            <span class="label">${r.name}</span>
            <div class="bar-track"><span class="bar-mid"></span></div>
            <span class="pct">…</span></div>`;
        }
        const pos = r.pct >= 0, w = (Math.abs(r.pct) / maxAbs) * 50;
        return `<div class="bar-row clickable" data-sector="${r.name}" title="${r.name} 대표 종목 보기">
          <span class="label">${r.name}</span>
          <div class="bar-track"><span class="bar-mid"></span>
            <span class="bar-fill ${pos?'pos':'neg'}" data-w="${w.toFixed(1)}" style="width:${w.toFixed(1)}%"></span></div>
          <span class="pct ${pos?'up':'down'}">${pos?'+':''}${r.pct.toFixed(2)}%</span>
        </div>`;
      }).join('');
    }
    async function refreshSectors() {
      renderSectorBars();  // 8개 섹터 골격 즉시 표시
      await Promise.all(SECTORS.map(async s => { const q = await fhQuote(s.etf); SECTOR_STOCKS[s.name].pct = q ? q.dp : null; }));
      renderSectorBars();
      if (typeof mmRender === 'function') mmRender();
    }
    // 특정 섹터의 대표 종목 등락률을 필요할 때만 로드 (프록시 부하 감소)
    async function loadSectorStocks(name) {
      const d = SECTOR_STOCKS[name]; if (!d) return;
      await Promise.all(d.stocks.map(async st => { if (st.chg == null) { const q = await fhQuote(st.t); st.chg = q ? q.dp : null; } }));
    }

    /* ============ 지수 (실시간 ETF 프록시) ============ */
    const INDEX_PROXIES = [
      { sym: 'SPY',  label: 'S&P 500',   sub: 'SPY ETF' },
      { sym: 'QQQ',  label: '나스닥100',  sub: 'QQQ ETF' },
      { sym: 'DIA',  label: '다우존스',   sub: 'DIA ETF' },
      { sym: 'VIXY', label: '변동성(VIX)', sub: 'VIXY ETF' },
    ];
    const indexStripEl = document.getElementById('indexStrip');
    async function refreshIndex() {
      if (!FH_KEY) { indexStripEl.innerHTML = keyNeeded('실시간 지수(ETF)'); return; }
      const qs = await Promise.all(INDEX_PROXIES.map(p => fhQuote(p.sym)));
      indexStripEl.innerHTML = INDEX_PROXIES.map((p, i) => {
        const q = qs[i];
        if (!q) return `<div class="idx"><div class="name">${p.label} <span class="idx-sub">${p.sub}</span></div><div class="val">—</div><div class="chg">데이터 없음</div></div>`;
        const up = q.dp >= 0;
        return `<button class="idx" type="button" data-symbol="${p.sym}" data-label="${p.label} (${p.sub})">
          <div class="name">${p.label} <span class="idx-sub">${p.sub}</span></div>
          <div class="val">${fmtUsd(q.c)}</div>
          <div class="chg ${up?'up':'down'}">${pctTxt(q.dp)}</div>
          <span class="idx-hint">상세 →</span>
        </button>`;
      }).join('');
    }

    /* ============ 주목 종목 (실시간 시세) ============ */
    async function refreshPicks() {
      const cards = [...document.querySelectorAll('.pick')];
      await Promise.all(cards.map(async card => {
        const t = card.dataset.sym;
        const chgEl = card.querySelector('.chg');
        const priceEl = card.querySelector('.pick-price');
        if (!FH_KEY) { chgEl.textContent = '키 필요'; chgEl.className = 'chg'; if (priceEl) priceEl.textContent = ''; return; }
        const q = await fhQuote(t);
        if (!q) { chgEl.textContent = '—'; chgEl.className = 'chg'; return; }
        const up = q.dp >= 0;
        chgEl.textContent = (up ? '+' : '') + q.dp.toFixed(2) + '%';
        chgEl.className = 'chg ' + (up ? 'up' : 'down');
        if (priceEl) priceEl.textContent = fmtUsd(q.c);
      }));
    }

    /* ============ 종목 검색 (미국=Finnhub 실시간 / 한국=네이버 금융 링크) ============ */
    const chartResult = document.getElementById('chartResult');
    const crStats = document.getElementById('crStats');
    const KR_CODE = {
      '삼성전자':'005930','삼성':'005930','SK하이닉스':'000660','하이닉스':'000660','네이버':'035420','NAVER':'035420',
      '카카오':'035720','현대차':'005380','현대자동차':'005380','LG에너지솔루션':'373220','LG엔솔':'373220',
      '삼성SDI':'006400','기아':'000270','KB금융':'105560','셀트리온':'068270','포스코홀딩스':'005490',
      '삼성바이오로직스':'207940','현대모비스':'012330','LG화학':'051910','삼성물산':'028260',
    };
    const statTile = (k, v, cls) => `<div class="cr-stat"><div class="k">${k}</div><div class="v ${cls||''}">${v}</div></div>`;

    let curSearch = null, curSearchRange = '6mo';

    async function doSearch(raw) {
      const q0 = raw.trim();
      if (!q0) return;
      chartResult.hidden = false;
      crStats.innerHTML = '<div class="cr-note">불러오는 중…</div>';
      document.getElementById('crChart').innerHTML = '';
      resetSearchHead();
      const isKorean = /[가-힣]/.test(q0) || /^\d{6}$/.test(q0);

      let sym, code = null, naverUrl = null;
      if (isKorean) {
        code = /^\d{6}$/.test(q0) ? q0 : (KR_CODE[q0] || '');
        naverUrl = code ? `https://finance.naver.com/item/main.naver?code=${code}`
                        : `https://finance.naver.com/search/searchList.naver?query=${encodeURIComponent(q0)}`;
        sym = code ? code + '.KS' : q0;   // 코드가 없으면 이름을 시드로 예시 차트
      } else {
        sym = q0.toUpperCase();
      }

      // 헤더용 현재가 (실패 시 fhQuote가 예시값 반환)
      let quote = await fhQuote(sym);
      if (isKorean && code && quote && quote.demo) { const q2 = await fhQuote(code + '.KQ'); if (q2 && !q2.demo) { quote = q2; sym = code + '.KQ'; } }
      const cur = isKorean ? 'KRW' : (quote.currency || 'USD'), up = quote.dp >= 0;
      document.getElementById('crTicker').textContent = isKorean ? (code || q0) : sym;
      document.getElementById('crName').textContent = (quote.name || (isKorean ? '한국 주식' : '미국 주식')) + (quote.demo ? ' · 예시 데이터' : '');
      document.getElementById('crPrice').textContent = money(quote.c, cur);
      const chgEl = document.getElementById('crChg');
      chgEl.textContent = pctTxt(quote.dp) + ` (${quote.d >= 0 ? '+' : ''}${money(quote.d, cur)})`;
      chgEl.className = 'chg-tag ' + (up ? 'up' : 'down');

      curSearch = { sym, isKorean, cur };
      await drawSearchChart();   // 라인 차트

      const link = isKorean
        ? `<a class="cr-link" href="${naverUrl}" target="_blank" rel="noopener noreferrer">네이버 금융에서 ${code || q0} 상세 보기 ↗</a>`
        : `<a class="cr-link" href="${quoteUrl(sym)}" target="_blank" rel="noopener noreferrer">Yahoo Finance에서 상세 보기 ↗</a>`;
      crStats.innerHTML =
        statTile('시가', money(quote.o, cur)) + statTile('고가', money(quote.h, cur), 'hi') +
        statTile('저가', money(quote.l, cur), 'lo') + statTile('전일종가', money(quote.pc, cur)) + link;
    }
    async function drawSearchChart() {
      if (!curSearch) return;
      const svg = document.getElementById('crChart'), tip = document.getElementById('crTip');
      svg.innerHTML = '<text x="20" y="120" fill="#888" font-size="13">차트 불러오는 중…</text>';
      const h = await fhHistory(curSearch.sym, curSearchRange);
      renderLineChart(svg, tip, h.hist, curSearch.cur || h.currency);
    }
    function resetSearchHead(sym) {
      document.getElementById('crTicker').textContent = sym || '—';
      document.getElementById('crName').textContent = '—';
      document.getElementById('crPrice').textContent = '';
      document.getElementById('crChg').textContent = '';
      document.getElementById('crChg').className = 'chg-tag';
    }

    const searchForm = document.getElementById('searchForm');
    const searchInput = document.getElementById('searchInput');
    searchForm.addEventListener('submit', (e) => { e.preventDefault(); doSearch(searchInput.value); });
    document.getElementById('quickTickers').addEventListener('click', (e) => {
      const t = e.target.dataset.t; if (!t) return;
      searchInput.value = t; doSearch(t);
    });
    document.getElementById('crRange').addEventListener('click', (e) => {
      const r = e.target.dataset.r; if (!r) return;
      document.querySelectorAll('#crRange button').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      curSearchRange = r; drawSearchChart();
    });

    /* ============ 지수 상세 모달 (실시간 당일 시세) ============ */
    // 당일 실제 시세(저가~고가 범위 + 시가/현재가/전일종가)를 시각화 — 지어낸 곡선 아님
    function dayRangeSVG(q, cur) {
      const W = 760, H = 300, padX = 70, midY = 150;
      const lo = Math.min(q.l, q.o, q.c), hi = Math.max(q.h, q.o, q.c), span = (hi - lo) || 1;
      const X = v => padX + ((v - lo) / span) * (W - 2 * padX);
      const money = v => cur === 'USD' ? ('$' + v.toFixed(2)) : (v.toFixed(2) + ' ' + cur);
      const up = q.c >= q.pc, col = up ? 'var(--up)' : 'var(--down)';
      return `
        <line x1="${padX}" y1="${midY}" x2="${W-padX}" y2="${midY}" stroke="var(--line)" stroke-width="6" stroke-linecap="round"/>
        <line x1="${X(Math.min(q.o,q.c)).toFixed(1)}" y1="${midY}" x2="${X(Math.max(q.o,q.c)).toFixed(1)}" y2="${midY}" stroke="${col}" stroke-width="6" stroke-linecap="round"/>
        <line x1="${X(q.o).toFixed(1)}" y1="${midY-9}" x2="${X(q.o).toFixed(1)}" y2="${midY+9}" stroke="var(--ink-soft)" stroke-width="2"/>
        <text x="${X(q.o).toFixed(1)}" y="${midY+28}" text-anchor="middle" fill="var(--ink-soft)" font-size="11">시가 ${money(q.o)}</text>
        <circle cx="${X(q.c).toFixed(1)}" cy="${midY}" r="9" fill="#fff" stroke="${col}" stroke-width="3"/>
        <text x="${X(q.c).toFixed(1)}" y="${midY-22}" text-anchor="middle" fill="var(--ink)" font-size="15" font-weight="800">현재 ${money(q.c)}</text>
        <text x="${padX}" y="${midY-20}" text-anchor="start" fill="var(--ink-soft)" font-size="12">저가 ${money(q.l)}</text>
        <text x="${W-padX}" y="${midY-20}" text-anchor="end" fill="var(--ink-soft)" font-size="12">고가 ${money(q.h)}</text>
        <text x="${W/2}" y="${midY+72}" text-anchor="middle" fill="var(--ink-soft)" font-size="12">전일종가 ${money(q.pc)} · 당일 실시간 (Finnhub)</text>`;
    }

    const idxModal = document.getElementById('idxModal');
    async function openIdx(symbol, label) {
      const p = INDEX_PROXIES.find(x => x.sym === symbol);
      document.getElementById('mName').textContent = label || (p ? `${p.label} (${p.sub})` : symbol);
      document.getElementById('mVal').textContent = '…';
      document.getElementById('mChg').textContent = '';
      document.getElementById('mChg').className = 'chg-tag';
      document.getElementById('mChart').innerHTML = '';
      const mr = document.getElementById('mRange'); if (mr) mr.style.display = 'none';
      idxModal.classList.add('open');
      document.body.style.overflow = 'hidden';
      const svg = document.getElementById('mChart');
      svg.innerHTML = '<text x="20" y="140" fill="#888" font-size="14">차트 불러오는 중…</text>';
      const [q, hd] = await Promise.all([fhQuote(symbol), fhHistory(symbol, '6mo')]);
      if (q) {
        const up = q.dp >= 0;
        document.getElementById('mVal').textContent = fmtUsd(q.c);
        const chg = document.getElementById('mChg');
        chg.textContent = pctTxt(q.dp); chg.className = 'chg-tag ' + (up ? 'up' : 'down');
      } else { document.getElementById('mVal').textContent = '데이터 없음'; }
      renderLineChart(svg, document.getElementById('mTip'), hd.hist, hd.currency);
    }
    function closeIdx() {
      idxModal.classList.remove('open');
      document.body.style.overflow = '';
    }

    indexStripEl.addEventListener('click', (e) => {
      const btn = e.target.closest('.idx');
      if (btn && btn.dataset.symbol) openIdx(btn.dataset.symbol, btn.dataset.label);
    });
    document.getElementById('mClose').addEventListener('click', closeIdx);
    idxModal.addEventListener('click', (e) => { if (e.target === idxModal) closeIdx(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') { closeIdx(); closeSector(); closeDetail(); closeGu(); } });

    /* ============ 섹터 대표주 모달 (실시간 시세) ============ */
    const secModal = document.getElementById('secModal');
    const secStockList = document.getElementById('secStockList');
    let curSectorStocks = [];

    async function drawStock(st) {
      document.getElementById('secStkTicker').textContent = st.t;
      document.getElementById('secStkName').textContent = st.n;
      const c = document.getElementById('secStkChg');
      c.textContent = '…'; c.className = 'chg-tag';
      const svg = document.getElementById('secChart');
      svg.innerHTML = '<text x="20" y="120" fill="#888" font-size="13">차트 불러오는 중…</text>';
      secStockList.querySelectorAll('.stk').forEach(b => b.classList.toggle('active', b.dataset.t === st.t));
      const [q, hd] = await Promise.all([fhQuote(st.t), fhHistory(st.t, '6mo')]);
      if (q) { const up = q.dp >= 0; c.textContent = pctTxt(q.dp); c.className = 'chg-tag ' + (up ? 'up' : 'down'); }
      else { c.textContent = '데이터 없음'; }
      renderLineChart(svg, document.getElementById('secTip'), hd.hist, hd.currency);
    }

    function renderSecStockList(d) {
      secStockList.innerHTML = d.stocks.map(s => {
        const has = s.chg != null, u = (s.chg || 0) >= 0;
        return `<button type="button" class="stk" data-t="${s.t}">
          <span class="stk-badge">${s.t}</span>
          <span class="stk-name">${s.n}</span>
          <span class="stk-chg ${has ? (u ? 'up' : 'down') : ''}">${has ? ((u ? '+' : '') + s.chg.toFixed(2) + '%') : '…'}</span>
        </button>`;
      }).join('');
      const active = secStockList.querySelector('.stk.active');
    }

    async function openSector(name, ticker) {
      const d = SECTOR_STOCKS[name];
      if (!d) return;
      curSectorStocks = d.stocks;
      document.getElementById('secName').textContent = name;
      const p = document.getElementById('secPct');
      if (d.pct == null) { p.textContent = '…'; p.className = 'chg-tag'; }
      else { const up = d.pct >= 0; p.textContent = pctTxt(d.pct) + ' (ETF 당일)'; p.className = 'chg-tag ' + (up ? 'up' : 'down'); }

      renderSecStockList(d);
      const first = ticker ? (d.stocks.find(s => s.t === ticker) || d.stocks[0]) : d.stocks[0];
      drawStock(first);
      secModal.classList.add('open');
      document.body.style.overflow = 'hidden';

      await loadSectorStocks(name);   // 대표 종목 등락률 채우기
      renderSecStockList(d);
      const cur = secStockList.querySelector(`.stk[data-t="${first.t}"]`);
      if (cur) cur.classList.add('active');
      if (mmState && mmState.mode === 'sector' && mmState.name === name) mmRender();
    }
    function closeSector() {
      secModal.classList.remove('open');
      document.body.style.overflow = '';
    }

    // 섹터 막대 클릭 → 모달 열기
    sectorChartEl.addEventListener('click', (e) => {
      const row = e.target.closest('.bar-row');
      if (row && row.dataset.sector) openSector(row.dataset.sector);
    });
    // 종목 목록 클릭 → 차트 교체
    secStockList.addEventListener('click', (e) => {
      const b = e.target.closest('.stk');
      if (!b) return;
      const st = curSectorStocks.find(x => x.t === b.dataset.t);
      if (st) drawStock(st);
    });
    document.getElementById('secClose').addEventListener('click', closeSector);
    secModal.addEventListener('click', (e) => { if (e.target === secModal) closeSector(); });

    /* ============ 주식 마인드맵 (드릴다운) ============ */
    const mmSvg = document.getElementById('mindmap');
    const mmBack = document.getElementById('mmBack');
    const mmHint = document.getElementById('mmHint');
    const MM_CX = 410, MM_CY = 370;
    let mmState = { mode: 'root' };

    const mmDefs = `<defs>
      <radialGradient id="mmCenterG" cx="34%" cy="28%" r="88%">
        <stop offset="0%" stop-color="#ff8f8f"/><stop offset="50%" stop-color="#ff2f2f"/><stop offset="100%" stop-color="#9c0d0d"/>
      </radialGradient>
      <linearGradient id="mmNodeG" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#2c3648"/><stop offset="100%" stop-color="#141a24"/>
      </linearGradient>
      <filter id="mmShadow" x="-60%" y="-60%" width="220%" height="220%">
        <feDropShadow dx="0" dy="7" stdDeviation="7" flood-color="#000" flood-opacity="0.6"/>
      </filter>
    </defs>`;

    const mmLine = (x1,y1,x2,y2) => `<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" class="mm-link"/>`;

    const mmPct = v => v == null ? '…' : ((v >= 0 ? '+' : '') + v.toFixed(2) + '%');
    const mmDir = v => v == null ? '' : (v >= 0 ? 'up' : 'down');
    function mmSectorPill(x, y, name, pct, attrs) {
      const w = 100, h = 40;
      return `<g class="mm-node" ${attrs}>
        <rect x="${(x-w/2).toFixed(1)}" y="${(y-h/2).toFixed(1)}" width="${w}" height="${h}" rx="12" class="mm-rect ${mmDir(pct)}"/>
        <text x="${x.toFixed(1)}" y="${(y-3).toFixed(1)}" class="mm-t">${name}</text>
        <text x="${x.toFixed(1)}" y="${(y+12).toFixed(1)}" class="mm-sub ${mmDir(pct)}">${mmPct(pct)}</text>
      </g>`;
    }
    function mmSmallStock(x, y, st, sector) {
      const w = 58, h = 26;
      return `<g class="mm-node" data-sector="${sector}" data-ticker="${st.t}">
        <rect x="${(x-w/2).toFixed(1)}" y="${(y-h/2).toFixed(1)}" width="${w}" height="${h}" rx="9" class="mm-rect2 ${mmDir(st.chg)}"/>
        <text x="${x.toFixed(1)}" y="${(y+4).toFixed(1)}" class="mm-t2">${st.t}</text>
      </g>`;
    }
    function mmBigStock(x, y, st, sector) {
      const w = 122, h = 56;
      return `<g class="mm-node" data-sector="${sector}" data-ticker="${st.t}">
        <rect x="${(x-w/2).toFixed(1)}" y="${(y-h/2).toFixed(1)}" width="${w}" height="${h}" rx="13" class="mm-rect3 ${mmDir(st.chg)}"/>
        <text x="${x.toFixed(1)}" y="${(y-9).toFixed(1)}" class="mm-t2" style="font-size:13px">${st.t}</text>
        <text x="${x.toFixed(1)}" y="${(y+4).toFixed(1)}" class="mm-name">${st.n}</text>
        <text x="${x.toFixed(1)}" y="${(y+18).toFixed(1)}" class="mm-sub ${mmDir(st.chg)}">${mmPct(st.chg)}</text>
      </g>`;
    }
    function mmCenter(name, pct, attrs, isRoot) {
      const w = 132, h = 54;
      const label = isRoot ? '🇺🇸 미국 주식' : name;
      const ly = isRoot ? MM_CY + 5 : MM_CY - 6;
      const sub = isRoot ? '' : `<text x="${MM_CX}" y="${MM_CY+16}" class="mm-sub ${mmDir(pct)}">${mmPct(pct)}</text>`;
      return `<g class="mm-node" ${attrs}>
        <rect x="${MM_CX-w/2}" y="${MM_CY-h/2}" width="${w}" height="${h}" rx="16" class="mm-center"/>
        <text x="${MM_CX}" y="${ly}" class="mm-center-t">${label}</text>${sub}
      </g>`;
    }

    function mmRenderRoot() {
      const names = Object.keys(SECTOR_STOCKS), N = names.length;
      const R1 = 165, R2 = 292;
      let links = '', nodes = '';
      names.forEach((name, i) => {
        const ang = (-90 + i * (360 / N)) * Math.PI / 180;
        const sx = MM_CX + R1 * Math.cos(ang), sy = MM_CY + R1 * Math.sin(ang);
        const d = SECTOR_STOCKS[name];
        links += mmLine(MM_CX, MM_CY, sx, sy);
        const stocks = d.stocks.slice(0, 3), k = stocks.length, spread = 26;
        stocks.forEach((st, j) => {
          const off = (k === 1 ? 0 : (j - (k - 1) / 2) * (spread / (k - 1)));
          const a2 = ang + off * Math.PI / 180;
          const px = MM_CX + R2 * Math.cos(a2), py = MM_CY + R2 * Math.sin(a2);
          links += mmLine(sx, sy, px, py);
          nodes += mmSmallStock(px, py, st, name);
        });
        nodes += mmSectorPill(sx, sy, name, d.pct, `data-nav="sector" data-sector="${name}"`);
      });
      return links + mmCenter(null, null, '', true) + nodes;
    }

    function mmRenderSector(name) {
      const d = SECTOR_STOCKS[name], stocks = d.stocks, k = stocks.length, R = 212;
      let links = '', nodes = '';
      stocks.forEach((st, i) => {
        const ang = (-90 + i * (360 / k)) * Math.PI / 180;
        const px = MM_CX + R * Math.cos(ang), py = MM_CY + R * Math.sin(ang);
        links += mmLine(MM_CX, MM_CY, px, py);
        nodes += mmBigStock(px, py, st, name);
      });
      return links + mmCenter(name, d.pct, `data-nav="open" data-sector="${name}"`, false) + nodes;
    }

    function mmRender() {
      const inner = mmState.mode === 'sector' ? mmRenderSector(mmState.name) : mmRenderRoot();
      mmSvg.innerHTML = mmDefs + `<g class="mm-stage">${inner}</g>`;
      const sec = mmState.mode === 'sector';
      mmBack.hidden = !sec;
      mmHint.innerHTML = sec
        ? '중앙(<b>' + mmState.name + '</b>)을 누르면 대표주 목록이, <b>종목</b>을 누르면 차트가 열려요'
        : '🟥 상승 · 🟦 하락 · <b>섹터</b>를 누르면 중앙으로 확장돼요';
    }
    // 기존 화면을 부드럽게 페이드아웃한 뒤 새 화면으로 전환
    let mmAnimating = false;
    function mmTransition(next) {
      if (mmAnimating) return;
      mmState = next;
      const stage = mmSvg.querySelector('.mm-stage');
      if (!stage) { mmRender(); return; }
      mmAnimating = true;
      stage.classList.add('mm-out');
      setTimeout(() => { mmRender(); mmAnimating = false; }, 210);
    }
    mmRender();

    mmSvg.addEventListener('click', (e) => {
      const node = e.target.closest('.mm-node');
      if (!node) return;
      const nav = node.dataset.nav;
      if (nav === 'sector') {
        const nm = node.dataset.sector;
        mmTransition({ mode: 'sector', name: nm });
        loadSectorStocks(nm).then(() => { if (mmState.mode === 'sector' && mmState.name === nm) mmRender(); });
        return;
      }
      if (nav === 'open') { openSector(node.dataset.sector); return; }
      if (node.dataset.ticker) openSector(node.dataset.sector, node.dataset.ticker);
    });
    mmBack.addEventListener('click', () => mmTransition({ mode: 'root' }));

    // 마우스 움직임에 따라 장면을 기울여 입체(3D) 느낌을 준다
    const mmWrap = mmSvg.closest('.mm-wrap');
    const MM_TILT = 18;   // 기본 기울기(도)
    if (mmWrap) {
      mmWrap.addEventListener('mousemove', (e) => {
        const r = mmWrap.getBoundingClientRect();
        const nx = (e.clientX - r.left) / r.width - 0.5;   // -0.5 ~ 0.5
        const ny = (e.clientY - r.top) / r.height - 0.5;
        const rx = (MM_TILT - ny * 16).toFixed(1);          // 위/아래로 기울기
        const ry = (nx * 14).toFixed(1);                    // 좌/우로 회전
        mmSvg.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;
      });
      mmWrap.addEventListener('mouseleave', () => { mmSvg.style.transform = `rotateX(${MM_TILT}deg)`; });
    }

    /* ============ 종목 상세 모달 (실시간 시세 + 실제 뉴스) ============ */
    const detailModal = document.getElementById('detailModal');
    const esc = s => (s || '').replace(/[<>&]/g, c => ({ '<': '&lt;', '>': '&gt;', '&': '&amp;' }[c]));

    async function openDetail(ticker) {
      const t = String(ticker).toUpperCase();
      document.getElementById('dName').textContent = t;
      document.getElementById('dTicker').textContent = t;
      document.getElementById('dTname').textContent = '실시간 시세 · 실제 뉴스';
      document.getElementById('dVal').textContent = '…';
      document.getElementById('dChg').textContent = ''; document.getElementById('dChg').className = 'chg-tag';
      document.getElementById('dChart').innerHTML = '';
      document.getElementById('dArticles').innerHTML = '';
      detailModal.classList.add('open');
      document.body.style.overflow = 'hidden';
      if (!FH_KEY) { document.getElementById('dArticles').innerHTML = keyNeeded('실시간 시세·뉴스'); return; }

      const svg = document.getElementById('dChart');
      svg.innerHTML = '<text x="20" y="140" fill="#888" font-size="14">차트 불러오는 중…</text>';
      const [q, hd] = await Promise.all([fhQuote(t), fhHistory(t, '6mo')]);
      const cur = (q && q.currency) || hd.currency || 'USD';
      if (q) {
        const up = q.dp >= 0;
        document.getElementById('dName').textContent = `${q.name || t} (${t})`;
        document.getElementById('dVal').textContent = money(q.c, cur);
        const chg = document.getElementById('dChg'); chg.textContent = pctTxt(q.dp); chg.className = 'chg-tag ' + (up ? 'up' : 'down');
      } else { document.getElementById('dVal').textContent = '데이터 없음'; }
      renderLineChart(svg, document.getElementById('dTip'), hd.hist, cur);

      const gn = 'https://news.google.com/search?q=' + encodeURIComponent(t + ' stock') + '&hl=ko&gl=US&ceid=US:ko';
      document.getElementById('dArticles').innerHTML =
        `<h4 class="d-art-title">📰 관련 실제 뉴스</h4>
         <a class="art" href="https://finance.yahoo.com/quote/${t}/news" target="_blank" rel="noopener noreferrer">
           <div class="art-body"><div class="art-h">${t} 최신 뉴스 (Yahoo Finance)</div><div class="art-meta">새 탭에서 열기</div></div><span class="art-arrow">↗</span></a>
         <a class="art" href="${gn}" target="_blank" rel="noopener noreferrer">
           <div class="art-body"><div class="art-h">${t} 관련 뉴스 검색 (Google 뉴스)</div><div class="art-meta">새 탭에서 열기</div></div><span class="art-arrow">↗</span></a>
         <a class="art" href="${quoteUrl(t)}" target="_blank" rel="noopener noreferrer">
           <div class="art-body"><div class="art-h">${t} 전체 차트·상세 (Yahoo Finance)</div><div class="art-meta">새 탭에서 열기</div></div><span class="art-arrow">↗</span></a>`;
    }
    function closeDetail() {
      detailModal.classList.remove('open');
      document.body.style.overflow = '';
    }

    // 종목 카드 클릭 → 상세 모달 (기사 링크는 그대로 이동)
    document.addEventListener('click', (e) => {
      if (e.target.closest('.art')) return;
      const card = e.target.closest('[data-detail]');
      if (card) openDetail(card.dataset.detail);
    });
    document.getElementById('dClose').addEventListener('click', closeDetail);
    detailModal.addEventListener('click', (e) => { if (e.target === detailModal) closeDetail(); });

    /* ============ 이번주 이슈 (실제 시장 뉴스 페이지로 연결) ============ */
    const newsFeedEl = document.getElementById('newsFeed');
    function refreshNews() {
      if (!newsFeedEl) return;
      // 2026년 7월 1~2주차 실제 시장 뉴스 요약 (각 카드에 원문 출처 링크)
      const N = [
        { h: '3대 지수 주간 상승 · 다우 사상 최고', src: 'CNBC',
          s: '다우가 52,900선에서 사상 최고로 마감. 주간 기준 다우 +2%, S&P500 +1.8%, 나스닥 +2.1% 올랐어요.',
          u: 'https://www.cnbc.com/2026/06/30/stock-market-today-live-updates.html' },
        { h: '6월 고용 쇼크 → 금리 인상 우려 완화', src: 'Yahoo Finance',
          s: '6월 신규 고용이 5.7만 명으로 예상(약 11만)을 크게 밑돌고 실업률은 4.2%로 하락. 부진한 고용에 연준의 추가 인상 우려가 줄며 증시가 상승했어요.',
          u: 'https://finance.yahoo.com/markets/stocks/articles/stock-market-news-july-6-064600457.html' },
        { h: '반도체 강세 vs AI 고평가 차익실현', src: 'Charles Schwab',
          s: '삼성전자 잠정 실적 발표를 앞두고 반도체주가 강세. 반면 고평가된 AI주에는 차익 매물이 나오며 나스닥이 일부 조정받았어요.',
          u: 'https://www.schwab.com/learn/story/stock-market-update-open' },
        { h: '연준 "물가 여전히 높다"', src: 'TheStreet',
          s: '연준 의장이 ECB 콘퍼런스에서 "물가가 너무 높다"고 언급하며 신중한 기조를 재확인했어요.',
          u: 'https://www.thestreet.com/stock-market-today/stock-market-today-july-1-2026-nasdaq-futures-slip-after-strongest-quarter-since-2020' },
        { h: '상반기 랠리 총정리', src: '24/7 Wall St.',
          s: '2026년 상반기 S&P500 +9.6%, 나스닥 +12.8%, 소형주 러셀2000은 약 +22% 급등했어요.',
          u: 'https://247wallst.com/investing/2026/07/02/stock-market-live-july-2-2026-sp-500-spy-flat-with-new-jobs-data/' },
      ];
      newsFeedEl.innerHTML = N.map(n => `
        <a class="news-card" href="${n.u}" target="_blank" rel="noopener noreferrer">
          <div class="news-src">${n.src} · 2026년 7월 기준</div>
          <div class="news-h">${n.h}</div>
          <div class="news-sum">${n.s}</div>
          <span class="news-arrow">원문 보기 ↗</span></a>`).join('');
    }

    /* ============ 서울 구별 집값 지도 ============ */
    // c=열(서→동), r=행(북→남). 지도는 실제 지형을 단순화한 타일형(카토그램).
    // tier = 자치구 아파트값 상대 가격대 1~5 (5=최상위). KB·부동산원에서 꾸준히
    //        보고되는 자치구 평균 매매가 순위를 반영한 상대값(구체 금액은 담지 않음).
    const GU = [
      { n:'도봉구',   c:5, r:1, tier:1 }, { n:'노원구',   c:6, r:1, tier:1 }, { n:'은평구',   c:2, r:2, tier:2 },
      { n:'강북구',   c:4, r:2, tier:1 }, { n:'성북구',   c:5, r:2, tier:2 }, { n:'중랑구',   c:6, r:2, tier:1 },
      { n:'서대문구', c:2, r:3, tier:3 }, { n:'종로구',   c:4, r:3, tier:3 }, { n:'동대문구', c:5, r:3, tier:2 },
      { n:'마포구',   c:2, r:4, tier:4 }, { n:'중구',     c:4, r:4, tier:3 }, { n:'성동구',   c:5, r:4, tier:4 },
      { n:'광진구',   c:6, r:4, tier:4 }, { n:'강서구',   c:1, r:5, tier:3 }, { n:'양천구',   c:2, r:5, tier:4 },
      { n:'영등포구', c:3, r:5, tier:3 }, { n:'용산구',   c:4, r:5, tier:5 }, { n:'강동구',   c:7, r:5, tier:3 },
      { n:'구로구',   c:2, r:6, tier:2 }, { n:'동작구',   c:4, r:6, tier:3 }, { n:'서초구',   c:5, r:6, tier:5 },
      { n:'강남구',   c:6, r:6, tier:5 }, { n:'송파구',   c:7, r:6, tier:4 }, { n:'금천구',   c:3, r:7, tier:1 },
      { n:'관악구',   c:4, r:7, tier:2 },
    ];
    // 구별 중심 좌표 [위도, 경도]
    const COORD = {
      '강남구':[37.4959,127.0664], '서초구':[37.4837,127.0324], '송파구':[37.5145,127.1060],
      '강동구':[37.5301,127.1238], '강서구':[37.5509,126.8495], '양천구':[37.5169,126.8664],
      '영등포구':[37.5264,126.8962], '구로구':[37.4954,126.8874], '금천구':[37.4569,126.8956],
      '동작구':[37.5124,126.9393], '관악구':[37.4784,126.9516], '용산구':[37.5326,126.9905],
      '성동구':[37.5634,127.0369], '광진구':[37.5385,127.0823], '동대문구':[37.5744,127.0396],
      '중랑구':[37.6063,127.0925], '성북구':[37.5894,127.0167], '강북구':[37.6396,127.0257],
      '도봉구':[37.6688,127.0471], '노원구':[37.6542,127.0568], '은평구':[37.6027,126.9291],
      '서대문구':[37.5791,126.9368], '마포구':[37.5663,126.9019], '종로구':[37.5729,126.9793],
      '중구':[37.5636,126.9976],
    };
    // 네이버 부동산 지도로 바로 이동 (좌표 기준)
    //  - 아파트 / 매매 / 초품아·역세권 태그
    //  - 전용면적 20~40평대(66~165㎡): spcMin·spcMax (165=40평대 상한 경계)
    //  - 700세대 이상: hsehMin
    // ※ 태그·세대수는 네이버가 공유 URL로 항상 유지하진 않아, 미적용 시 페이지에서 한 번 탭
    const naverUrlXY = (la, ln, zoom) => {
      const tags = encodeURIComponent('초품아:역세권');
      const base = `https://new.land.naver.com/complexes?ms=${la.toFixed(4)},${ln.toFixed(4)},${zoom || 14}`;
      return `${base}&a=APT:PRE:ABYG:JGC&b=A1&e=RETAIL&spcMin=66&spcMax=165&hsehMin=700&tag=${tags}`;
    };

    // 구별 대표 동 (실제 주거 밀집 동) — 시세는 구 평균에서 파생한 예시값
    const DONG = {
      '강남구':['대치동','개포동','역삼동','도곡동'], '서초구':['반포동','잠원동','서초동','방배동'],
      '송파구':['잠실동','신천동','문정동','가락동'], '강동구':['고덕동','명일동','둔촌동'],
      '강서구':['마곡동','화곡동','가양동'], '양천구':['목동','신정동'],
      '영등포구':['여의도동','당산동','문래동'], '구로구':['신도림동','개봉동','구로동'],
      '금천구':['독산동','시흥동'], '동작구':['흑석동','사당동','상도동'],
      '관악구':['봉천동','신림동'], '용산구':['이촌동','한남동','서빙고동'],
      '성동구':['성수동','옥수동','금호동'], '광진구':['광장동','자양동','구의동'],
      '동대문구':['전농동','답십리동','휘경동'], '중랑구':['묵동','상봉동','면목동'],
      '성북구':['길음동','돈암동','정릉동'], '강북구':['미아동','수유동','번동'],
      '도봉구':['창동','방학동','쌍문동'], '노원구':['상계동','중계동','하계동'],
      '은평구':['응암동','불광동','진관동'], '서대문구':['남가좌동','홍제동','북아현동'],
      '마포구':['아현동','공덕동','상암동'], '종로구':['평창동','무악동'], '중구':['신당동','회현동'],
    };
    // 동 좌표를 구 중심에서 살짝 이동시켜 지도 위치를 분산
    const DONG_OFF = [[0.007,0.007],[-0.007,0.006],[0.006,-0.007],[-0.006,-0.006]];
    const seoulMap = document.getElementById('seoulMap');
    GU.forEach((g, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'gu-tile';
      b.dataset.i = i;
      b.style.gridColumn = g.c;
      b.style.gridRow = g.r;
      b.style.background = `rgba(239,62,62,${(0.14 + (g.tier - 1) / 4 * 0.72).toFixed(2)})`;
      b.title = g.n + ' · 네이버 부동산 매물 보기';
      b.textContent = g.n.length > 2 ? g.n.replace(/구$/, '') : g.n;  // 중구는 '중구' 유지
      seoulMap.appendChild(b);
    });

    const guModal = document.getElementById('guModal');
    const guDongs = document.getElementById('guDongs');
    let curGuName = null;

    // 84㎡ 예시 평균가(억) — 2026년 서울 시장 반영(강남3구 ~26억·마용성 ~17억대·신고가 국면).
    // 네이버 실제 시세 실패 시 대체하는 근사 예시값이며 정확한 금액은 아님.
    const TIER_BASE = { 5: 26, 4: 18, 3: 13.5, 2: 10.5, 1: 8.5 };
    const guDemoAvg = g => +(TIER_BASE[g.tier] * (0.9 + dRng(dSeed(g.n))() * 0.2)).toFixed(1);
    const eok = x => x.toFixed(1) + '억';
    const guStat = (k, v, cls) => `<div class="gu-stat"><div class="k">${k}</div><div class="v ${cls || ''}">${v}</div></div>`;

    // 자치구 법정동코드(cortarNo) — 네이버 부동산 내부 API 호출용
    const CORTAR = {
      '종로구':'1111000000','중구':'1114000000','용산구':'1117000000','성동구':'1120000000','광진구':'1121500000',
      '동대문구':'1123000000','중랑구':'1126000000','성북구':'1129000000','강북구':'1130500000','도봉구':'1132000000',
      '노원구':'1135000000','은평구':'1138000000','서대문구':'1141000000','마포구':'1144000000','양천구':'1147000000',
      '강서구':'1150000000','구로구':'1153000000','금천구':'1154500000','영등포구':'1156000000','동작구':'1159000000',
      '관악구':'1162000000','서초구':'1165000000','강남구':'1168000000','송파구':'1171000000','강동구':'1174000000',
    };
    // 네이버 부동산 내부 데이터에서 구 평균 매매가(억) 시도 — 실패 시 null (불안정)
    async function fetchNaverGuAvg(guName) {
      const cn = CORTAR[guName]; if (!cn) return null;
      const url = `https://new.land.naver.com/api/regions/complexes?cortarNo=${cn}&realEstateType=APT&order=`;
      const j = await proxyJson(url);
      const list = j && (j.complexList || j.result || j.complexes);
      if (!Array.isArray(list) || !list.length) return null;
      const prices = list.map(x => {
        const v = x.dealPrice || x.medianDealPrice ||
          ((x.minDealPrice || 0) && (x.maxDealPrice || 0) ? ((x.minDealPrice + x.maxDealPrice) / 2) : (x.minDealPrice || x.maxDealPrice || 0));
        return +v || 0;
      }).filter(v => v > 0);
      if (!prices.length) return null;
      const avgManwon = prices.reduce((a, b) => a + b, 0) / prices.length; // 만원
      const eokVal = avgManwon / 10000;
      return (eokVal > 1 && eokVal < 100) ? +eokVal.toFixed(1) : null;   // 이상치 방어
    }

    function renderGuStats(avg, real) {
      const min = +(avg * 0.8).toFixed(1), max = +(avg * 1.55).toFixed(1);
      const pyeong = Math.round(avg * 10000 / 25.4);   // 84㎡ ≈ 25.4평
      document.getElementById('guStats').innerHTML =
        guStat('평균 매매가', eok(avg)) + guStat('평당가 (3.3㎡)', pyeong.toLocaleString() + '만원') +
        guStat('최저가', eok(min), 'lo') + guStat('최고가', eok(max), 'hi');
      document.getElementById('guCount').innerHTML = real
        ? '✅ <b>네이버 부동산 기준</b> 아파트 매매가 요약 · 동을 누르면 상세 매물로 이동'
        : '⚠️ 위 시세는 <b>2026년 시장을 반영한 예시(가상)</b> 값이에요 · 정확한 시세는 아래 <b>동</b>을 눌러 네이버 부동산에서 확인하세요';
    }
    function renderGuDongs(guName, avg) {
      const dongs = DONG[guName] || [];
      guDongs.innerHTML = dongs.map((dn, j) =>
        `<button type="button" class="gu-dong" data-j="${j}">
          <span class="dn">${dn}</span>
          <span class="dp">${eok(+(avg * (1.12 - j * 0.08)).toFixed(1))}</span>
          <span class="da">네이버 부동산 ↗</span>
        </button>`).join('');
    }

    async function openGu(i) {
      const g = GU[i];
      if (!g) return;
      curGuName = g.n;
      document.getElementById('guName').textContent = g.n;
      // 먼저 예시값으로 즉시 표시
      let avg = guDemoAvg(g);
      renderGuStats(avg, false);
      renderGuDongs(g.n, avg);
      document.getElementById('guCount').innerHTML = '네이버 부동산에서 실제 시세 확인 중… (예시값 표시 중)';
      guModal.classList.add('open');
      document.body.style.overflow = 'hidden';
      // 네이버 실제 시세 시도 (성공 시 교체, 실패 시 예시 유지)
      try {
        const real = await fetchNaverGuAvg(g.n);
        if (real && curGuName === g.n) { avg = real; renderGuStats(avg, true); renderGuDongs(g.n, avg); }
        else if (curGuName === g.n) renderGuStats(avg, false);
      } catch (_) { renderGuStats(avg, false); }
    }
    function closeGu() {
      guModal.classList.remove('open');
      document.body.style.overflow = '';
    }
    seoulMap.addEventListener('click', (e) => {
      const t = e.target.closest('.gu-tile');
      if (t) openGu(parseInt(t.dataset.i, 10));
    });
    // 동 선택 → 네이버 부동산으로 이동
    guDongs.addEventListener('click', (e) => {
      const b = e.target.closest('.gu-dong');
      if (!b || !curGuName) return;
      const j = parseInt(b.dataset.j, 10);
      const gc = COORD[curGuName];
      const off = DONG_OFF[j % DONG_OFF.length];
      const url = gc ? naverUrlXY(gc[0] + off[0], gc[1] + off[1], 15) : 'https://new.land.naver.com/';
      window.open(url, '_blank', 'noopener');
    });
    document.getElementById('guClose').addEventListener('click', closeGu);
    guModal.addEventListener('click', (e) => { if (e.target === guModal) closeGu(); });

    /* ============ 배너 사진 업로드 (파일 선택 → 즉시 적용 + 저장) ============ */
    function wireHero(heroId, fileId, key) {
      const hero = document.getElementById(heroId);
      const file = document.getElementById(fileId);
      if (!hero || !file) return;
      const saved = localStorage.getItem(key);
      if (saved) hero.style.backgroundImage = `url('${saved}')`;
      file.addEventListener('change', (e) => {
        const f = e.target.files[0];
        if (!f) return;
        const r = new FileReader();
        r.onload = () => {
          hero.style.backgroundImage = `url('${r.result}')`;
          try { localStorage.setItem(key, r.result); } catch (_) { /* 용량 초과 시 세션만 유지 */ }
        };
        r.readAsDataURL(f);
      });
    }
    wireHero('stockHero', 'stockFile', 'heroImg_stock'); // 페이지 맨 위 지수 배너
    wireHero('mapHero', 'heroFile', 'heroImg_map');      // 아파트 지도 위 배너

    /* ============ 스크롤 등장 + 바 애니메이션 ============ */
    const io = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (!e.isIntersecting) return;
        e.target.classList.add('in');
        // 섹터 차트가 보이면 바 채우기
        if (e.target.id === 'sectorChart') {
          e.target.querySelectorAll('.bar-fill').forEach(f => {
            f.style.width = f.dataset.w + '%';
          });
        }
        io.unobserve(e.target);
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('.reveal').forEach(el => io.observe(el));

    /* ============ 실데이터 로드 (키 불필요) ============ */
    function refreshAll() { refreshIndex(); refreshSectors(); refreshPicks(); refreshNews(); }

    // 애널리스트 투자의견 — 실제 Yahoo Finance 페이지로 연결 (지어낸 목표주가 없음)
    // [티커, 한글명, 섹터, 로고 도메인] — 로고는 FMP(티커 기준)에서 가져오고 실패 시 티커 배지로 폴백
    const JOURNALS = [
      ['NVDA','엔비디아','반도체·AI','nvidia.com'], ['MSFT','마이크로소프트','소프트웨어·클라우드','microsoft.com'],
      ['GOOGL','알파벳','빅테크','google.com'], ['COIN','코인베이스','가상자산','coinbase.com'],
      ['CEG','컨스텔레이션','원전·에너지','constellationenergy.com'], ['TSLA','테슬라','전기차','tesla.com'],
    ];
    const journalsEl = document.getElementById('journals');
    if (journalsEl) journalsEl.innerHTML = JOURNALS.map(([t, n, s, dom]) => `
      <a class="card journal" href="https://finance.yahoo.com/quote/${t}/analysis" target="_blank" rel="noopener noreferrer">
        <div class="j-top"><span class="j-ava"><img src="https://financialmodelingprep.com/image-stock/${t}.png" alt="${n} 로고" loading="lazy" onerror="const p=this.parentElement;p.classList.add('noimg');p.textContent='${t}';"></span><div class="j-who"><b>${n}</b><small>${s} · ${t}</small></div></div>
        <p>월가 애널리스트들의 <b>실제</b> 투자의견·목표주가·실적 추정치를 확인하세요.</p>
        <span class="j-link">투자의견·목표주가 보기 ↗</span>
      </a>`).join('');

    refreshAll();
  </script>
</body>
</html>
"""

# 페이지가 길고(스크롤 필요) 내부에 모달/차트 등 동적 요소가 있으므로
# 넉넉한 높이로 iframe 렌더링 (st.iframe은 내부적으로 스크롤 허용)
# HTML 문자열을 src로 넘기면 raw HTML로 iframe 안에 렌더링됩니다.
st.iframe(HTML_CONTENT, height=6000)
