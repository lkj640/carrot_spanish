(async () => {
  const { esc, fmtDate, store, load } = CS;
  const $ = id => document.getElementById(id);
  const fmt = t => { t = Math.max(0, t | 0); return (t / 60 | 0) + ":" + String(t % 60).padStart(2, "0"); };

  // ---------- 모임 정보 ----------
  const site = await load().catch(() => null);
  const date = new URLSearchParams(location.search).get("d");
  const qs = new URLSearchParams(location.search);
  const mm = site && site.meetings.find(x => x.date === date);
  // 추가 자료: meeting.html?d=날짜&x=자료id → meetings/<날짜>/<자료id>/data.json
  const ex = mm && qs.get("x") ? (mm.extras || []).find(e => e.id === qs.get("x")) : null;
  const m = ex ? { date: mm.date, ep: mm.ep, ...ex } : mm;
  if (!m || (qs.get("x") && !ex)) { $("hero").innerHTML = '<h1>모임을 찾을 수 없어요</h1><p><a href="./">홈으로 돌아가기</a></p>'; document.querySelectorAll(".pane,.bar,.tabs").forEach(e => e.remove()); return; }
  const base = `meetings/${m.date}/` + (ex ? ex.id + "/" : "");
  const channel = m.channel || "Easy Spanish Podcast";
  document.title = `${fmtDate(m.date)} · ${m.title} · 당근 스페인어 스터디`;
  $("ttl").textContent = `${fmtDate(m.date)} · ` + (ex ? `자료 ${mm.extras.indexOf(ex) + 2}` : `Ep.${m.ep}`);
  // 같은 모임의 자료(본 자료 + 추가 자료) 사이를 오가는 버튼
  const mats = mm.extras && mm.extras.length ? [{ href: `meeting.html?d=${mm.date}`, on: !ex, label: `${mm.emoji || ""} 자료 1 · Ep.${mm.ep}` },
    ...mm.extras.map((e, i) => ({ href: `meeting.html?d=${mm.date}&x=${encodeURIComponent(e.id)}`, on: ex === e, label: `${e.emoji || "📎"} 자료 ${i + 2}${e.short ? " · " + e.short : ""}` }))] : [];
  $("hero").innerHTML = `<span class="chip yel">${esc(channel)}${ex ? "" : " · Ep." + esc(m.ep)} · ${esc(m.level || "A1")}${m.duration ? " · " + esc(m.duration) : ""}</span>
    <h1>${esc(m.emoji || "")} ${esc(m.title)}</h1><div class="es">${esc(m.es || "")}</div>
    ${mats.length ? `<nav class="mats">${mats.map(x => `<a href="${x.href}"${x.on ? ' aria-current="page"' : ""}>${esc(x.label)}</a>`).join("")}</nav>` : ""}`;
  // 교재가 없는 자료는 교재 탭을 숨겨요.
  if (!m.pdf && !m.workbookHtml && !m.pages) document.querySelector('.tabs [data-tab="book"]').remove();

  // ---------- 탭 ----------
  const tabs = [...document.querySelectorAll(".tabs button")];
  function showTab(name) {
    if (!tabs.some(b => b.dataset.tab === name)) name = "listen";
    tabs.forEach(b => b.setAttribute("aria-selected", b.dataset.tab === name));
    document.querySelectorAll(".pane").forEach(p => p.classList.toggle("on", p.id === "pane-" + name));
    if (name === "book") loadBook();
    window.scrollTo(0, 0);
  }
  tabs.forEach(b => b.onclick = () => { history.replaceState(null, "", "#" + b.dataset.tab); showTab(b.dataset.tab); });
  window.addEventListener("hashchange", () => showTab(location.hash.slice(1)));

  // ---------- 대본 ----------
  const data = await fetch(base + "data.json").then(r => r.json());
  const who = Object.assign({ S: "Sofía", M: "Mateo" }, data.speakers);
  let html = "", opts = '<option value="">📍 구간으로 이동…</option>', n = 0;
  data.sections.forEach((s, si) => {
    html += `<h2 class="secT" id="sec${si}">${esc(s.title)}</h2>`;
    opts += `<option value="${si}">${esc(s.title)}</option>`;
    for (const l of s.lines) {
      html += `<div class="line ${l.s}" data-i="${n++}" data-t="${l.t}"><div class="who">${esc(who[l.s] || l.s)}<span class="ts">${fmt(l.t)}</span></div>
        <div class="txt"><div class="es">${esc(l.es)}</div><div class="ko">${esc(l.ko)}</div></div></div>`;
    }
  });
  $("lines").innerHTML = html;
  $("jump").innerHTML = opts;
  $("jump").onchange = e => { const v = e.target.value; if (v !== "") { $("sec" + v).scrollIntoView({ behavior: "smooth" }); e.target.value = ""; } };
  const lines = [...document.querySelectorAll(".line")];
  const T = lines.map(l => +l.dataset.t);

  // ---------- 재생 엔진 (유튜브 / MP3) ----------
  const au = $("au");
  let yt = null, ytReady = false, ytState = -1, ytPromise = null;
  const hasMp3 = !!m.audio, hasYt = !!m.youtube;
  let mode = store.get("cs_src", "yt");
  if (mode === "yt" && !hasYt) mode = "mp3";
  if (mode === "mp3" && !hasMp3) mode = "yt";

  const E = {
    time: () => mode === "yt" ? (ytReady ? yt.getCurrentTime() || 0 : 0) : au.currentTime,
    dur: () => mode === "yt" ? (ytReady ? yt.getDuration() || 0 : 0) : (au.duration || 0),
    paused: () => mode === "yt" ? !(ytState === 1 || ytState === 3) : au.paused,
    async play() {
      if (mode === "yt") { await ensureYT(); yt.playVideo(); watchIOS(); }
      else { try { await au.play(); } catch {} }
    },
    pause() { if (mode === "yt") { ytReady && yt.pauseVideo(); } else au.pause(); },
    async seek(t) {
      if (mode === "yt") { await ensureYT(); yt.seekTo(t, true); return; }
      if (au.readyState < 1) await new Promise(r => au.addEventListener("loadedmetadata", r, { once: true }));
      au.currentTime = t;
    },
    rate(r) { if (mode === "yt") { ytReady && yt.setPlaybackRate(r); } else au.playbackRate = r; },
  };

  function ensureYT() {
    if (ytPromise) return ytPromise;
    ytPromise = new Promise(res => {
      window.onYouTubeIframeAPIReady = () => {
        yt = new YT.Player("yt", {
          videoId: m.youtube, host: "https://www.youtube-nocookie.com",
          playerVars: { playsinline: 1, rel: 0, modestbranding: 1 },
          events: {
            onReady: () => { ytReady = true; E.rate(+$("rate").value); res(); },
            onStateChange: e => { ytState = e.data; updPlayBtn(); },
          },
        });
      };
      const s = document.createElement("script");
      s.src = "https://www.youtube.com/iframe_api";
      document.head.appendChild(s);
    });
    return ytPromise;
  }
  // 아이폰 등에서는 처음 한 번은 영상 화면을 직접 눌러야 재생되는 경우가 있어요.
  function watchIOS() {
    setTimeout(() => {
      if (mode === "yt" && ytState !== 1 && ytState !== 3) {
        $("srcHint").innerHTML = "⚠ 재생이 시작되지 않으면 <b>위 영상 화면의 ▶를 한 번 직접 눌러</b> 주세요. 그다음부터는 문장을 누르면 바로 재생돼요.";
        $("ytbox").scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }, 1500);
  }

  function setMode(next, keepTime) {
    const t = keepTime ? E.time() : 0, wasPlaying = !E.paused();
    E.pause();
    mode = next; store.set("cs_src", mode);
    document.querySelectorAll("#srcSel button").forEach(b => b.setAttribute("aria-pressed", b.dataset.src === mode));
    $("ytbox").style.display = mode === "yt" ? "" : "none";
    $("srcHint").innerHTML = mode === "yt"
      ? `유튜브 공식 영상(<a href="https://www.youtube.com/watch?v=${esc(m.youtube)}" target="_blank" rel="noopener">${esc(channel)}</a>)으로 재생해요. 화면을 끄면 멈출 수 있어요.`
      : "MP3로 재생해요. 화면을 꺼도 계속 들을 수 있어요.";
    if (mode === "mp3" && !au.src) au.src = base + m.audio;
    if (mode === "yt") ensureYT();
    if (t > 0) E.seek(t).then(() => wasPlaying && E.play());
    updPlayBtn();
  }
  document.querySelectorAll("#srcSel button").forEach(b => {
    if ((b.dataset.src === "yt" && !hasYt) || (b.dataset.src === "mp3" && !hasMp3)) b.disabled = true;
    b.onclick = () => b.dataset.src !== mode && setMode(b.dataset.src, true);
  });
  if (!(hasYt && hasMp3)) $("srcSel").style.display = "none";

  // ---------- 화면 동기화 ----------
  let cur = -1, loopIdx = -1, seeking = false;
  const idxAt = t => { let lo = 0, hi = T.length - 1, r = -1; while (lo <= hi) { const k = (lo + hi) >> 1; if (T[k] <= t + 0.05) { r = k; lo = k + 1; } else hi = k - 1; } return r; };
  const lineEnd = i => i + 1 < T.length ? T[i + 1] : (E.dur() || 1e9);
  function setActive(i) {
    if (i === cur) return;
    if (cur >= 0) lines[cur].classList.remove("active");
    cur = i;
    if (i < 0) return;
    const l = lines[i]; l.classList.add("active");
    $("now").textContent = l.querySelector(".who").firstChild.textContent + ": " + l.querySelector(".es").textContent;
    if ($("optScroll").checked && !E.paused() && $("pane-listen").classList.contains("on")) {
      const r = l.getBoundingClientRect(), barH = document.querySelector(".bar").offsetHeight;
      if (r.top < 120 || r.bottom > innerHeight - barH - 20) l.scrollIntoView({ behavior: "smooth", block: "center" });
    }
  }
  function updPlayBtn() {
    const p = E.paused();
    $("btnPlay").textContent = p ? "▶" : "❚❚";
    $("btnPlay").setAttribute("aria-label", p ? "재생" : "일시정지");
  }
  setInterval(() => {
    const t = E.time(), d = E.dur();
    if (d && +$("seek").max !== d) { $("seek").max = d; $("dur").textContent = fmt(d); }
    if ($("optLoop").checked && loopIdx >= 0 && !E.paused() && t >= lineEnd(loopIdx) - 0.05) { E.seek(T[loopIdx]); return; }
    if (!seeking) $("seek").value = t;
    $("cur").textContent = fmt(t);
    setActive(idxAt(t));
  }, 200);
  ["play", "pause", "ended"].forEach(ev => au.addEventListener(ev, updPlayBtn));
  au.addEventListener("error", () => { if (mode === "mp3") $("now").textContent = "⚠ 음성 파일을 불러오지 못했어요. 유튜브로 듣기를 이용해 주세요."; });

  async function playLine(i) {
    i = Math.max(0, Math.min(lines.length - 1, i));
    loopIdx = i; setActive(i);
    await E.seek(T[i]); E.play();
  }
  lines.forEach((l, i) => l.addEventListener("click", () => playLine(i)));
  $("btnPlay").onclick = () => E.paused() ? E.play() : E.pause();
  $("btnPrev").onclick = () => playLine((cur < 0 ? 0 : cur) - 1);
  $("btnNext").onclick = () => playLine(cur + 1);
  $("seek").addEventListener("input", e => { seeking = true; $("cur").textContent = fmt(+e.target.value); });
  $("seek").addEventListener("change", e => { E.seek(+e.target.value); seeking = false; loopIdx = idxAt(+e.target.value); });
  $("rate").onchange = e => E.rate(+e.target.value);
  $("optKo").checked = store.get("cs_ko", true);
  document.body.classList.toggle("noko", !$("optKo").checked);
  $("optKo").onchange = e => { document.body.classList.toggle("noko", !e.target.checked); store.set("cs_ko", e.target.checked); };
  $("optLoop").onchange = e => { loopIdx = e.target.checked ? Math.max(cur, 0) : -1; };
  document.addEventListener("keydown", e => {
    if (e.code === "Space" && !/INPUT|SELECT|BUTTON|TEXTAREA/.test(e.target.tagName)) { e.preventDefault(); $("btnPlay").click(); }
  });
  setMode(mode, false);

  // ---------- 교재 ----------
  let bookLoaded = false;
  async function loadBook() {
    if (bookLoaded) return; bookLoaded = true;
    $("wbtools").innerHTML = m.pdf ? `<a class="btn ghost" href="${base + m.pdf}" target="_blank" rel="noopener">📄 PDF 열기</a>
      <a class="btn primary" href="${base + m.pdf}" download="스페인어_교재_${m.date}_Ep${m.ep}.pdf">⬇ PDF 저장</a>` : "";
    const wb = $("wb");
    if (m.workbookHtml) {
      wb.innerHTML = '<p class="hint">교재를 불러오는 중…</p>';
      const src = await fetch(base + m.workbookHtml).then(r => r.text());
      const doc = new DOMParser().parseFromString(src, "text/html");
      const css = [...doc.querySelectorAll("style")].map(s => s.textContent).join("\n").replace(/(^|[}\s,])body\{/g, "$1.wbroot{");
      const host = document.createElement("div"); host.className = "wbhost";
      const root = host.attachShadow({ mode: "open" });
      root.innerHTML = `<style>${css}.wbroot{padding-top:4px}</style><div class="wbroot">${doc.body.innerHTML}</div>`;
      wb.replaceChildren(host);
      const p = document.createElement("p"); p.className = "hint";
      p.textContent = "빈칸 문제는 PDF를 인쇄하거나, 노트에 따로 써 보세요. 정답은 교재 맨 뒤 부록에 있어요.";
      wb.prepend(p);
    } else if (m.pages) {
      let im = '<p class="hint">페이지를 누르면 크게 볼 수 있어요. (두 손가락으로 확대 가능)</p><div class="pages">';
      for (let i = 1; i <= m.pages; i++) {
        const f = `${base}pages/p${String(i).padStart(2, "0")}.jpg`;
        im += `<a href="${f}" target="_blank" rel="noopener"><img src="${f}" loading="lazy" alt="교재 ${i}쪽"></a>`;
      }
      wb.innerHTML = im + "</div>";
    } else wb.innerHTML = '<p class="hint">이번 주 교재는 준비 중이에요.</p>';
  }

  // ---------- 단어장 ----------
  const vkey = "cs_vocab_" + m.date + (ex ? "_" + ex.id : "");
  const known = new Set(store.get(vkey, []));
  let vh = "";
  data.vocab.forEach((g, gi) => {
    vh += `<div class="vgroup"><h3>${esc(g.title)}</h3>`;
    g.rows.forEach(([w, mean], ri) => {
      const id = gi + "-" + ri;
      vh += `<label class="vrow${known.has(id) ? " done" : ""}" data-id="${id}"><input type="checkbox"${known.has(id) ? " checked" : ""} aria-label="외웠어요">
        <span class="w">${esc(w)}</span><span class="m">${esc(mean)}</span></label>`;
    });
    vh += "</div>";
  });
  $("vlist").innerHTML = vh;
  const total = document.querySelectorAll(".vrow").length;
  const prog = () => $("vprog").textContent = `외운 단어 ${known.size} / ${total}개 · 체크한 기록은 이 기기에만 저장돼요.`;
  prog();
  $("vlist").addEventListener("change", e => {
    const row = e.target.closest(".vrow"); const id = row.dataset.id;
    e.target.checked ? known.add(id) : known.delete(id);
    row.classList.toggle("done", e.target.checked);
    store.set(vkey, [...known]); prog();
  });
  $("vlist").addEventListener("click", e => {
    if (e.target.classList.contains("m") && document.body.classList.contains("hidemean")) { e.preventDefault(); e.target.closest(".vrow").classList.toggle("peek"); }
  });
  const tog = (btn, cls) => { const on = btn.getAttribute("aria-pressed") !== "true"; btn.setAttribute("aria-pressed", on); document.body.classList.toggle(cls, on); };
  $("vHide").onclick = e => { tog(e.currentTarget, "hidemean"); document.querySelectorAll(".vrow.peek").forEach(r => r.classList.remove("peek")); };
  $("vUndone").onclick = e => tog(e.currentTarget, "undone");

  showTab(location.hash.slice(1));
})();
