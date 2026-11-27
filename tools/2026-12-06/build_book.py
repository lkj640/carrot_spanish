import json, sys, html
work, times_f, out = sys.argv[1:4]
sys.path.insert(0, work)
from lines import L
from vocab import VOCAB

T = {int(k): v for k, v in json.load(open(times_f)).items()}
fmt = lambda t: f"{int(t)//60}:{int(t)%60:02d}"
e = lambda s: html.escape(s, quote=False)

def find(prefix, after=0):
    for i, x in enumerate(L):
        if i >= after and x[0] != "H" and x[1].startswith(prefix):
            return i
    raise KeyError(prefix)

def sec_start(n):
    for i, x in enumerate(L):
        if x[0] == "H" and x[1].startswith(f"{n}."):
            return T[i + 1]
END = 10 * 60 + 59

def rng(a, b):
    return f"{fmt(sec_start(a))}–{fmt(sec_start(b)) if b else fmt(END)}"

def dlg(*prefixes, after=0):
    rows = []
    for p in prefixes:
        i = find(p, after)
        sp, es, ko = L[i][:3]
        who = "Sofía" if sp == "S" else "Mateo"
        rows.append(f'<div class="dl"><div class="dw {sp}">{who}<span>{fmt(T[i])}</span></div>'
                    f'<div><b>{e(es)}</b><small>{e(ko)}</small></div></div>')
    return '<div class="dlg">' + "".join(rows) + "</div>"

def ask(*qs):
    rows = []
    for who, q in qs:
        rows.append(f'<div class="dl"><div class="dw {who[0]}">{who}</div><div><b>{q}</b></div></div>'
                    f'<div class="dl"><div class="dw T">Tú</div><div class="ans"></div></div>')
    return '<div class="dlg">' + "".join(rows) + "</div>"

def lesson(no, rng_, title, sub, goals):
    g = "".join(f"<li>{x}</li>" for x in goals)
    return (f'<section class="lesson"><div class="hd"><div class="k">LESSON {no} · {rng_}</div><h1>{title}</h1>'
            f'<div class="s">{sub}</div></div><div class="goal"><b>오늘의 목표</b><ul>{g}</ul></div>')

def h(tag, title, cls=""):
    return f'<h2 class="{cls}"><span class="tag">{tag}</span>{title}</h2>'

def blanks(items, start=1):
    return '<ol class="q">' + "".join(f"<li><span class=n>{i}</span>{x}</li>" for i, x in enumerate(items, start)) + "</ol>"

B = '<span class="bl"></span>'
BS = '<span class="bl s"></span>'

P = []
# ---------- cover ----------
P.append(f"""<section class="cover"><div class="stripe"></div>
<div class="ct"><h1>왕초보 스페인어<br>주말 이야기</h1>
<div class="cs">Easy Spanish Podcast Ep.13 · A1 입문 · 8주차</div>
<div class="big">¿Qué haces el fin de semana?</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · el sábado (토요일에) · 불규칙 yo 동사 (hago, salgo, veo)</td></tr>
<tr><th>LESSON 1</th><td>토요일 아침 · Me levanto temprano / tarde · Hago deporte</td></tr>
<tr><th>LESSON 2</th><td>토요일 오후와 일요일 · Voy de compras · Me encuentro con amigos · Me relajo</td></tr>
<tr><th>LESSON 3</th><td>지난 주말과 이번 주말 · Fui, vi, hice, comí ↔ Voy a + 동사원형</td></tr>
<tr><th>LESSON 4</th><td>약속 잡기 · ¿Qué te parece si…? · 나의 주말 발표</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 12월 6일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기 · 11분짜리 에피소드예요</div></div>
<div class="stripe"></div></section>""")

