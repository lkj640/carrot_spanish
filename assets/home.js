(async () => {
  const { esc, todayKST, fmtDate, daysBetween, isUpcoming, load } = CS;
  const app = document.getElementById("app");
  let data;
  try { data = await load(); } catch (e) { app.innerHTML = '<p class="hint">모임 정보를 불러오지 못했어요. 새로고침해 주세요.</p>'; return; }
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
      <div class="btns">
        <a class="btn primary" href="${link(next)}#listen">🎧 예습하기</a>
        <a class="btn ghost" href="${link(next)}#book">📘 교재 보기</a>
      </div>
    </section>`;
  } else {
    html += `<section class="card notice"><div class="top"><span class="chip red">📢 다음 모임</span></div>
      <h2>다음 모임 내용은 곧 공지돼요</h2>
      <dl class="info"><dt>📅 일시</dt><dd>${esc(D.day)} ${esc(D.time)}</dd>
      <dt>📍 장소</dt><dd><a href="${esc(D.mapUrl)}" target="_blank" rel="noopener">${esc(D.place)}</a></dd>
      <dt>🎒 준비물</dt><dd>${esc(D.bring)}</dd></dl></section>`;
  }

  const item = (m, chip) => `<a class="mitem" href="${link(m)}">
      <div class="em">${esc(m.emoji || "📗")}</div>
      <div><div class="d">${fmtDate(m.date)} · Ep.${esc(m.ep)} ${chip}</div>
      <div class="t">${esc(m.title)}</div><div class="d">${esc(m.es || "")}</div></div>
      <div class="go">›</div></a>`;
  const upcoming = list.filter(m => isUpcoming(m.date, today) && m !== next);
  const past = list.filter(m => !isUpcoming(m.date, today)).reverse();
  if (upcoming.length) html += `<h3 class="sec">예정된 모임</h3><div class="mlist">${upcoming.map(m => item(m, '<span class="chip">예정</span>')).join("")}</div>`;
  if (next) html += `<h3 class="sec">${past.length ? "모든 모임 자료" : "모임 자료"}</h3><div class="mlist">${item(next, `<span class="chip red">${next.date === today ? "오늘" : "다음"}</span>`)}${past.map(m => item(m, '<span class="chip gray">지난 모임</span>')).join("")}</div>`;
  else html += `<h3 class="sec">지난 모임 자료</h3><div class="mlist">${past.map(m => item(m, '<span class="chip gray">지난 모임</span>')).join("")}</div>`;

  app.innerHTML = html;
  document.getElementById("foot").innerHTML =
    `팟캐스트 출처: <a href="${esc(data.site.sourceUrl)}" target="_blank" rel="noopener">${esc(data.site.source)}</a><br>
     문장별 한국어 번역과 교재는 스터디 학습용으로 만든 자료예요.`;
})();
