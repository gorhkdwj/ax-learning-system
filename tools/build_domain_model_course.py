#!/usr/bin/env python
"""구조화된 공개 콘텐츠에서 온톨로지 D2 오프라인 HTML 교재를 생성합니다."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


PUBLIC_ROOT = Path(__file__).resolve().parents[1]
COURSE_ROOT = (
    PUBLIC_ROOT
    / "catalog"
    / "items"
    / "unit.data-analytics-ml.domain-concept-relationship-modeling"
    / "resources"
    / "course"
)
DEFAULT_SOURCE = COURSE_ROOT / "course-content.json"
DEFAULT_OUTPUT = COURSE_ROOT / "index.html"


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _list(items: list[str], *, ordered: bool = False, checklist_prefix: str = "") -> str:
    tag = "ol" if ordered else "ul"
    rows: list[str] = []
    for index, item in enumerate(items, start=1):
        if checklist_prefix:
            store_id = f"{checklist_prefix}.step-{index}"
            rows.append(
                "<li class=\"check-row\"><label>"
                f"<input type=\"checkbox\" data-store-id=\"{_escape(store_id)}\">"
                f"<span>{_escape(item)}</span></label></li>"
            )
        else:
            rows.append(f"<li>{_escape(item)}</li>")
    return f"<{tag}>{''.join(rows)}</{tag}>"


def _render_concept(concept: dict[str, Any], *, opened: bool = False) -> str:
    open_attribute = " open" if opened else ""
    paragraphs = "".join(
        f"<p>{_escape(paragraph)}</p>" for paragraph in concept.get("paragraphs", [])
    )
    bullets = _list(concept.get("bullets", [])) if concept.get("bullets") else ""
    return (
        f"<details class=\"concept\"{open_attribute}>"
        f"<summary>{_escape(concept['title'])}</summary>"
        f"<div class=\"concept-body\">{paragraphs}{bullets}</div>"
        "</details>"
    )


def _render_module(module: dict[str, Any]) -> str:
    module_id = _escape(module["id"])
    concepts = "".join(
        _render_concept(concept, opened=index == 0)
        for index, concept in enumerate(module.get("concepts", []))
    )
    steps = _list(
        module.get("steps", []),
        ordered=True,
        checklist_prefix=f"module.{module['id']}",
    )
    checkpoint = module["checkpoint"]
    resource_links = ""
    if module.get("resources"):
        links = "".join(
            f'<li><a href="{_escape(resource["href"])}">{_escape(resource["label"])}</a></li>'
            for resource in module["resources"]
        )
        resource_links = f'<h4>실습 자료</h4><ul class="resource-links">{links}</ul>'
    kind_label = "연결 Probe" if module.get("kind") == "linked_probe" else "핵심 Unit"
    return f"""
    <section class="module" id="{module_id}" aria-labelledby="{module_id}-title">
      <header class="module-header">
        <div>
          <p class="eyebrow">블록 {module['number']} · {_escape(kind_label)}</p>
          <h2 id="{module_id}-title">{_escape(module['title'])}</h2>
          <p class="objective">{_escape(module['objective'])}</p>
        </div>
        <div class="time-card" aria-label="예상 학습 시간 {module['minutes']}분">
          <strong>{module['minutes']}분</strong>
          <span>예상 시간</span>
        </div>
      </header>

      <div class="timer" data-timer data-minutes="{module['minutes']}">
        <span class="timer-display" data-timer-display aria-live="polite">{module['minutes']}:00</span>
        <button type="button" data-timer-action="start">타이머 시작</button>
        <button type="button" data-timer-action="pause">일시정지</button>
        <button type="button" data-timer-action="reset">초기화</button>
      </div>

      <div class="concept-stack" aria-label="개념 설명">{concepts}</div>

      <div class="work-grid">
        <div class="panel">
          <h3>학습 절차</h3>
          {steps}
        </div>
        <div class="panel artifact">
          <h3>필수 산출물</h3>
          <p>{_escape(module['artifact'])}</p>
          {resource_links}
          <label class="artifact-check">
            <input type="checkbox" data-store-id="module.{module['id']}.artifact">
            산출물을 작성했습니다.
          </label>
        </div>
      </div>

      <div class="checkpoint">
        <h3>자기 설명</h3>
        <p>{_escape(checkpoint['prompt'])}</p>
        <label for="note-{module_id}">자신의 말로 작성하십시오.</label>
        <textarea id="note-{module_id}" rows="6" data-store-id="module.{module['id']}.note"></textarea>
        <details>
          <summary>검토 기준 보기</summary>
          <p>{_escape(checkpoint['guidance'])}</p>
        </details>
      </div>

      <label class="module-complete">
        <input type="checkbox" data-module-complete="{module_id}" data-store-id="module.{module['id']}.complete">
        <span>블록 {module['number']} 완료로 표시</span>
      </label>
    </section>
    """


CSS = r"""
:root {
  color-scheme: light dark;
  --bg: #f4f1ea;
  --surface: #fffdf8;
  --surface-strong: #ffffff;
  --ink: #17211d;
  --muted: #53645c;
  --line: #cfd8d2;
  --accent: #0b6b4f;
  --accent-strong: #064f3a;
  --accent-soft: #dcefe7;
  --warm: #a34f14;
  --shadow: 0 16px 36px rgba(23, 33, 29, 0.10);
  --radius: 18px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background:
    radial-gradient(circle at 12% 4%, rgba(11, 107, 79, 0.12), transparent 27rem),
    var(--bg);
  color: var(--ink);
  font-family: "Pretendard", "Noto Sans KR", "Malgun Gothic", system-ui, sans-serif;
  line-height: 1.72;
}
a { color: var(--accent-strong); }
a:focus-visible, button:focus-visible, summary:focus-visible, input:focus-visible, textarea:focus-visible {
  outline: 3px solid #e79a48;
  outline-offset: 3px;
}
.skip-link {
  position: fixed; top: 0; left: 1rem; z-index: 100;
  transform: translateY(-120%); padding: .7rem 1rem;
  background: var(--ink); color: white; border-radius: 0 0 10px 10px;
}
.skip-link:focus { transform: translateY(0); }
.hero {
  padding: 4.5rem max(1.5rem, calc((100vw - 1180px) / 2));
  background: linear-gradient(125deg, #0a4937, #0b6b4f 58%, #9b5b25);
  color: #fff;
}
.hero-inner { max-width: 920px; }
.kicker { margin: 0 0 .6rem; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
h1 { max-width: 820px; margin: 0; font-size: clamp(2.2rem, 5vw, 4.6rem); line-height: 1.08; letter-spacing: -.04em; }
.subtitle { max-width: 720px; margin: 1.2rem 0 0; font-size: 1.15rem; color: #e9fff6; }
.time-summary { display: flex; flex-wrap: wrap; gap: .7rem; margin-top: 1.8rem; }
.time-summary span { padding: .45rem .75rem; border: 1px solid rgba(255,255,255,.38); border-radius: 999px; background: rgba(255,255,255,.1); }
.layout { display: grid; grid-template-columns: 260px minmax(0, 1fr); gap: 2rem; max-width: 1240px; margin: 0 auto; padding: 2rem 1.5rem 5rem; }
.sidebar { position: sticky; top: 1rem; align-self: start; padding: 1.2rem; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); }
.sidebar h2 { margin-top: 0; font-size: 1rem; }
.sidebar nav ol { margin: 0; padding-left: 1.3rem; }
.sidebar nav a { display: block; padding: .36rem 0; text-decoration: none; }
.progress-track { height: .7rem; overflow: hidden; border-radius: 999px; background: var(--line); }
.progress-bar { width: 0; height: 100%; background: linear-gradient(90deg, var(--accent), #e5903b); transition: width .2s ease; }
.progress-text { margin: .45rem 0 1rem; color: var(--muted); font-size: .9rem; }
.reset-button { width: 100%; padding: .65rem; border: 1px solid var(--line); border-radius: 10px; background: transparent; color: var(--ink); cursor: pointer; }
.privacy { margin: 0 0 2rem; padding: 1rem 1.2rem; border-left: 5px solid var(--warm); background: var(--surface); border-radius: 0 12px 12px 0; }
.module { scroll-margin-top: 1rem; margin-bottom: 2rem; padding: clamp(1.2rem, 3vw, 2.3rem); background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); box-shadow: var(--shadow); }
.module-header { display: flex; justify-content: space-between; gap: 1rem; align-items: start; }
.eyebrow { margin: 0; color: var(--warm); font-weight: 800; font-size: .82rem; letter-spacing: .08em; text-transform: uppercase; }
h2 { margin: .25rem 0 .4rem; font-size: clamp(1.55rem, 3vw, 2.2rem); line-height: 1.2; }
.objective { margin: 0; color: var(--muted); max-width: 780px; }
.time-card { min-width: 96px; padding: .7rem; text-align: center; border-radius: 14px; color: var(--accent-strong); background: var(--accent-soft); }
.time-card strong, .time-card span { display: block; }
.time-card strong { font-size: 1.25rem; }
.time-card span { font-size: .76rem; }
.timer { display: flex; flex-wrap: wrap; gap: .55rem; align-items: center; margin: 1.3rem 0; padding: .8rem; border: 1px dashed var(--line); border-radius: 12px; }
.timer-display { min-width: 5rem; font-variant-numeric: tabular-nums; font-size: 1.15rem; font-weight: 800; }
button { font: inherit; }
.timer button { padding: .35rem .65rem; border: 1px solid var(--line); border-radius: 8px; background: var(--surface-strong); color: var(--ink); cursor: pointer; }
.concept-stack { display: grid; gap: .7rem; }
.concept { border: 1px solid var(--line); border-radius: 12px; background: var(--surface-strong); }
.concept summary { cursor: pointer; padding: .9rem 1rem; font-weight: 800; }
.concept-body { padding: 0 1rem 1rem; }
.concept-body p:first-child { margin-top: 0; }
.work-grid { display: grid; grid-template-columns: 1.15fr .85fr; gap: 1rem; margin-top: 1.2rem; }
.panel, .checkpoint { padding: 1rem; border-radius: 12px; background: color-mix(in srgb, var(--accent-soft) 55%, var(--surface)); }
.panel h3, .checkpoint h3 { margin-top: 0; }
.check-row { list-style: none; margin: .45rem 0; }
.check-row label, .artifact-check, .module-complete { display: flex; align-items: flex-start; gap: .65rem; cursor: pointer; }
input[type="checkbox"] { width: 1.15rem; height: 1.15rem; margin-top: .25rem; accent-color: var(--accent); }
.artifact { border-left: 4px solid var(--warm); }
.artifact h4 { margin-bottom: .35rem; }
.resource-links { margin-top: 0; padding-left: 1.25rem; }
.resource-links li { margin-bottom: .35rem; }
.checkpoint { margin-top: 1rem; background: var(--surface-strong); border: 1px solid var(--line); }
.checkpoint label { display: block; margin-bottom: .4rem; font-weight: 700; }
textarea { width: 100%; resize: vertical; padding: .8rem; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); color: var(--ink); font: inherit; }
.checkpoint details { margin-top: .75rem; }
.module-complete { margin-top: 1rem; padding: .85rem 1rem; border-radius: 12px; background: var(--accent); color: white; font-weight: 800; }
.references { padding: 1.5rem; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); }
.references li { margin-bottom: .7rem; }
.references span { display: block; color: var(--muted); }
.noscript { padding: 1rem; background: #ffe9c8; color: #4a270d; }
@media (max-width: 860px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { position: static; }
  .work-grid { grid-template-columns: 1fr; }
}
@media (max-width: 560px) {
  .hero { padding-top: 3.2rem; }
  .module-header { display: block; }
  .time-card { margin-top: 1rem; width: max-content; }
}
@media (prefers-reduced-motion: reduce) {
  * { scroll-behavior: auto !important; transition: none !important; }
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #101714; --surface: #17211d; --surface-strong: #1e2a25; --ink: #eef8f3;
    --muted: #b7c8c0; --line: #405149; --accent: #55c99f; --accent-strong: #8ce4c2;
    --accent-soft: #203b31; --warm: #f0a761; --shadow: 0 16px 36px rgba(0,0,0,.28);
  }
}
@media print {
  body { background: white; color: black; font-size: 10.5pt; }
  .hero { padding: 1rem 0; background: none; color: black; }
  .subtitle { color: black; }
  .layout { display: block; max-width: none; padding: 0; }
  .sidebar, .timer, .reset-button, .module-complete, textarea { display: none !important; }
  .module, .references { break-inside: avoid; box-shadow: none; border: 1px solid #aaa; }
  details, details > * { display: block !important; }
  details summary { list-style: none; }
  a { color: black; text-decoration: underline; }
}
"""


JS = r"""
(() => {
  const body = document.body;
  const storageKey = `${body.dataset.courseId}@${body.dataset.courseVersion}`;
  const stored = JSON.parse(localStorage.getItem(storageKey) || '{}');
  const controls = [...document.querySelectorAll('[data-store-id]')];

  for (const control of controls) {
    const key = control.dataset.storeId;
    if (control.type === 'checkbox') control.checked = Boolean(stored[key]);
    else if (typeof stored[key] === 'string') control.value = stored[key];
    control.addEventListener('input', () => {
      stored[key] = control.type === 'checkbox' ? control.checked : control.value;
      localStorage.setItem(storageKey, JSON.stringify(stored));
      updateProgress();
    });
  }

  function updateProgress() {
    const modules = [...document.querySelectorAll('[data-module-complete]')];
    const done = modules.filter((item) => item.checked).length;
    const percent = modules.length ? Math.round((done / modules.length) * 100) : 0;
    document.querySelector('[data-progress-bar]').style.width = `${percent}%`;
    document.querySelector('[data-progress-bar]').setAttribute('aria-valuenow', String(percent));
    document.querySelector('[data-progress-text]').textContent = `${done}/${modules.length} 블록 · ${percent}%`;
  }
  updateProgress();

  document.querySelector('[data-reset-progress]').addEventListener('click', () => {
    if (!window.confirm('이 브라우저에 저장된 체크와 메모를 모두 지우시겠습니까?')) return;
    localStorage.removeItem(storageKey);
    for (const control of controls) {
      if (control.type === 'checkbox') control.checked = false;
      else control.value = '';
    }
    updateProgress();
  });

  const timerStates = new Map();
  const formatTime = (seconds) => {
    const minutes = Math.floor(seconds / 60);
    const rest = seconds % 60;
    return `${minutes}:${String(rest).padStart(2, '0')}`;
  };
  for (const timer of document.querySelectorAll('[data-timer]')) {
    const display = timer.querySelector('[data-timer-display]');
    const initial = Number(timer.dataset.minutes) * 60;
    const state = { remaining: initial, interval: null };
    timerStates.set(timer, state);
    const render = () => { display.textContent = formatTime(state.remaining); };
    timer.addEventListener('click', (event) => {
      const action = event.target.dataset.timerAction;
      if (!action) return;
      if (action === 'start' && !state.interval && state.remaining > 0) {
        state.interval = window.setInterval(() => {
          state.remaining -= 1;
          render();
          if (state.remaining <= 0) {
            window.clearInterval(state.interval);
            state.interval = null;
            display.textContent = '완료';
          }
        }, 1000);
      }
      if (action === 'pause' && state.interval) {
        window.clearInterval(state.interval);
        state.interval = null;
      }
      if (action === 'reset') {
        if (state.interval) window.clearInterval(state.interval);
        state.interval = null;
        state.remaining = initial;
        render();
      }
    });
  }
})();
"""


def render_course(data: dict[str, Any]) -> str:
    modules = data["modules"]
    nav = "".join(
        f"<li><a href=\"#{_escape(module['id'])}\">{_escape(module['title'])}</a></li>"
        for module in modules
    )
    module_html = "".join(_render_module(module) for module in modules)
    references = "".join(
        "<li>"
        f"<a href=\"{_escape(reference['url'])}\" target=\"_blank\" rel=\"noreferrer\">{_escape(reference['title'])}</a>"
        f"<span>{_escape(reference['scope'])}</span>"
        "</li>"
        for reference in data["references"]
    )
    rendered = f"""<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light dark">
  <title>{_escape(data['title'])}</title>
  <style>{CSS}</style>
</head>
<body data-course-id="{_escape(data['course_id'])}" data-course-version="{_escape(data['version'])}">
  <a class="skip-link" href="#course-content">본문으로 건너뛰기</a>
  <noscript><div class="noscript">JavaScript가 꺼져 있어 진행률·메모·타이머는 저장되지 않습니다. 모든 개념 설명과 절차는 그대로 읽고 인쇄할 수 있습니다.</div></noscript>
  <header class="hero">
    <div class="hero-inner">
      <p class="kicker">Adaptive D2 Course · v{_escape(data['version'])}</p>
      <h1>{_escape(data['title'])}</h1>
      <p class="subtitle">{_escape(data['subtitle'])}</p>
      <div class="time-summary" aria-label="과정 시간">
        <span>핵심 Unit {data['core_minutes'] // 60}시간</span>
        <span>연결 Probe {data['probe_minutes'] // 60}시간</span>
        <span>조건부 보충 최대 {data['maximum_remediation_minutes'] // 60}시간</span>
      </div>
    </div>
  </header>

  <div class="layout">
    <aside class="sidebar" aria-label="과정 탐색과 진행률">
      <h2>학습 블록</h2>
      <nav aria-label="학습 블록"><ol>{nav}</ol></nav>
      <h2>진행률</h2>
      <div class="progress-track">
        <div class="progress-bar" data-progress-bar role="progressbar" aria-label="과정 진행률" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"></div>
      </div>
      <p class="progress-text" data-progress-text aria-live="polite">0/{len(modules)} 블록 · 0%</p>
      <button class="reset-button" type="button" data-reset-progress>로컬 진행률 초기화</button>
    </aside>

    <main id="course-content">
      <p class="privacy"><strong>개인정보 경계:</strong> {_escape(data['privacy_note'])}</p>
      {module_html}
      <section class="references" aria-labelledby="references-title">
        <h2 id="references-title">공개 근거와 선별 읽기</h2>
        <p>전체 사양을 순서대로 정독하지 않고 각 블록의 학습성과에 필요한 범위만 확인합니다.</p>
        <ul>{references}</ul>
      </section>
    </main>
  </div>
  <script>{JS}</script>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"


def build(source: Path, output: Path, *, check: bool) -> int:
    data = json.loads(source.read_text(encoding="utf-8"))
    rendered = render_course(data)
    if check:
        if not output.exists():
            print(f"COURSE_BUILD_ERROR|MISSING_OUTPUT|{output}")
            return 1
        if output.read_text(encoding="utf-8") != rendered:
            print("COURSE_BUILD_ERROR|STALE_OUTPUT|생성 HTML이 정본 콘텐츠와 다릅니다.")
            return 1
        print(f"COURSE_BUILD_SUMMARY|status=passed|modules={len(data['modules'])}|output={output.name}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"COURSE_BUILD_SUMMARY|status=generated|modules={len(data['modules'])}|output={output.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    try:
        return build(args.source, args.output, check=args.check)
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"COURSE_BUILD_ERROR|INPUT|{exc}")
        return 2


if __name__ == "__main__":
    sys.exit(main())
