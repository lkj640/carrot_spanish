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
END = 17 * 60 + 22

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
<div class="ct"><h1>왕초보 스페인어<br>나의 하루 일과</h1>
<div class="cs">Easy Spanish Podcast Ep.5 · A1 입문 · 7주차</div>
<div class="big">Me levanto a las siete.</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · 재귀동사 (me levanto) · 시간 말하기 (a las ocho)</td></tr>
<tr><th>LESSON 1</th><td>아침 일과 · Me despierto, me levanto, me ducho, me visto, desayuno</td></tr>
<tr><th>LESSON 2</th><td>낮 · 저녁 · 밤 · Voy al trabajo, como, vuelvo a casa, ceno, me acuesto</td></tr>
<tr><th>LESSON 3</th><td>듣기: 카를로스와 아나의 하루 (se levanta · come · vuelve)</td></tr>
<tr><th>LESSON 4</th><td>네 차례 · 다 이어서 말하기 · 나의 하루 발표</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 11월 29일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기 · 17분이라 1–8번 / 9–12번 구간으로 나눠 들어도 좋아요</div></div>
<div class="stripe"></div></section>""")

# ---------- intro ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 재귀동사와 시간 말하기</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. 5주차 <b>요일</b>, 6주차 <b>열두 달</b>에 이어 이번 주는 <b>하루의 시간</b>이에요!</div>
""" + h("발음", "이번 에피소드에 나오는 주의할 소리") + """
<table class="t"><tr><th>글자</th><th>소리</th><th>예</th></tr>
<tr><td><b>v</b> = <b>b</b></td><td>둘 다 'ㅂ'에 가까워요</td><td>me <b>v</b>isto 메 비스또 · <b>v</b>uelvo 부엘보 · <b>b</b>ien</td></tr>
<tr><td><b>ll</b></td><td>'y'처럼</td><td><b>ll</b>amo 야모</td></tr>
<tr><td><b>c + e, i</b> / <b>z</b></td><td>스페인: th / 중남미: ㅆ</td><td><b>ce</b>no 쎄노 · ha<b>ce</b>r · al<b>m</b>uer<b>z</b>o</td></tr>
<tr><td><b>ue</b></td><td>'우에'를 빠르게 → '웨'</td><td>d<b>ue</b>rmo 두에르모 · v<b>ue</b>lvo · ac<b>ue</b>sto 아꾸에스또</td></tr>
<tr><td><b>강세</b></td><td>표시된 곳을 세게</td><td>m<b>ú</b>sica · televisi<b>ó</b>n · r<b>u</b>tina</td></tr>
</table>
<p class="sm">※ ceno(저녁을 먹어요)는 자막에 'Sino', 'Seno'로 잘못 나오기도 해요. 소리는 '쎄노'예요.</p>
""" + h("문법 0-①", "재귀동사 — 나 자신에게 하는 동작 (me levanto)") + """
<table class="t"><tr><th>주어</th><th>levantarse 일어나다</th><th>ducharse 샤워하다</th><th>acostarse 자러 가다</th></tr>
<tr><td>yo</td><td><b>me</b> levanto</td><td><b>me</b> ducho</td><td><b>me</b> acuesto</td></tr>
<tr><td>tú</td><td><b>te</b> levantas</td><td><b>te</b> duchas</td><td><b>te</b> acuestas</td></tr>
<tr><td>él / ella</td><td><b>se</b> levanta</td><td><b>se</b> ducha</td><td><b>se</b> acuesta</td></tr></table>
<p class="sm">사전에는 -se가 붙어 있어요(levantar<b>se</b>). 말할 때는 me/te/se를 동사 앞에! 1주차의 <b>me llamo / te llamas / se llama</b>도 같은 원리예요.</p>
""" + h("문법 0-②", "시간 말하기 — a las + 숫자") + """
<div class="two"><div class="box y"><b>몇 시에?</b>
<p>¿<b>A qué hora</b> te levantas?<br>— <b>A las</b> siete. 7시에.<br>— <b>A la</b> una. 1시에. (1시만 la!)<br>— <b>A las</b> ocho <b>y media</b>. 8시 반에.</p></div>
<div class="box y"><b>하루의 때</b>
<p><b>por la mañana</b> 아침에<br><b>por la tarde</b> 오후에<br><b>por la noche</b> 밤에<br><b>y cuarto</b> 15분 · <b>menos cuarto</b> 15분 전 (+보너스)</p></div></div>
<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 7시 기상, 9시 출근, 2시 점심, 6시 귀가, 8시 저녁, 11시 취침 · 8시간 자요. · <b class="cM">Mateo</b> — 8시 기상, 커피와 빵, 1시 반 점심, 5시 귀가, 10시 취침 · 9시간 자요. · <b class="cT">Tú (나)</b> — 나의 하루를 말할 청취자!</p>
</section>""")

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 5), "아침 일과", "팟캐스트 1. 오프닝 · 2. 일어나기 · 3. 씻고 입고 먹기 · 4. 아침 식사",
    ["<b>me despierto, me levanto, me ducho, me lavo los dientes, me visto, desayuno</b>로 아침 일과를 말할 수 있다.", "<b>¿A qué hora te levantas? — Me levanto a las …</b>로 시간을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Empezamos con la mañana", "Excelente. «Me despierto»", "«Me levanto» es salir", "Y tú, Mateo, ¿a qué hora te levantas", "Yo me levanto a las ocho", "Después de levantarme", "Muy bien. Después me lavo", "Entonces, mi rutina de la mañana", "Yo desayuno café", "Yo desayuno a las ocho y media")
 + h("문법", "아침 일과 순서대로")
 + """<table class="t"><tr><th>순서</th><th>스페인어</th><th>뜻</th></tr>
<tr><td>①</td><td>Me <b>despierto</b>.</td><td>잠에서 깨요. (abrir los ojos 눈을 뜨다)</td></tr>
<tr><td>②</td><td>Me <b>levanto</b>.</td><td>일어나요. (salir de la cama 침대에서 나오다)</td></tr>
<tr><td>③</td><td>Me <b>ducho</b>.</td><td>샤워해요.</td></tr>
<tr><td>④</td><td>Me <b>lavo</b> los dientes.</td><td>이를 닦아요.</td></tr>
<tr><td>⑤</td><td>Me <b>visto</b>.</td><td>옷을 입어요.</td></tr>
<tr><td>⑥</td><td><b>Desayuno</b>. (me 없음!)</td><td>아침을 먹어요.</td></tr></table>
<div class="note g"><b>순서를 잇는 말</b> <b>Primero</b> me levanto, <b>después</b> me ducho, <b>luego</b> me visto y <b>finalmente</b> desayuno. 먼저 일어나고, 그다음 샤워하고, 그리고 옷을 입고, 마지막으로 아침을 먹어요.
<br><b>Después de + 동사원형</b>: Después de <b>levantarme</b>, me ducho. 일어난 다음에 샤워해요.</div>"""
 + h("연습 A", "그림을 보고 알맞은 동사를 쓰세요. (주어: 나)")
 + blanks([f"⏰ {B}.", f"🚿 {B}.", f"🪥 {B}.", f"👕 {B}.", f"🥐☕ {B}."])
 + h("연습 B", "me / te / se 중 알맞은 것을 쓰세요.")
 + blanks([f"Yo {BS} levanto a las siete.", f"¿A qué hora {BS} levantas tú?", f"Carlos {BS} ducha y {BS} viste."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿A qué hora te levantas?"), ("Sofía", "¿Qué haces por la mañana? ¿Qué desayunas?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(5, 9), "낮 · 저녁 · 밤", "팟캐스트 5. 일하러 가요 · 6. 오후 · 7. 저녁 · 밤 · 8. 잠자리에 들기",
    ["<b>Voy al trabajo, como, vuelvo a casa, ceno</b>로 낮과 저녁 일과를 말할 수 있다.", "<b>Me acuesto a las … Duermo … horas.</b>로 잠자는 시간을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Sí, sí. Yo voy al trabajo", "Yo trabajo a las nueve", "Puedes decir «como»", "Yo como a la una y media", "Y por la tarde vuelvo", "Yo vuelvo a casa a las cinco", "Después de cenar, a veces", "Yo me acuesto a las once", "Yo me acuesto a las diez", "Yo duermo nueve horas")
 + h("문법", "모음이 바뀌는 동사 (o → ue)")
 + """<table class="t"><tr><th>동사원형</th><th>나 (yo)</th><th>너 (tú)</th><th>그/그녀 (él/ella)</th><th>예문</th></tr>
<tr><td>volver 돌아오다</td><td><b>vuelvo</b></td><td>vuelves</td><td>vuelve</td><td>Vuelvo a casa a las seis.</td></tr>
<tr><td>dormir 자다</td><td><b>duermo</b></td><td>duermes</td><td>duerme</td><td>Duermo ocho horas.</td></tr>
<tr><td>acostarse 자러 가다</td><td><b>me acuesto</b></td><td>te acuestas</td><td>se acuesta</td><td>Me acuesto a las once.</td></tr>
</table>
<div class="note g"><b>점심은 como 또는 almuerzo</b> 스페인에서는 점심을 보통 <b>comer</b>(como)라고 해요. 점심이 하루의 큰 식사라 2시쯤 먹어요. 저녁은 <b>cenar</b>(ceno), 보통 8~9시로 늦어요!
<br><b>ir al trabajo</b> 일하러 가다 → Voy <b>al</b> trabajo (a + el = al)</div>
""" + h("표현", "저녁에 하는 일") + """
<table class="t"><tr><td>📺 <b>Veo la televisión.</b></td><td>텔레비전을 봐요.</td><td>📖 <b>Leo un libro.</b></td><td>책을 읽어요.</td></tr>
<tr><td>🎧 <b>Escucho música.</b></td><td>음악을 들어요.</td><td>🛋️ <b>Descanso.</b></td><td>쉬어요.</td></tr></table>
"""
 + h("연습 A", "동사를 yo 형태로 바꾸세요.")
 + blanks([f"(volver) {BS} a casa a las seis.", f"(dormir) {BS} siete horas.", f"(acostarse) {BS} a las doce.", f"(ir) {BS} al trabajo a las nueve.", f"(cenar) {BS} a las ocho."])
 + h("연습 B", "시간을 스페인어로 쓰세요.")
 + blanks([f"🕐 1:00 → a {B}", f"🕗 8:30 → a {B}", f"🕚 11:00 → a {B}"])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿A qué hora comes? ¿Cuándo vuelves a casa?"), ("Sofía", "¿Qué haces por la noche? ¿A qué hora te acuestas?"))
 + "</section>")

# ---------- Lesson 3 ----------
iC = find("Carlos se levanta a las siete")
iA = find("Ana se levanta a las seis")
P.append(lesson(3, rng(9, 11), "듣기: 카를로스와 아나의 하루", "팟캐스트 9. 카를로스의 하루 · 10. 아나의 하루",
    ["다른 사람의 하루 일과를 듣고 시간과 활동을 파악할 수 있다.", "<b>se levanta, come, vuelve, se acuesta</b>처럼 3인칭으로 말할 수 있다."])
 + h("듣기 ①", f"La rutina de Carlos — 카를로스의 하루 ({fmt(T[iC])})")
 + '<div class="story">Carlos se levanta a las siete. Se ducha y se viste. Desayuna a las ocho. Va al trabajo. Come a la una. Vuelve a casa a las seis. Cena a las siete y media. Ve la televisión. Se acuesta a las diez y duerme ocho horas.</div>'
 + h("이해 확인", "카를로스의 시간표를 채우세요.")
 + '<table class="t fill"><tr><th>일어나요</th><th>아침</th><th>점심</th><th>집에 와요</th><th>저녁</th><th>자러 가요</th><th>몇 시간?</th></tr><tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr></table>'
 + h("듣기 ②", f"Un pequeño reto — 아나의 하루 ({fmt(T[iA])})")
 + '<div class="story">Ana se levanta a las seis. Se ducha. Desayuna café y fruta a las siete. Estudia español por la mañana. Come a la una. Por la tarde lee un libro. Cena a las ocho. Se acuesta a las once.</div>'
 + h("이해 확인", "질문에 스페인어로 답하세요.")
 + blanks([f"¿A qué hora se levanta Ana? {B}", f"¿Qué desayuna? {B}", f"¿Qué hace por la mañana? {B}", f"¿Qué hace por la tarde? {B}", f"¿A qué hora se acuesta? {B}"])
 + h("문법", "나 → 그/그녀로 바꾸기")
 + """<table class="t"><tr><th>본인이 말할 때 (yo)</th><th>남이 말할 때 (él / ella)</th></tr>
<tr><td><b>Me levanto</b> a las siete.</td><td><b>Se levanta</b> a las siete.</td></tr>
<tr><td><b>Me ducho</b> y <b>me visto</b>.</td><td><b>Se ducha</b> y <b>se viste</b>.</td></tr>
<tr><td><b>Voy</b> al trabajo. · <b>Como</b> a la una.</td><td><b>Va</b> al trabajo. · <b>Come</b> a la una.</td></tr>
<tr><td><b>Vuelvo</b> a casa. · <b>Veo</b> la televisión.</td><td><b>Vuelve</b> a casa. · <b>Ve</b> la televisión.</td></tr>
<tr><td><b>Me acuesto</b> y <b>duermo</b> ocho horas.</td><td><b>Se acuesta</b> y <b>duerme</b> ocho horas.</td></tr></table>"""
 + "</section>")

# ---------- Lesson 4 ----------
iT = find("Ahora te toca a ti, Mateo")
iJ = find("Sí. Dime tu rutina paso a paso")
iS = find("Hola, me llamo Sofía. Me levanto")
P.append(lesson(4, rng(11, None), "나의 하루 말하기", "팟캐스트 11. 네 차례 · 12. 다 이어서 말하기 · 소피아의 하루",
    ["하루 일과에 대한 질문 8개에 시간을 넣어 대답할 수 있다.", "<b>아침부터 밤까지</b> 나의 하루를 이어서 말할 수 있다."])
 + h("예시", f"소피아의 하루 ({fmt(T[iS])})")
 + '<div class="story">Hola, me llamo Sofía. Me levanto a las siete. Me ducho, me lavo los dientes, me visto. Desayuno a las ocho, voy al trabajo a las nueve, como a las dos. Vuelvo a casa a las seis, ceno a las ocho. Veo la televisión, leo un libro, escucho música. Me acuesto a las once. Duermo ocho horas.</div>'
 + h("최종 시험", f"Te toca a ti — 질문에 대답하세요! ({fmt(T[iT])})")
 + '<p class="sm">플레이어에서 해당 문장부터 재생하고, 마테오가 대답하기 전에 먼저 내 시간으로 말해 보세요.</p>'
 + ask(("Sofía", "¿A qué hora te levantas?"), ("Sofía", "¿Qué haces por la mañana?"), ("Sofía", "¿Qué desayunas?"), ("Sofía", "¿Trabajas o estudias? ¿A qué hora?"), ("Sofía", "¿A qué hora comes?"), ("Sofía", "¿Cuándo vuelves a casa?"), ("Sofía", "¿Qué haces por la noche?"), ("Sofía", "¿A qué hora te acuestas?"))
 + h("최종 미션", f"Mi rutina diaria — 나의 하루 ({fmt(T[iJ])})")
 + """<table class="t mine"><tr><th>때</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>아침 ①</td><td><b>Me levanto a las …</b></td><td></td></tr>
<tr><td>아침 ②</td><td><b>Me ducho, me visto y desayuno …</b></td><td></td></tr>
<tr><td>오전</td><td><b>Voy al trabajo / Estudio … a las …</b></td><td></td></tr>
<tr><td>오후</td><td><b>Como a la(s) … Vuelvo a casa a las …</b></td><td></td></tr>
<tr><td>저녁</td><td><b>Ceno a las … Después de cenar, …</b></td><td></td></tr>
<tr><td>밤</td><td><b>Me acuesto a las … Duermo … horas.</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> Me levanto a las seis y media. Me ducho, me visto y desayuno café y pan. Voy al trabajo a las ocho. Como a las doce. Vuelvo a casa a las siete. Ceno a las siete y media. Después de cenar, veo la televisión o leo un libro. Me acuesto a las once y duermo siete horas.</div>
<p class="sm">한국은 점심이 12시, 저녁이 7시쯤이죠. 스페인과 비교해서 말해 보세요: En Corea comemos a las doce. 한국에서는 12시에 점심을 먹어요.</p>
""" + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>아침 일과 6개를 순서대로 말할 수 있다.</li><li>me / te / se를 써서 재귀동사를 말할 수 있다.</li><li>a la una / a las ocho y media처럼 시간을 말할 수 있다.</li><li>vuelvo · duermo · me acuesto (o → ue) 동사를 쓸 수 있다.</li><li>다른 사람의 하루를 se levanta, come, vuelve로 말할 수 있다.</li><li>아침부터 밤까지 나의 하루를 이어서 말할 수 있다.</li></ul>'
 + "</section>")

# ---------- Appendix ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: 1 Me levanto (Me despierto) · 2 Me ducho · 3 Me lavo los dientes · 4 Me visto · 5 Desayuno &nbsp;|&nbsp; B: 1 me · 2 te · 3 se / se</p>
<p><b>Lesson 2</b> A: 1 Vuelvo · 2 Duermo · 3 Me acuesto · 4 Voy · 5 Ceno &nbsp;|&nbsp; B: 1 la una · 2 las ocho y media · 3 las once</p>
<p><b>Lesson 3</b> 카를로스: 7시 · 8시 · 1시 · 6시 · 7시 반 · 10시 · 8시간<br>
아나: 1 Se levanta a las seis. · 2 Desayuna café y fruta. · 3 Estudia español. · 4 Lee un libro. · 5 Se acuesta a las once.</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">재귀동사는 me / te / se, 굵은 글씨는 모음이 바뀌는 동사(o → ue, e → i)예요.</p>
<table class="t"><tr><th>주어</th><th>levantarse</th><th>vestirse</th><th>acostarse</th><th>volver</th><th>dormir</th><th>ir</th><th>ver</th></tr>
<tr><td>yo</td><td>me levanto</td><td>me <b>visto</b></td><td>me <b>acuesto</b></td><td><b>vuelvo</b></td><td><b>duermo</b></td><td>voy</td><td>veo</td></tr>
<tr><td>tú</td><td>te levantas</td><td>te <b>vistes</b></td><td>te <b>acuestas</b></td><td><b>vuelves</b></td><td><b>duermes</b></td><td>vas</td><td>ves</td></tr>
<tr><td>él / ella / usted</td><td>se levanta</td><td>se <b>viste</b></td><td>se <b>acuesta</b></td><td><b>vuelve</b></td><td><b>duerme</b></td><td>va</td><td>ve</td></tr>
<tr><td>nosotros/as</td><td>nos levantamos</td><td>nos vestimos</td><td>nos acostamos</td><td>volvemos</td><td>dormimos</td><td>vamos</td><td>vemos</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>se levantan</td><td>se <b>visten</b></td><td>se <b>acuestan</b></td><td><b>vuelven</b></td><td><b>duermen</b></td><td>van</td><td>ven</td></tr></table>
<p class="sm">ducharse · lavarse · despertarse(<b>me despierto</b>, e → ie)도 같은 방식이에요. nosotros 줄에서는 모음이 바뀌지 않아요.</p>
</section>""")

voc = ['<section class="lesson"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'단어장\' 탭과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 하루 일과 교재 Ep5</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