# ---------- intro ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 주말을 말하는 세 가지 시간</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. 7주차 <b>하루 일과</b>에 이어 이번 주는 <b>주말</b>이에요. 지난주에 배운 me levanto, me ducho, desayuno가 다시 나와요!</div>
""" + h("발음", "이번 에피소드에 나오는 주의할 소리") + """
<table class="t"><tr><th>글자</th><th>소리</th><th>예</th></tr>
<tr><td><b>j</b> / <b>g + e, i</b></td><td>목에서 나는 'ㅎ'</td><td><b>j</b>untos 훈또스 · ho<b>j</b>a · <b>g</b>ente</td></tr>
<tr><td><b>h</b></td><td>소리 없음</td><td><b>h</b>ago 아고 · <b>h</b>ice 이세 · <b>h</b>ermana 에르마나</td></tr>
<tr><td><b>qu</b></td><td>'ㄲ' (u는 안 읽어요)</td><td><b>qu</b>é 께 · <b>qu</b>edarse 께다르세 · par<b>qu</b>e</td></tr>
<tr><td><b>강세</b></td><td>표시된 곳을 세게 — 과거형은 끝!</td><td>s<b>á</b>bado · pel<b>í</b>cula · com<b>í</b> · dorm<b>í</b> · pr<b>ó</b>ximo</td></tr>
</table>
""" + h("문법 0-①", "요일 앞에는 el — '토요일에'에 전치사가 필요 없어요") + """
<div class="two"><div class="box y"><b>그 날 한 번</b>
<p><b>El sábado</b> me levanto temprano.<br>토요일에 일찍 일어나요. ('en el sábado' ✗)</p></div>
<div class="box y"><b>매주 (습관)</b>
<p><b>Los sábados</b> hago deporte.<br>토요일마다 운동해요.<br><b>El fin de semana</b> 주말에 · <b>los fines de semana</b> 주말마다</p></div></div>
""" + h("문법 0-②", "주말을 말하는 세 가지 시간") + """
<table class="t"><tr><th>언제</th><th>형태</th><th>예문</th></tr>
<tr><td>평소 (현재)</td><td>현재형</td><td>El sábado <b>hago</b> deporte. 토요일에 운동해요.</td></tr>
<tr><td>지난 주말 (과거)</td><td>과거형</td><td>El sábado pasado <b>hice</b> deporte. 지난 토요일에 운동했어요.</td></tr>
<tr><td>이번 주말 (계획)</td><td><b>voy a</b> + 동사원형</td><td>Este sábado <b>voy a hacer</b> deporte. 이번 토요일에 운동할 거예요.</td></tr></table>

<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 토요일엔 늦잠(10~11시), 오후엔 쇼핑과 친구, 일요일엔 가족과 함께 · 조용한 게 좋아요. · <b class="cM">Mateo</b> — 토요일엔 일찍 일어나 운동, 일요일엔 신문·시장·영화 · 운동과 낮잠을 좋아해요. · <b class="cT">Tú (나)</b> — 나의 주말을 말할 청취자!</p>
</section>""")

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 4), "토요일 아침", "팟캐스트 1. 오프닝 · 2. 마테오의 토요일 아침 · 3. 소피아의 토요일",
    ["<b>¿Qué haces el fin de semana?</b>에 <b>El sábado …</b>로 대답할 수 있다.", "<b>temprano / tarde</b>, <b>me gusta + 동사원형</b>으로 주말 아침을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("¿Cansado? ¿Qué haces", "Ah, el fin de semana es mi parte", "El sábado me levanto temprano", "¿Temprano?", "Sí, temprano. Me gusta", "Voy al parque, corro", "¡Qué bien! ¿Y después", "Después me ducho", "Entiendo. Yo el sábado", "Sí, me levanto a las diez")
 + h("문법", "me gusta + 동사원형 — '…하는 걸 좋아해요'")
 + """<table class="t"><tr><th>스페인어</th><th>뜻</th></tr>
