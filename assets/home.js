(async () => {
  const { esc, todayKST, fmtDate, daysBetween, isUpcoming, load } = CS;
  const app = document.getElementById("app");
  let data;
  try { data = await load(); } catch (e) { app.innerHTML = '<p class="hint">모임 정보를 불러오지 못했어요. 새로고침해 주세요.</p>'; return; }
  const plan = await fetch("plan.json", { cache: "no-cache" }).then(r => r.json()).catch(() => null);
  // 학습 순서: 1주차 = plan.start, 매주 일요일 (주차에 "date"가 있으면 그 날짜)
  const addDays = (d, n) => new Date(Date.parse(d) + n * 864e5).toISOString().slice(0, 10);
  const weeks = plan ? plan.stages.flatMap((st, si) => st.weeks.map(w => ({ ...w, si, date: w.date || addDays(plan.start, 7 * (w.week - 1)) }))) : [];
  const D = data.defaults, today = todayKST();
  document.getElementById("tagline").textContent = `${D.day} ${D.time} · ${D.place}`;

  const list = data.meetings;
  const next = list.find(m => isUpcoming(m.date, today));
  const link = m => `meeting.html?d=${m.date}`;
  let html = "";

  if (next) {
    const n = daysBetween(today, next.date);
    const dday = n === 0 ? esc(next.time || D.time) : `D-${n}`;
    html += `<section class="card notice">
      <div class="top"><span class="chip red">📢 ${n === 0 ? "오늘 모임" : "다음 모임 공지"}</span><span class="dday">${dday}</span></div>
      <div class="chip yel">Ep.${esc(next.ep)} · ${esc(next.level || "A1")}</div>
      <h2>${esc(next.emoji || "")} ${esc(next.title)}</h2>
      <div class="es">${esc(next.es || "")}</div>
      <dl class="info">
        <dt>📅 일시</dt><dd>${fmtDate(next.date)} ${esc(next.time || D.time)}</dd>
        <dt>📍 장소</dt><dd><a href="${esc(next.mapUrl || D.mapUrl)}" target="_blank" rel="noopener">${esc(next.place || D.place)}</a></dd>
        <dt>🎒 준비물</dt><dd>${esc(next.bring || D.bring)}</dd>
      </dl>
      ${next.notice ? `<div class="msg">${esc(next.notice)}</div>` : ""}
      ${next.topics ? `<b style="font-size:14px">이번 주에 배울 내용</b><ul class="topics">${next.topics.map(t => `<li>${esc(t)}</li>`).join("")}</ul>` : ""}
      ${next.extras && next.extras.length ? `<b style="font-size:14px;display:block;margin-top:14px">추가 자료</b><div class="extras">${next.extras.map((e, i) => `<a href="${link(next)}&x=${encodeURIComponent(e.id)}">
          <span class="em">${esc(e.emoji || "📎")}</span><span><span class="d">자료 ${i + 2}${e.channel ? " · " + esc(e.channel) : ""}${e.duration ? " · " + esc(e.duration) : ""}</span><br>
          <span class="t">${esc(e.title)}</span><br><span class="d">${esc(e.es || "")}</span></span></a>`).join("")}</div>` : ""}
      <div class="btns">
        <a class="btn primary" href="${link(next)}#listen">🎧 예습하기</a>
        <a class="btn ghost" href="${link(next)}#book">📘 교재 보기</a>
      </div>
    </section>`;
  } else {
    const pw = weeks.find(w => isUpcoming(w.date, today));
    html += `<section class="card notice"><div class="top"><span class="chip red">📢 다음 모임</span>${pw ? `<span class="dday">D-${daysBetween(today, pw.date)}</span>` : ""}</div>
      ${pw ? `<div class="chip yel">${pw.week}주차 · Ep.${pw.ep} · A1</div><h2>${esc(pw.emoji)} ${esc(pw.title)}</h2>
        <div class="msg">${fmtDate(pw.date)} 모임은 학습 순서에 따라 이 주제로 해요. 자세한 자료는 곧 올라와요. 먼저 <a href="https://www.youtube.com/watch?v=${esc(pw.youtube)}" target="_blank" rel="noopener">유튜브 영상</a>을 들어 봐도 좋아요!</div>`
      : `<h2>다음 모임 내용은 곧 공지돼요</h2>`}
      <dl class="info"><dt>📅 일시</dt><dd>${pw ? fmtDate(pw.date) : esc(D.day)} ${esc(D.time)}</dd>
      <dt>📍 장소</dt><dd><a href="${esc(D.mapUrl)}" target="_blank" rel="noopener">${esc(D.place)}</a></dd>
      <dt>🎒 준비물</dt><dd>${esc(D.bring)}</dd></dl></section>`;
  }

  html += "<!--plan-->";

  const item = (m, chip) => `<a class="mitem" href="${link(m)}">
      <div class="em">${esc(m.emoji || "📗")}</div>
      <div><div class="d">${fmtDate(m.date)} · Ep.${esc(m.ep)} ${chip}</div>
      <div class="t">${esc(m.title)}</div><div class="d">${esc(m.es || "")}${m.extras && m.extras.length ? ` · 📎 추가 자료 ${m.extras.length}개` : ""}</div></div>
      <div class="go">›</div></a>`;
  const upcoming = list.filter(m => isUpcoming(m.date, today) && m !== next);
  const past = list.filter(m => !isUpcoming(m.date, today)).reverse();
  if (upcoming.length) html += `<h3 class="sec">예정된 모임</h3><div class="mlist">${upcoming.map(m => item(m, '<span class="chip">예정</span>')).join("")}</div>`;
  if (next) html += `<h3 class="sec">${past.length ? "모든 모임 자료" : "모임 자료"}</h3><div class="mlist">${item(next, `<span class="chip red">${next.date === today ? "오늘" : "다음"}</span>`)}${past.map(m => item(m, '<span class="chip gray">지난 모임</span>')).join("")}</div>`;
  else html += `<h3 class="sec">지난 모임 자료</h3><div class="mlist">${past.map(m => item(m, '<span class="chip gray">지난 모임</span>')).join("")}</div>`;

  // ---------- A1 학습 순서 (공지 카드 바로 아래) ----------
  let planHtml = "";
  if (weeks.length) {
    const done = weeks.filter(w => !isUpcoming(w.date, today)).length;
    const curW = weeks[done];
    const mByDate = Object.fromEntries(list.map(m => [m.date, m]));
    planHtml = `<h3 class="sec">📚 ${esc(plan.title)} · ${weeks.length}주</h3>
    <section class="card plan">
      <p class="pnote">${esc(plan.note)}</p>
      <div class="pbar" role="progressbar" aria-valuemin="0" aria-valuemax="${weeks.length}" aria-valuenow="${done}"><i style="width:${(done / weeks.length * 100).toFixed(1)}%"></i></div>
      <div class="pstat">${done} / ${weeks.length}주 완료${curW ? ` · 이번 주는 <b>${curW.week}주차 ${esc(curW.title)}</b>` : " · 🎉 A1 완주!"}</div>
      ${plan.stages.map((st, si) => {
        const ws = weeks.filter(w => w.si === si);
        const open = curW ? curW.si === si : si === plan.stages.length - 1;
        const nDone = ws.filter(w => !isUpcoming(w.date, today)).length;
        return `<details class="stage"${open ? " open" : ""}><summary><span>${esc(st.title)}</span><span class="sc">${nDone === ws.length ? "✅" : `${nDone}/${ws.length}`}</span></summary>
          ${ws.map(w => {
            const st2 = w === curW ? "cur" : isUpcoming(w.date, today) ? "" : "done";
            const m = mByDate[w.date];
            const href = m ? `meeting.html?d=${w.date}` : `https://www.youtube.com/watch?v=${esc(w.youtube)}`;
            return `<a class="wk ${st2}" href="${href}"${m ? "" : ' target="_blank" rel="noopener"'}>
              <span class="n">${w.week}주차</span><span class="em">${esc(w.emoji)}</span>
              <span class="b"><span class="t">${esc(w.title)}</span><span class="d">${fmtDate(w.date)} · Ep.${w.ep}${m ? " · 📘 자료" : " · ▶ 유튜브"}${w.tip ? " · " + esc(w.tip) : ""}</span></span>
              <span class="st">${st2 === "done" ? "✓" : st2 === "cur" ? "이번 주" : ""}</span></a>`;
          }).join("")}</details>`;
      }).join("")}
      <a class="btn ghost plist" href="${esc(plan.playlist)}" target="_blank" rel="noopener">▶ 유튜브 플레이리스트 전체 보기</a>
    </section>`;
  }

  app.innerHTML = html.replace("<!--plan-->", planHtml);
  document.getElementById("foot").innerHTML =
    `팟캐스트 출처: <a href="${esc(data.site.sourceUrl)}" target="_blank" rel="noopener">${esc(data.site.source)}</a><br>
     문장별 한국어 번역과 교재는 스터디 학습용으로 만든 자료예요.`;
})();
