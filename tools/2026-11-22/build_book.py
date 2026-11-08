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
END = 12 * 60 + 54

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
<div class="ct"><h1>왕초보 스페인어<br>열두 달과 나의 한 해</h1>
<div class="cs">Easy Spanish Podcast Ep.25 · A1 입문 · 6주차</div>
<div class="big">Mi cumpleaños es en mayo.</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · 달 이름의 규칙 (en mayo · 소문자)</td></tr>
<tr><th>LESSON 1</th><td>생일 묻고 답하기 · 1월~4월과 날씨</td></tr>
<tr><th>LESSON 2</th><td>5월~12월 · después de / antes de · 달마다 하는 일</td></tr>
<tr><th>LESSON 3</th><td>가장 좋아하는 달 · 여행 계획 (Quiero viajar en junio)</td></tr>
<tr><th>LESSON 4</th><td>짧은 문장 연습 · 기억력 퀴즈 · 나의 한 해 발표</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 11월 22일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
※ 이 영상은 공식 자막이 없어서 자동 자막을 듣고 다듬었어요. 각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>""")

# ---------- intro ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 발음과 달 이름의 규칙</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. 지난주 <b>요일</b>에 이어 이번 주는 <b>열두 달</b>이에요. 둘을 합치면 날짜를 말할 수 있어요!</div>
""" + h("발음", "열두 달 소리 내어 읽기") + """
<table class="t"><tr><th>달</th><th>소리</th><th>달</th><th>소리</th></tr>
<tr><td><b>enero</b></td><td>에<b>네</b>로</td><td><b>julio</b></td><td><b>훌</b>리오 (j = 강한 ㅎ)</td></tr>
<tr><td><b>febrero</b></td><td>페<b>브레</b>로</td><td><b>agosto</b></td><td>아<b>고</b>스또</td></tr>
<tr><td><b>marzo</b></td><td><b>마르</b>소 (z = th / ㅆ)</td><td><b>septiembre</b></td><td>셉띠<b>엠</b>브레</td></tr>
<tr><td><b>abril</b></td><td>아<b>브릴</b></td><td><b>octubre</b></td><td>옥<b>뚜</b>브레</td></tr>
<tr><td><b>mayo</b></td><td><b>마</b>요</td><td><b>noviembre</b></td><td>노비<b>엠</b>브레</td></tr>
<tr><td><b>junio</b></td><td><b>후</b>니오 (j = 강한 ㅎ)</td><td><b>diciembre</b></td><td>디씨<b>엠</b>브레</td></tr>
</table>
<p class="sm">junio(6월)와 julio(7월)가 헷갈려요: <b>ju-NI-o</b> / <b>ju-LI-o</b>. 9~12월은 모두 <b>-bre</b>로 끝나요.</p>
""" + h("문법 0", "달 이름의 세 가지 규칙") + """
<div class="two"><div class="box y"><b>① 소문자로 써요</b>
<p>요일처럼 <b>enero</b>, <b>mayo</b> … 모두 소문자예요. (문장 맨 앞만 대문자)</p>
<b>② "~월에" = en + 달</b>
<p><b>en</b> mayo 5월에 · <b>en</b> diciembre 12월에<br>Mi cumpleaños es <b>en</b> mayo.</p></div>
<div class="box y"><b>③ 요일은 el, 달은 en</b>
<p><b>El</b> lunes trabajo. 월요일에 일해요. (5주차)<br><b>En</b> agosto estoy de vacaciones. 8월엔 휴가예요.</p>
<p><b>+보너스 날짜</b>: el 5 de mayo 5월 5일 · el 25 de diciembre 12월 25일 (el + 숫자 + de + 달)</p></div></div>
<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 생일은 <b>5월</b>, 가장 좋아하는 달도 5월. 4월엔 가끔 여행, 12월엔 가족을 만나요. · <b class="cM">Mateo</b> — 생일은 <b>7월</b>(바닷가!), 가장 좋아하는 달은 휴가인 <b>8월</b>. <b>6월</b>에 여행 가고 싶어 해요. · <b class="cT">Tú (나)</b> — 나의 한 해를 말할 청취자!</p>
</section>""")

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 3), "생일과 1월~4월", "팟캐스트 1. 오프닝 · 2. 1월 · 2월 · 3월 · 4월",
    ["<b>¿Cuándo es tu cumpleaños? — Mi cumpleaños es en …</b>로 생일을 말할 수 있다.", "<b>En enero hace frío.</b>처럼 달과 날씨를 함께 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Muy bien, gracias. Oye", "Mi cumpleaños es en mayo", "¿Y tú, Mateo? ¿Cuándo", "Mi cumpleaños es en julio", "En enero hace frío", "Febrero. En febrero", "Después de febrero viene marzo", "Después de marzo viene abril", "En abril a veces viajo")
 + h("문법", "생일 · 날씨 말하기")
 + """<table class="t"><tr><th></th><th>묻기</th><th>대답</th></tr>
<tr><td>생일</td><td>¿<b>Cuándo</b> es tu cumpleaños?</td><td>Mi cumpleaños es <b>en</b> mayo.</td></tr>
<tr><td>날씨</td><td>¿Qué tiempo hace en enero? +보너스</td><td>En enero <b>hace frío</b>. · En junio <b>hace calor</b>.</td></tr>
<tr><td>비</td><td></td><td>En abril <b>llueve</b>. 4월엔 비가 와요.</td></tr></table>
<div class="note g"><b>hace + frío / calor</b> 날씨는 '하다' 동사 <b>hacer</b>의 3인칭 <b>hace</b>로 말해요: hace frío 추워요 · hace calor 더워요. 비는 동사 하나로: <b>llueve</b>.
<br><b>a veces</b> = 가끔: En febrero <b>a veces</b> hace más frío. · <b>más</b> = 더: hace <b>más</b> frío 더 추워요</div>
<div class="note y"><b>스페인의 날씨</b> 스페인은 한국과 같은 북반구라 계절이 비슷해요. 3월엔 봄(la primavera), 6월엔 여름(el verano)이 시작돼요. 남미(아르헨티나, 칠레)는 반대예요 — 12월이 여름!</div>"""
 + h("연습 A", "빈칸에 알맞은 달을 쓰세요.")
 + blanks([f"Después de enero viene {B}.", f"Después de {BS} viene abril.", f"En {BS} empieza la primavera.", f"Mi cumpleaños es en {B}. (내 생일)"])
 + h("연습 B", "날씨 표현을 완성하세요.")
 + blanks([f"🥶 En enero {B}.", f"☀️ En julio {B}.", f"🌧️ En abril {B}."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Mateo", "¿Cuándo es tu cumpleaños?"), ("Sofía", "¿Qué haces en abril? ¿Viajas?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(3, 5), "5월~12월과 달마다 하는 일", "팟캐스트 3. 5월~8월 · 4. 9월~12월",
    ["<b>después de / antes de</b>로 달의 순서를 말할 수 있다.", "<b>En agosto estoy de vacaciones.</b>처럼 달마다 하는 일을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Después de mayo viene junio", "Y después de junio viene julio", "Porque hace calor. Voy", "Después de julio viene agosto", "Sí, más. Porque en agosto", "Septiembre. En septiembre", "Sí, volvemos a trabajar", "Noviembre. A veces llueve", "Sí, en diciembre veo", "Antes de diciembre viene")
 + h("문법", "순서 말하기 — después de / antes de")
 + """<div class="two"><div class="box y"><b>다음 (después de)</b>
<p>¿Qué mes viene <b>después de</b> julio?<br>— <b>Después de</b> julio viene agosto.<br><b>viene</b> = 와요 (venir 오다)</p></div>
<div class="box y"><b>전 (antes de)</b>
<p>¿Qué mes viene <b>antes de</b> diciembre?<br>— <b>Antes de</b> diciembre viene noviembre.</p></div></div>
<p class="sm">요일과 달리 달 이름엔 el이 없어서 de가 del로 바뀌지 않아요: después <b>de</b> mayo (✗ del mayo) · 요일은 después <b>del</b> lunes</p>
""" + h("표현", "달마다 하는 일") + """
<table class="t"><tr><td>🏖️ En julio <b>voy a la playa</b>.</td><td>7월엔 바닷가에 가요.</td></tr>
<tr><td>🌴 En agosto <b>estoy de vacaciones</b>. No trabajo.</td><td>8월엔 휴가예요. 일을 안 해요.</td></tr>
<tr><td>💼 En septiembre <b>volvemos al trabajo</b>.</td><td>9월엔 다시 일을 시작해요.</td></tr>
<tr><td>🎒 <b>Los niños van a la escuela</b>.</td><td>아이들이 학교에 가요.</td></tr>
<tr><td>🎄 En diciembre <b>veo a mi familia</b>. Es un mes para la familia.</td><td>12월엔 가족을 만나요. 가족을 위한 달이에요.</td></tr></table>
<div class="note g"><b>스페인의 8월</b> 스페인에서는 8월에 많은 사람이 한 달 가까이 휴가를 가요. 그래서 마테오가 8월을 가장 좋아해요!</div>"""
 + h("연습 A", "빈칸을 채우세요.")
 + blanks([f"Después de junio viene {B}.", f"Antes de octubre viene {B}.", f"Después de {BS} viene enero.", f"El último mes del año es {B}."])
 + h("연습 B", "그림을 보고 문장을 완성하세요. (주어: 나)")
 + blanks([f"🏖️ julio → En julio {B}.", f"🌴 agosto → En agosto {B}.", f"🎄 diciembre → En diciembre {B}."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Qué haces en julio? ¿Y en agosto?"), ("Mateo", "¿Qué mes viene antes de diciembre?"))
 + "</section>")

# ---------- Lesson 3 ----------
P.append(lesson(3, rng(5, 7), "가장 좋아하는 달과 여행 계획", "팟캐스트 5. 가장 좋아하는 달 · 6. 여행 계획",
    ["<b>Mi mes favorito es … porque …</b>로 좋아하는 달과 이유를 말할 수 있다.", "<b>Quiero + 동사원형</b>으로 하고 싶은 일을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Muy bien. Sofía, ¿cuál es tu mes", "Mmm. Mi mes favorito", "¿Por qué te gusta mayo", "Porque es mi cumpleaños", "Sí. Agosto. Porque", "Sofía, quiero hacer", "Quiero viajar en junio", "Sí. En junio el tiempo", "Sí. Junio es un mes perfecto", "No, junio es mejor")
 + h("문법 ①", "가장 좋아하는 달과 이유")
 + """<div class="two"><div class="box y"><b>Sofía</b>
<p><b>Mi mes favorito es mayo</b><br><b>porque</b> es mi cumpleaños y el tiempo es muy bueno.</p></div>
<div class="box y"><b>Mateo</b>
<p><b>Mi mes favorito es agosto</b><br><b>porque</b> no trabajo. ¡Vacaciones!</p></div></div>
""" + h("문법 ②", "하고 싶어요 — quiero + 동사원형") + """
<table class="t"><tr><th>querer (원하다)</th><th>예문</th></tr>
<tr><td>yo <b>quiero</b></td><td><b>Quiero viajar</b> en junio. 6월에 여행 가고 싶어요.</td></tr>
<tr><td>tú <b>quieres</b></td><td>¿Cuándo <b>quieres viajar</b>? 언제 여행 가고 싶어요?</td></tr>
<tr><td>él / ella <b>quiere</b></td><td>Mateo <b>quiere viajar</b> en junio.</td></tr></table>
<div class="note g"><b>3주차의 querer!</b> Quiero <b>a</b> mi familia(가족을 사랑해요)와 같은 동사예요. 사람 앞에서는 '사랑하다', 동사원형 앞에서는 '~하고 싶다'.
<br><b>¿Qué prefieres?</b> 뭐가 더 좋아요? · ¿Verano <b>o</b> invierno? 여름이요, 겨울이요? · Junio es <b>mejor</b>. 6월이 더 좋아요.</div>"""
 + h("연습 A", "이유를 붙여 문장을 완성하세요.")
 + blanks([f"Mi mes favorito es diciembre porque {B}. (가족을 만나서)", f"Mi mes favorito es agosto porque {B}. (휴가라서)", f"Mi mes favorito es {BS} porque {B}. (나)"])
 + h("연습 B", "quiero / quieres / quiere 중 알맞은 것을 쓰세요.")
 + blanks([f"Yo {BS} viajar en octubre.", f"¿Cuándo {BS} viajar tú?", f"Mateo {BS} viajar en junio."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Mateo", "¿Cuál es tu mes favorito? ¿Por qué?"), ("Sofía", "¿Cuándo quieres viajar? ¿Verano o invierno?"))
 + "</section>")

# ---------- Lesson 4 ----------
iQ = find("Escucha bien. ¿En qué mes")
iR = find("Muy bien. Ahora, tu reto final")
iP = find("Ahora, un poco de práctica")
P.append(lesson(4, rng(7, None), "나의 한 해 말하기", "팟캐스트 7. 짧은 문장 · 8. 짧은 대화 · 9. 기억력 퀴즈 · 10. 복습과 마지막 도전",
    ["질문에 열두 달로 바로 대답할 수 있다.", "<b>5–7문장</b>으로 나의 한 해를 말할 수 있다."])
 + h("정리", "소피아와 마테오의 한 해")
 + """<table class="t fill"><tr><th></th><th>생일</th><th>가장 좋아하는 달 · 이유</th><th>그 밖에</th></tr>
<tr><td><b class="cS">Sofía</b></td><td></td><td></td><td>4월: viaja un poco · 12월: ve a su familia</td></tr>
<tr><td><b class="cM">Mateo</b></td><td></td><td></td><td>quiere viajar en …</td></tr></table>"""
 + h("퀴즈", f"¿Lo recuerdas? — 기억력 퀴즈 ({fmt(T[iQ])})")
 + blanks([f"¿En qué mes es el cumpleaños de Sofía? {B}", f"¿Cuál es el mes favorito de Mateo? ¿Por qué? {B}", f"¿En qué mes quiere viajar Mateo? {B}", f"¿Qué tiempo hace en enero? {B}"])
 + h("문법", "나 → 그/그녀로 바꾸기")
 + """<table class="t"><tr><th>본인이 말할 때 (yo)</th><th>남이 말할 때 (él / ella)</th></tr>
<tr><td><b>Mi</b> cumpleaños es en mayo.</td><td>El cumpleaños <b>de Sofía</b> es en mayo. · <b>Su</b> cumpleaños …</td></tr>
<tr><td><b>Mi</b> mes favorito es agosto.</td><td>El mes favorito <b>de Mateo</b> es agosto.</td></tr>
<tr><td><b>No trabajo.</b></td><td><b>No trabaja.</b></td></tr>
<tr><td><b>Quiero</b> viajar en junio.</td><td>Mateo <b>quiere</b> viajar en junio.</td></tr></table>"""
 + h("최종 미션", f"Tu reto final — 나의 한 해 ({fmt(T[iP])} · {fmt(T[iR])})")
 + """<table class="t mine"><tr><th>항목</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 생일</td><td><b>Mi cumpleaños es en …</b></td><td></td></tr>
<tr><td>② 좋아하는 달</td><td><b>Mi mes favorito es … porque …</b></td><td></td></tr>
<tr><td>③ 날씨</td><td><b>En enero hace frío. / En julio hace calor.</b></td><td></td></tr>
<tr><td>④ 달마다 하는 일</td><td><b>En junio hago … / En diciembre estoy con …</b></td><td></td></tr>
<tr><td>⑤ 좋아요 · 싫어요</td><td><b>Me gusta abril. No me gusta noviembre.</b></td><td></td></tr>
<tr><td>⑥ 하고 싶은 일</td><td><b>Quiero viajar en …</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> Mi cumpleaños es en octubre. Mi mes favorito es octubre porque el tiempo es muy bueno. En enero hace mucho frío en Corea. En agosto hace calor y voy a la playa. En diciembre estoy con mi familia. No me gusta febrero. Quiero viajar a España en mayo.</div>
<p class="sm">viajar <b>a</b> + 나라 = …로 여행 가다 (Quiero viajar <b>a</b> España) · 한국의 명절: <b>el Año Nuevo Lunar</b> 설날 · <b>Chuseok</b> 추석 (septiembre u octubre)</p>
""" + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>1월부터 12월까지 순서대로 말할 수 있다. (junio / julio 구분!)</li><li>en + 달로 "~월에"를 말할 수 있다. (요일은 el, 달은 en)</li><li>생일을 묻고 대답할 수 있다.</li><li>hace frío / hace calor / llueve로 달마다 날씨를 말할 수 있다.</li><li>después de / antes de로 달의 순서를 말할 수 있다.</li><li>가장 좋아하는 달과 이유, 하고 싶은 일(quiero + 동사원형)을 말할 수 있다.</li></ul>'
 + "</section>")

# ---------- Appendix ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: 1 febrero · 2 marzo · 3 marzo · 4 (나의 생일 달) &nbsp;|&nbsp; B: 1 hace frío · 2 hace calor · 3 llueve</p>
<p><b>Lesson 2</b> A: 1 julio · 2 septiembre · 3 diciembre · 4 diciembre &nbsp;|&nbsp; B: 1 voy a la playa · 2 estoy de vacaciones · 3 veo a mi familia</p>
<p><b>Lesson 3</b> A: 1 veo a mi familia · 2 estoy de vacaciones (no trabajo) · 3 (나) &nbsp;|&nbsp; B: 1 quiero · 2 quieres · 3 quiere</p>
<p><b>Lesson 4</b> 표 — Sofía: mayo · mayo, porque es su cumpleaños y el tiempo es muy bueno / Mateo: julio · agosto, porque no trabaja (vacaciones) · junio<br>
퀴즈: 1 En mayo. · 2 Agosto, porque no trabaja. · 3 En junio. · 4 Hace frío.</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">이번 에피소드의 핵심 동사예요. 날씨는 <b>hace</b> · <b>llueve</b> 그대로 외워요.</p>
<table class="t"><tr><th>주어</th><th>ser</th><th>venir (오다)</th><th>hacer</th><th>querer</th><th>viajar</th><th>ir</th><th>estar</th></tr>
<tr><td>yo</td><td>soy</td><td>vengo</td><td>hago</td><td><b>quiero</b></td><td>viajo</td><td>voy</td><td>estoy</td></tr>
<tr><td>tú</td><td>eres</td><td>vienes</td><td>haces</td><td><b>quieres</b></td><td>viajas</td><td>vas</td><td>estás</td></tr>
<tr><td>él / ella / usted</td><td>es</td><td><b>viene</b></td><td><b>hace</b> (frío)</td><td><b>quiere</b></td><td>viaja</td><td>va</td><td>está</td></tr>
<tr><td>nosotros/as</td><td>somos</td><td>venimos</td><td>hacemos</td><td>queremos</td><td>viajamos</td><td>vamos</td><td>estamos</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>son</td><td>vienen</td><td>hacen</td><td>quieren</td><td>viajan</td><td>van</td><td>están</td></tr></table>
<p class="sm">volver (돌아가다) → <b>volvemos</b> al trabajo · llover (비가 오다) → <b>llueve</b></p>
</section>""")

voc = ['<section class="lesson"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'단어장\' 탭과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 열두 달 교재 Ep25</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