<tr><td>Me gusta <b>hacer</b> deporte.</td><td>운동하는 걸 좋아해요.</td></tr>
<tr><td>Me gusta <b>dormir</b> mucho.</td><td>많이 자는 걸 좋아해요.</td></tr>
<tr><td>Me gusta <b>preparar</b> la cena.</td><td>저녁 준비하는 걸 좋아해요.</td></tr>
<tr><td><b>No</b> me gusta <b>levantarme</b> temprano.</td><td>일찍 일어나는 걸 안 좋아해요.</td></tr></table>
<div class="note g"><b>temprano ↔ tarde</b> Me levanto <b>temprano</b>. 일찍 일어나요. · Me levanto <b>tarde</b>. 늦게 일어나요.
<br>※ tarde는 '늦게'와 '오후(la tarde)' 두 가지 뜻이 있어요. <b>por la tarde</b> 오후에.</div>"""
 + h("연습 A", "temprano 또는 tarde를 쓰세요.")
 + blanks([f"Mateo se levanta {B} el sábado. (7시)", f"Sofía se levanta {B} el sábado. (11시)", f"Yo me levanto {B} el domingo. (나의 경우)"])
 + h("연습 B", "그림을 보고 'Me gusta + 동사원형'으로 쓰세요.")
 + blanks([f"🏃 Me gusta {B}.", f"🚲 Me gusta {B} en bicicleta.", f"😴 Me gusta {B} mucho."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Qué haces el fin de semana normalmente?"), ("Mateo", "¿Te levantas temprano o tarde el sábado?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(4, 7), "토요일 오후와 일요일", "팟캐스트 4. 토요일 오후 · 5. 일요일 · 6. 여러분은 주말에 뭐 해요?",
    ["<b>voy de compras, me encuentro con mis amigos, leo, veo, me relajo</b>로 주말 활동을 말할 수 있다.", "<b>a veces</b>(가끔)를 넣어 얼마나 자주 하는지 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("¿Y qué haces el sábado por la tarde", "Por la tarde a veces voy", "Vamos a un café, hablamos", "Yo por la tarde a veces también", "El domingo es un día", "Por la mañana leo", "Por la tarde me relajo", "Yo el domingo paso tiempo", "Por la noche me gusta preparar", "Sí, me gusta mucho la tranquilidad")
 + h("표현", "주말 활동 모음")
 + """<table class="t"><tr><td>🛍️ <b>Voy de compras.</b></td><td>쇼핑하러 가요.</td><td>👫 <b>Me encuentro con mis amigos.</b></td><td>친구들을 만나요.</td></tr>
