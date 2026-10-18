// 공통 도우미: 날짜(한국 시간 기준)·HTML 이스케이프·모임 목록 불러오기
const CS = (() => {
  const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  const todayKST = () => new Intl.DateTimeFormat("en-CA", { timeZone: "Asia/Seoul" }).format(new Date()); // YYYY-MM-DD
  const WD = ["일", "월", "화", "수", "목", "금", "토"];
  const parts = d => { const [y, m, dd] = d.split("-").map(Number); return { y, m, d: dd, wd: WD[new Date(Date.UTC(y, m - 1, dd)).getUTCDay()] }; };
  const fmtDate = d => { const p = parts(d); return `${p.m}월 ${p.d}일 (${p.wd})`; };
  // 모임 당일은 낮 12시(한국 시간)까지 '오늘 모임'으로 보여 주고, 그 뒤에는 다음 모임을 공지해요.
  const hourKST = () => +new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Seoul", hour: "2-digit", hour12: false }).format(new Date());
  const isUpcoming = (d, today) => d > today || (d === today && hourKST() < 12);
  const daysBetween = (a, b) => Math.round((Date.parse(b) - Date.parse(a)) / 864e5);
  const store = {
    get(k, def) { try { const v = localStorage.getItem(k); return v === null ? def : JSON.parse(v); } catch { return def; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} },
  };
  async function load() {
    const r = await fetch("meetings.json", { cache: "no-cache" });
    const j = await r.json();
    j.meetings.sort((a, b) => a.date.localeCompare(b.date));
    return j;
  }
  return { esc, todayKST, fmtDate, daysBetween, isUpcoming, store, load };
})();