<tr><td>☕ <b>Tomo algo.</b></td><td>뭘 좀 마셔요.</td><td>🍽️ <b>Voy a un restaurante.</b></td><td>식당에 가요.</td></tr>
<tr><td>📰 <b>Leo el periódico.</b></td><td>신문을 읽어요.</td><td>🥕 <b>Voy al mercado.</b></td><td>시장에 가요.</td></tr>
<tr><td>🎬 <b>Veo una película / una serie.</b></td><td>영화 / 드라마를 봐요.</td><td>🛋️ <b>Me relajo.</b></td><td>쉬어요.</td></tr>
<tr><td>👨‍👩‍👧 <b>Paso tiempo con mi familia.</b></td><td>가족과 시간을 보내요.</td><td>🚶 <b>Camino un poco.</b></td><td>조금 걸어요.</td></tr></table>
<div class="note g"><b>a veces … a veces …</b> <b>A veces</b> voy de compras, <b>a veces</b> me encuentro con mis amigos. 가끔은 쇼핑하고, 가끔은 친구들을 만나요.
<br><b>나 → 우리 (nosotros)</b> hablo → habl<b>amos</b> · como → com<b>emos</b> · camino → camin<b>amos</b> · voy → <b>vamos</b></div>
""" + h("문법", "'나가요?' 아니면 '집에 있어요?'") + """
<div class="two"><div class="box y"><b>salir 나가다</b>
<p>¿<b>Sales</b> el sábado?<br>토요일에 나가요?<br>Sí, <b>salgo</b> con mis amigos.</p></div>
<div class="box y"><b>quedarse en casa 집에 있다</b>
<p>¿Prefieres <b>quedarte</b> en casa?<br>집에 있는 게 더 좋아요?<br>Sí, <b>me quedo</b> en casa.</p></div></div>
"""
 + h("연습 A", "누가 한 말일까요? Sofía 또는 Mateo를 쓰세요.")
 + blanks([f"Por la mañana leo el periódico. → {BS}", f"Paso tiempo con mi familia. → {BS}", f"A veces voy al mercado. → {BS}", f"Vamos a un restaurante o a un bar. → {BS}", f"Me gusta preparar la cena. → {BS}"])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Sales el sábado o prefieres quedarte en casa?"), ("Sofía", "¿Qué haces el domingo? ¿Con quién pasas tiempo?"))
 + "</section>")

# ---------- Lesson 3 ----------
P.append(lesson(3, rng(7, 9), "지난 주말과 이번 주말", "팟캐스트 7. 지난 주말 · 8. 이번 주말 계획",
    ["<b>fui, vi, hice, comí, dormí</b>로 지난 주말에 한 일을 말할 수 있다.", "<b>voy a + 동사원형</b>으로 이번 주말 계획을 말할 수 있다."])
 + h("대화 ①", "지난 주말 — ¿Qué hiciste?")
 + dlg("Bueno, Sofía, ¿qué hiciste", "El fin de semana pasado, el sábado", "El sábado pasado fui", "Y por la tarde dormí", "Mateo, ¡siempre", "El domingo pasado comí", "El domingo pasado vi")
 + h("문법", "과거형 (나: yo) — 이 다섯 개만 먼저!")
 + """<table class="t"><tr><th>지금</th><th>→ 지난 주말</th><th>예문</th></tr>
<tr><td>voy 가요</td><td><b>fui</b> 갔어요</td><td>Fui al centro. 시내에 갔어요.</td></tr>
<tr><td>veo 봐요</td><td><b>vi</b> 봤어요</td><td>Vi una película. 영화를 봤어요.</td></tr>
<tr><td>hago 해요</td><td><b>hice</b> 했어요</td><td>Hice deporte. 운동했어요.</td></tr>
<tr><td>como 먹어요</td><td><b>comí</b> 먹었어요</td><td>Comí con mi familia. 가족과 먹었어요.</td></tr>
<tr><td>duermo 자요</td><td><b>dormí</b> 잤어요</td><td>Dormí una siesta. 낮잠을 잤어요.</td></tr>
<tr><td>es …예요</td><td><b>fue</b> …였어요</td><td>Fue muy agradable. 아주 즐거웠어요.</td></tr></table>"""
 + h("대화 ②", "이번 주말 — ¿Qué vas a hacer?")
 + dlg("¿Y este fin de semana?", "Hm. Este fin de semana voy", "¡Qué bien! ¿Y qué vas", "Vamos a cenar juntos", "Suena muy bien. Yo este fin")
 + h("문법", "ir a + 동사원형 — '…할 거예요'")
 + """<table class="t"><tr><th>주어</th><th>ir</th><th>+ a + 동사원형</th></tr>
<tr><td>yo</td><td><b>voy</b></td><td>a descansar 쉴 거예요</td></tr>
<tr><td>tú</td><td><b>vas</b></td><td>a hacer … ¿Qué vas a hacer? 뭐 할 거예요?</td></tr>
<tr><td>nosotros</td><td><b>vamos</b></td><td>a cenar juntos 같이 저녁 먹을 거예요</td></tr></table>
<p class="sm">7주차의 <b>voy al trabajo</b>(일하러 가요)와 모양이 비슷하죠? <b>voy a + 동사원형</b>은 '가요'가 아니라 '…할 거예요'예요.</p>"""
 + h("연습 A", "지난 주말(과거) 또는 이번 주말(계획)으로 바꾸세요.")
 + blanks([f"Hago deporte. → El sábado pasado {B}.", f"Veo una película. → El domingo pasado {B}.", f"Voy al parque. → El sábado pasado {B}.", f"Descanso. → Este fin de semana {B}.", f"Leo un libro. → Este fin de semana {B}."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Mateo", "¿Qué hiciste el fin de semana pasado?"), ("Sofía", "¿Qué vas a hacer este fin de semana?"))
 + "</section>")

# ---------- Lesson 4 ----------
iQ = find("¿Podéis recordar")
iR = find("Ahora, el último reto")
P.append(lesson(4, rng(9, None), "약속 잡기와 나의 주말", "팟캐스트 9. 함께 약속 잡기 · 10. 여러분의 계획 · 11. 퀴즈와 정리 · 12. 마지막 도전",
    ["<b>¿Qué te parece si …? · ¿A qué hora? · ¿Te parece bien?</b>으로 친구와 약속을 잡을 수 있다.", "쉬운 문장 5~7개로 <b>나의 주말</b>을 이어서 말할 수 있다."])
 + h("대화", "팟캐스트에서 — 토요일 4시, 광장 카페!")
 + dlg("Sofía, ¿qué te parece si", "Sí, me gusta la idea", "Podemos ir al parque", "Mm. ¿El sábado por la mañana?", "Claro. Entonces", "El sábado por la tarde. Sí", "Perfecto. Vamos a un café. ¿A qué", "A las cuatro. ¿Te parece", "Sí, a las cuatro en el café", "Perfecto, ya tengo planes")
 + h("표현", "약속 잡기 순서")
 + """<table class="t"><tr><th>단계</th><th>스페인어</th><th>뜻</th></tr>
<tr><td>① 제안</td><td>¿<b>Qué te parece si</b> hacemos algo juntos?</td><td>우리 같이 뭐 하는 거 어때요?</td></tr>
<tr><td>② 수락</td><td>Sí, <b>me gusta la idea</b>.</td><td>좋은 생각이에요.</td></tr>
<tr><td>③ 장소</td><td><b>Podemos</b> ir al parque. / <b>Vamos a</b> un café.</td><td>공원에 갈 수 있어요. / 카페에 가요.</td></tr>
<tr><td>④ 거절 · 다른 제안</td><td>No, <b>prefiero</b> dormir. — <b>Entonces</b>, por la tarde.</td><td>자는 게 더 좋아요. — 그럼 오후로 해요.</td></tr>
<tr><td>⑤ 시간</td><td>¿<b>A qué hora</b>? — A las cuatro. ¿<b>Te parece bien</b>?</td><td>몇 시에요? — 4시. 괜찮아요?</td></tr>
<tr><td>⑥ 확인</td><td><b>Así que</b> el sábado a las cuatro en el café.</td><td>그러니까 토요일 4시에 카페에서.</td></tr></table>"""
 + h("퀴즈", f"¿Podéis recordar? — 기억나요? ({fmt(T[iQ])})")
 + blanks([f"¿Qué hace Sofía el sábado por la mañana? {B}", f"¿Qué hace Mateo el sábado? {B}", f"¿Qué hace Mateo el domingo? {B}", f"¿Dónde van a ir Sofía y Mateo? ¿A qué hora? {B}"])
 + h("짝 활동", "옆 사람과 약속을 잡아 보세요")
 + ask(("Tú", "¿Qué te parece si … el próximo fin de semana?"), ("Tú", "¿A qué hora? ¿Dónde?"))
 + h("최종 미션", f"Mi fin de semana — 나의 주말 ({fmt(T[iR])})")
 + """<table class="t mine"><tr><th>질문</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>토요일엔?</td><td><b>El sábado me levanto … y …</b></td><td></td></tr>
<tr><td>일요일엔?</td><td><b>El domingo …</b></td><td></td></tr>
<tr><td>누구와?</td><td><b>Paso tiempo con …</b></td><td></td></tr>
<tr><td>좋아하는 것</td><td><b>Me gusta … / No me gusta …</b></td><td></td></tr>
<tr><td>지난 주말</td><td><b>El fin de semana pasado fui / vi / hice …</b></td><td></td></tr>
<tr><td>다음 주말</td><td><b>El próximo fin de semana voy a …</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> El sábado me levanto tarde, a las nueve. Por la tarde me encuentro con mis amigos y vamos a un café. El domingo paso tiempo con mi familia. Me gusta caminar por el parque. No me gusta limpiar la casa. El fin de semana pasado vi una película. El próximo fin de semana voy a ir a la montaña.</div>
""" + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>el sábado / los sábados를 써서 주말을 말할 수 있다.</li><li>hago · salgo · veo · voy를 쓸 수 있다.</li><li>주말 활동 8개 이상을 말할 수 있다.</li><li>fui · vi · hice · comí로 지난 주말을 말할 수 있다.</li><li>voy a + 동사원형으로 계획을 말할 수 있다.</li><li>¿Qué te parece si…?로 약속을 잡을 수 있다.</li></ul>'
 + "</section>")

# ---------- Appendix ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: 1 temprano · 2 tarde · 3 (자유) &nbsp;|&nbsp; B: 1 correr (hacer deporte) · 2 montar · 3 dormir</p>
<p><b>Lesson 2</b> A: 1 Mateo · 2 Sofía · 3 Mateo · 4 Mateo · 5 Sofía</p>
<p><b>Lesson 3</b> A: 1 hice deporte · 2 vi una película · 3 fui al parque · 4 voy a descansar · 5 voy a leer un libro</p>
<p><b>Lesson 4</b> 퀴즈: 1 Se levanta tarde (duerme mucho). · 2 Hace deporte (va al parque, corre o monta en bicicleta). · 3 Se relaja y ve películas (lee el periódico, va al mercado). · 4 Van al café de la plaza, a las cuatro (el sábado por la tarde).</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">현재형 · 과거형(나) · 계획(voy a + 동사원형). 굵은 글씨는 모양이 특이한 형태예요.</p>
<table class="t"><tr><th>동사</th><th>yo 현재</th><th>tú 현재</th><th>nosotros 현재</th><th>yo 과거</th><th>계획</th></tr>
<tr><td>hacer 하다</td><td><b>hago</b></td><td>haces</td><td>hacemos</td><td><b>hice</b></td><td>voy a hacer</td></tr>
<tr><td>ir 가다</td><td><b>voy</b></td><td><b>vas</b></td><td><b>vamos</b></td><td><b>fui</b></td><td>voy a ir</td></tr>
<tr><td>ver 보다</td><td><b>veo</b></td><td>ves</td><td>vemos</td><td>vi</td><td>voy a ver</td></tr>
<tr><td>salir 나가다</td><td><b>salgo</b></td><td>sales</td><td>salimos</td><td>salí</td><td>voy a salir</td></tr>
<tr><td>comer 먹다</td><td>como</td><td>comes</td><td>comemos</td><td>comí</td><td>voy a comer</td></tr>
<tr><td>dormir 자다</td><td><b>duermo</b></td><td><b>duermes</b></td><td>dormimos</td><td>dormí</td><td>voy a dormir</td></tr>
<tr><td>quedarse 머물다</td><td>me quedo</td><td>te quedas</td><td>nos quedamos</td><td>me quedé</td><td>voy a quedarme</td></tr></table>
<p class="sm">과거형은 마지막 글자에 강세가 와요: comí, salí, dormí, me quedé. (fui, vi는 한 음절이라 표시 없음)</p>
</section>""")

voc = ['<section class="lesson vk"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'단어장\' 탭과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 주말 이야기 교재 Ep13</title><style>{CSS}.vk .t.v{{font-size:8.2pt;margin-bottom:7px}}.vk .t.v td,.vk .t.v th{{padding:2px 6px}}</style></head><body>{"".join(P)}</body></html>')
print("ok")
