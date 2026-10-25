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
END = 10 * 60 + 22

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
<div class="ct"><h1>왕초보 스페인어<br>요일과 나의 일주일</h1>
<div class="cs">Easy Spanish Podcast Ep.23 · A1 입문 · 5주차</div>
<div class="big">Hoy es lunes. ¡Por fin es viernes!</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · 요일 단어의 규칙 (el lunes / los lunes)</td></tr>
<tr><th>LESSON 1</th><td>오늘 · 내일은 무슨 요일? · ¿Qué día es hoy?</td></tr>
<tr><th>LESSON 2</th><td>요일마다 하는 일 · El lunes trabajo / El sábado descanso</td></tr>
<tr><th>LESSON 3</th><td>좋아하는 요일 · 어제 · 약속 잡기 (Ayer fue domingo · ¿Café el miércoles?)</td></tr>
<tr><th>LESSON 4</th><td>듣고 답하기 · 작은 도전 · 나의 일주일 발표</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 11월 15일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>""")

# ---------- intro ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 발음과 요일 단어의 규칙</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. 이번 에피소드는 10분으로 짧아요. 대신 <b>¿Qué haces el …?</b> 질문이 계속 나오니 매번 멈추고 내 대답을 말해 보세요!</div>
""" + h("발음", "요일 단어 소리 내어 읽기") + """
<table class="t"><tr><th>요일</th><th>소리</th><th>주의할 점</th></tr>
<tr><td><b>lunes</b></td><td>루네스</td><td>달(luna)의 날</td></tr>
<tr><td><b>martes</b></td><td>마르떼스</td><td>r은 혀를 한 번 튕겨요</td></tr>
<tr><td><b>miércoles</b></td><td>미<b>에</b>르꼴레스</td><td>강세 부호 é를 세게 · 가장 긴 요일</td></tr>
<tr><td><b>jueves</b></td><td>후<b>에</b>베스</td><td>j = 강한 ㅎ, v = ㅂ</td></tr>
<tr><td><b>viernes</b></td><td>비<b>에</b>르네스</td><td>v = ㅂ</td></tr>
<tr><td><b>sábado</b></td><td><b>사</b>바도</td><td>강세 부호 á를 세게 · d는 부드럽게</td></tr>
<tr><td><b>domingo</b></td><td>도<b>밍</b>고</td><td>go는 '고'</td></tr>
</table>
<p class="sm">※ 한글 표기는 감을 잡기 위한 참고용이에요. 마테오가 "Dominic"처럼 빨리 말하는 부분(4:29)도 들어 보세요.</p>
""" + h("문법 0", "요일 단어의 세 가지 규칙") + """
<div class="two"><div class="box y"><b>① 소문자로 써요</b>
<p>영어 Monday와 달리 <b>lunes</b>, <b>martes</b> … 모두 소문자예요. (문장 맨 앞만 대문자)</p>
<b>② 모두 남성 명사 → el</b>
<p><b>el</b> lunes · <b>el</b> sábado · <b>el</b> domingo</p></div>
<div class="box y"><b>③ el + 요일 = "~요일에"</b>
<p><b>El lunes</b> trabajo. 월요일에 일해요. (en을 쓰지 않아요!)<br>✗ <s>En lunes trabajo.</s><br><b>Los lunes</b> trabajo. 월요일마다 일해요.</p>
<p class="sm">lunes~viernes는 복수형도 같아요(el lunes / los lunes). sábado·domingo는 -s를 붙여요(los sábados).</p></div></div>
<div class="note y"><b>요일 이름의 뜻</b> lunes 달(Luna) · martes 화성(Marte) · miércoles 수성(Mercurio) · jueves 목성(Júpiter) · viernes 금성(Venus) — 한국어 월·화·수·목·금과 같은 행성 이름이에요! sábado는 안식일, domingo는 '주님의 날'이에요.</div>
<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 목요일엔 요리하고, 토요일엔 운동과 쇼핑. 가장 좋아하는 요일은 가족과 쉬는 <b>일요일</b>. · <b class="cM">Mateo</b> — 월요일이 싫고 커피가 필요해요. 수요일엔 운동, <b>금요일</b>엔 친구들을 만나요. · <b class="cT">Tú (나)</b> — 나의 일주일을 말할 청취자!</p>
</section>""")

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 3), "오늘 · 내일은 무슨 요일?", "팟캐스트 1. 오프닝 · 2. 월요일 · 화요일 · 수요일",
    ["<b>¿Qué día es hoy? — Hoy es lunes.</b>로 오늘 요일을 말할 수 있다.", "<b>¿Qué día es mañana? — Mañana es martes.</b>로 내일 요일을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Sofía, ¡por fin", "¿Viernes, Mateo?", "¿Lunes? Ay, no me gusta", "No. El lunes necesito", "¿Qué haces el lunes?", "El lunes trabajo mucho", "Ah, entiendo. ¿Y mañana?", "Mañana… mañana es martes", "Exacto. ¿Qué haces el martes", "El martes trabajo también", "El miércoles… el miércoles")
 + h("문법", "오늘 · 내일 · 어제")
 + """<table class="t"><tr><th></th><th>묻기</th><th>대답</th></tr>
<tr><td><b>hoy</b> 오늘</td><td>¿Qué día es <b>hoy</b>?</td><td><b>Hoy es</b> lunes.</td></tr>
<tr><td><b>mañana</b> 내일</td><td>¿Qué día es <b>mañana</b>?</td><td><b>Mañana es</b> martes.</td></tr>
<tr><td><b>ayer</b> 어제 (Lesson 3)</td><td>¿Qué día <b>fue</b> ayer?</td><td><b>Ayer fue</b> domingo.</td></tr></table>
<div class="note g"><b>요일을 말할 때는 el이 없어요</b> Hoy es lunes. (✗ Hoy es el lunes.) — '~요일<b>에</b> 무엇을 한다'고 할 때만 <b>el</b>: <b>El</b> lunes trabajo.
<br><b>mañana</b>는 '내일'과 '아침' 두 뜻이 있어요: mañana 내일 · por la mañana 아침에.</div>
<div class="note y"><b>마테오의 기분</b> ¡Por fin es viernes! 드디어 금요일이다! · No me gusta el lunes. 월요일이 싫어. · El lunes necesito mucho café. 월요일엔 커피가 많이 필요해. — 2주차의 <b>(no) me gusta</b>를 요일에도 써요.</div>"""
 + h("연습 A", "다음 요일을 쓰세요.")
 + blanks([f"Hoy es lunes. Mañana es {B}.", f"Hoy es jueves. Mañana es {B}.", f"Hoy es sábado. Mañana es {B}.", f"Hoy es domingo. Mañana es {B}.", f"Hoy es martes. Mañana es {B}."])
 + h("연습 B", "el이 필요하면 el, 필요 없으면 ✗를 쓰세요.")
 + blanks([f"Hoy es {BS} miércoles.", f"{BS} lunes trabajo mucho.", f"¿Qué haces {BS} viernes?", f"Mañana es {BS} sábado."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Qué día es hoy?"), ("Sofía", "¿Qué día es mañana?"), ("Mateo", "¿Te gusta el lunes?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(3, 5), "요일마다 하는 일", "팟캐스트 3. 목요일 · 금요일 · 4. 토요일 · 일요일 · 주말",
    ["<b>¿Qué haces el …?</b>에 <b>El … + 동사(yo)</b>로 대답할 수 있다.", "<b>después del …</b>로 요일 순서를 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Después del miércoles es", "¿Qué haces el jueves, Sofía?", "El jueves yo trabajo", "Después del jueves es viernes", "El viernes veo a mis amigos", "El domingo… el domingo estoy en casa", "El sábado yo hago deporte", "El domingo… el domingo estoy con")
 + h("문법", "요일 + 하는 일 (yo 형태)")
 + """<table class="t"><tr><th>동사원형</th><th>나는 (yo)</th><th>너는? (tú)</th><th>예문</th></tr>
<tr><td>trabajar 일하다</td><td><b>trabajo</b></td><td>trabajas</td><td>El lunes trabajo mucho.</td></tr>
<tr><td>estudiar 공부하다</td><td><b>estudio</b></td><td>estudias</td><td>El martes estudio.</td></tr>
<tr><td>hacer 하다</td><td><b>hago</b> deporte</td><td>haces</td><td>El miércoles hago deporte.</td></tr>
<tr><td>cocinar 요리하다</td><td><b>cocino</b></td><td>cocinas</td><td>El jueves cocino.</td></tr>
<tr><td>ver 보다, 만나다</td><td><b>veo</b> a mis amigos</td><td>ves</td><td>El viernes veo a mis amigos.</td></tr>
<tr><td>descansar 쉬다</td><td><b>descanso</b></td><td>descansas</td><td>El sábado descanso.</td></tr>
<tr><td>ir 가다</td><td><b>voy</b> de compras</td><td>vas</td><td>El sábado voy de compras.</td></tr>
<tr><td>estar 있다</td><td><b>estoy</b> en casa</td><td>estás</td><td>El domingo estoy en casa.</td></tr></table>
<div class="note g"><b>hacer → hago, ver → veo</b> yo 형태가 불규칙해요. <b>¿Qué haces?</b>(뭐 해?)에 <b>Hago …</b>로 대답해요.
<br><b>después de + el = después del</b>: Después <b>del</b> miércoles es jueves. (de + el은 항상 del로 합쳐요)
<br><b>ver a + 사람</b>: Veo <b>a</b> mis amigos. (4주차의 '사람 앞의 a')</div>"""
 + h("연습 A", "동사를 yo 형태로 바꾸세요.")
 + blanks([f"El lunes (trabajar) {BS}.", f"El miércoles (hacer) {BS} deporte.", f"El viernes (ver) {BS} a mis amigos.", f"El sábado (ir) {BS} de compras.", f"El domingo (estar) {BS} en casa."])
 + h("연습 B", "빈칸에 알맞은 요일을 쓰세요.")
 + blanks([f"Después del lunes es {B}.", f"Después del viernes es {B}.", f"El fin de semana es {B} y {B}."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Qué haces el viernes?"), ("Mateo", "¿Qué haces el sábado? ¿Y el domingo?"))
 + "</section>")

# ---------- Lesson 3 ----------
P.append(lesson(3, rng(5, 7), "좋아하는 요일 · 어제 · 약속 잡기", "팟캐스트 5. 일주일 정리 · 6. 어제 · 약속 잡기",
    ["<b>Mi día favorito es … porque …</b>로 좋아하는 요일과 이유를 말할 수 있다.", "<b>¿Café el miércoles? — Puedo / No puedo</b>로 약속을 잡을 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Exacto. ¿Cuál es tu día favorito", "El domingo.", "Porque estoy con mi familia", "Ah, sí. Mi día favorito", "Hoy es lunes. ¿Qué día fue", "Ayer fue domingo", "Vamos a hacer planes", "El martes trabajo, Sofía", "Miércoles… miércoles")
 + h("문법 ①", "가장 좋아하는 요일과 이유")
 + """<div class="two"><div class="box y"><b>묻기</b>
<p><b>¿Cuál es tu día favorito?</b><br>가장 좋아하는 요일이 뭐예요?<br><b>¿Por qué te gusta ese día?</b><br>그 요일이 왜 좋아요?</p></div>
<div class="box y"><b>대답하기</b>
<p><b>Mi día favorito es el domingo</b><br><b>porque</b> estoy con mi familia y descanso.<br>일요일이 제일 좋아요. 가족과 함께 쉬니까요.</p></div></div>
""" + h("문법 ②", "어제는 과거형 — 미리 보기") + """
<table class="t"><tr><th>현재 (지금 · 평소)</th><th>과거 (어제)</th></tr>
<tr><td>Hoy <b>es</b> lunes. 오늘은 월요일이에요.</td><td>Ayer <b>fue</b> domingo. 어제는 일요일이었어요.</td></tr>
<tr><td>¿Qué <b>haces</b>? 뭐 해?</td><td>¿Qué <b>hiciste</b> ayer? 어제 뭐 했어?</td></tr>
<tr><td><b>Descanso</b>. 쉬어요.</td><td>Ayer <b>descansé</b> mucho. 어제 많이 쉬었어요.</td></tr></table>
<p class="sm">과거형은 나중에 자세히 배워요. 지금은 <b>Ayer fue …</b>와 <b>Ayer descansé.</b> 두 문장만 통째로 외워요.</p>
""" + h("표현", "약속 잡기 (Vamos a hacer planes)") + """
<div class="note y"><b>¿Café el martes?</b> 화요일에 커피 어때? → <b>El martes trabajo. No puedo.</b> 화요일엔 일해. 안 돼. → <b>¿Y el miércoles?</b> 그럼 수요일은? → <b>Puedo.</b> 돼! → <b>Perfecto. El miércoles, café.</b> 좋아. 수요일에 커피.
<br>모임 약속도 이렇게: <b>¿Estudiamos español el domingo?</b> 일요일에 스페인어 공부할까요? — <b>¡Sí, puedo!</b></div>"""
 + h("연습 A", "이유를 붙여 문장을 완성하세요.")
 + blanks([f"Mi día favorito es el viernes porque {B}. (친구들을 만나서)", f"Mi día favorito es el domingo porque {B}. (집에서 쉬어서)", f"No me gusta el lunes porque {B}. (일을 많이 해서)"])
 + h("연습 B", "약속 대화를 완성하세요.")
 + blanks([f"A: ¿Café el jueves? — B: El jueves estudio. No {BS}.", f"A: ¿Y el sábado? — B: ¡Sí, {BS}!", f"A: Hoy es martes. ¿Qué día {BS} ayer? — B: Ayer fue lunes."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Mateo", "¿Cuál es tu día favorito? ¿Por qué?"), ("Mateo", "¿Qué día fue ayer?"), ("Sofía", "¿Café el sábado? ¿Sí o no?"))
 + "</section>")

# ---------- Lesson 4 ----------
iQ = find("Mateo hace deporte el miércoles")
iP = find("Es hora de practicar")
iR = find("Ahora, un pequeño reto")
iF = find("Muy bien. Ahora, el reto final")
P.append(lesson(4, rng(7, None), "듣고 답하기 · 나의 일주일", "팟캐스트 7. 여러분의 일주일 · 8. 듣고 답하기 · 9. 문장 완성 · 10. 작은 도전 · 11. 마지막 도전",
    ["소피아와 마테오가 요일마다 하는 일을 <b>él / ella</b> 형태로 말할 수 있다.", "<b>5–7문장</b>으로 나의 일주일을 말할 수 있다."])
 + h("정리", "소피아와 마테오의 일주일")
 + """<table class="t fill"><tr><th></th><th>lun.</th><th>mar.</th><th>miér.</th><th>jue.</th><th>vier.</th><th>sáb.</th><th>dom.</th></tr>
<tr><td><b class="cS">Sofía</b></td><td></td><td>estudia español</td><td>café con Mateo</td><td></td><td></td><td></td><td></td></tr>
<tr><td><b class="cM">Mateo</b></td><td>trabaja mucho</td><td></td><td></td><td></td><td></td><td></td><td>está en casa</td></tr></table>
<p class="sm">팟캐스트를 다시 들으며 빈칸을 채워 보세요. (정답은 부록)</p>"""
 + h("문법", "나 → 그/그녀로 바꾸기")
 + """<table class="t"><tr><th>본인이 말할 때 (yo)</th><th>남이 말할 때 (él / ella)</th></tr>
<tr><td>El miércoles <b>hago</b> deporte.</td><td>Mateo <b>hace</b> deporte el miércoles.</td></tr>
<tr><td>El domingo <b>veo</b> a <b>mi</b> familia.</td><td>Sofía <b>ve</b> a <b>su</b> familia el domingo.</td></tr>
<tr><td>El martes <b>estudio</b> español.</td><td>Sofía <b>estudia</b> español el martes.</td></tr>
<tr><td>El viernes <b>veo</b> a <b>mis</b> amigos.</td><td>Mateo <b>ve</b> a <b>sus</b> amigos el viernes.</td></tr>
<tr><td>El domingo <b>estoy</b> en casa.</td><td>Mateo <b>está</b> en casa el domingo.</td></tr></table>"""
 + h("퀴즈", f"듣고 답하기 ({fmt(T[iQ])}) · 작은 도전 ({fmt(T[iR])})")
 + blanks([f"¿Qué hace Mateo el miércoles? {B}", f"¿Qué día ve Sofía a su familia? {B}", f"¿Qué hace Sofía el martes? {B}", f"¿Qué día ve Mateo a sus amigos? {B}", f"¿Cuál es el día favorito de Sofía? {B}"])
 + h("최종 미션", f"Describe tu semana — 나의 일주일 ({fmt(T[iP])} · {fmt(T[iF])})")
 + """<table class="t mine"><tr><th>요일</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>lunes</td><td><b>El lunes trabajo / estudio …</b></td><td></td></tr>
<tr><td>martes</td><td><b>El martes …</b></td><td></td></tr>
<tr><td>miércoles</td><td><b>El miércoles hago deporte …</b></td><td></td></tr>
<tr><td>jueves</td><td><b>El jueves cocino …</b></td><td></td></tr>
<tr><td>viernes</td><td><b>El viernes veo a mis amigos …</b></td><td></td></tr>
<tr><td>fin de semana</td><td><b>El sábado … El domingo …</b></td><td></td></tr>
<tr><td>좋아하는 요일</td><td><b>Mi día favorito es el … porque …</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> El lunes trabajo mucho. El martes estudio español. El miércoles hago deporte. El viernes veo a mis amigos y ceno fuera. El sábado voy de compras. El domingo estudio español con mis amigos en Ilsan. Mi día favorito es el domingo porque estudio español. ¡Me encanta!</div>
""" + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>월요일부터 일요일까지 순서대로 말할 수 있다.</li><li>오늘·내일·어제가 무슨 요일인지 말할 수 있다.</li><li>el + 요일로 "~요일에"를 말할 수 있다. (en 없이!)</li><li>trabajo · estudio · hago · veo · voy · estoy로 요일마다 하는 일을 말할 수 있다.</li><li>가장 좋아하는 요일과 이유를 porque로 말할 수 있다.</li><li>¿Café el …?로 약속을 잡고 Puedo / No puedo로 대답할 수 있다.</li></ul>'
 + "</section>")

# ---------- Appendix ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: 1 martes · 2 viernes · 3 domingo · 4 lunes · 5 miércoles &nbsp;|&nbsp; B: 1 ✗ · 2 El · 3 el · 4 ✗</p>
<p><b>Lesson 2</b> A: 1 trabajo · 2 hago · 3 veo · 4 voy · 5 estoy &nbsp;|&nbsp; B: 1 martes · 2 sábado · 3 sábado y domingo</p>
<p><b>Lesson 3</b> A: 1 veo a mis amigos · 2 estoy en casa y descanso · 3 trabajo mucho &nbsp;|&nbsp; B: 1 puedo · 2 puedo · 3 fue</p>
<p><b>Lesson 4</b> 일주일 표 — Sofía: jueves trabaja y cocina · viernes ve a sus amigos y cena fuera · sábado hace deporte y va de compras · domingo está con su familia / Mateo: martes trabaja y estudia · miércoles hace deporte · jueves trabaja · viernes ve a sus amigos y descansa<br>
퀴즈: 1 Hace deporte. · 2 El domingo. · 3 Estudia español. · 4 El viernes. · 5 Es el domingo.</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">요일마다 하는 일을 말할 때 쓰는 동사예요. yo / tú / él·ella 세 줄을 외워요.</p>
<table class="t"><tr><th>주어</th><th>trabajar</th><th>hacer</th><th>ver</th><th>ir</th><th>estar</th><th>descansar</th><th>poder (할 수 있다)</th></tr>
<tr><td>yo</td><td>trabajo</td><td><b>hago</b></td><td><b>veo</b></td><td><b>voy</b></td><td><b>estoy</b></td><td>descanso</td><td><b>puedo</b></td></tr>
<tr><td>tú</td><td>trabajas</td><td>haces</td><td>ves</td><td>vas</td><td>estás</td><td>descansas</td><td>puedes</td></tr>
<tr><td>él / ella / usted</td><td>trabaja</td><td>hace</td><td>ve</td><td>va</td><td>está</td><td>descansa</td><td>puede</td></tr>
<tr><td>nosotros/as</td><td>trabajamos</td><td>hacemos</td><td>vemos</td><td>vamos</td><td>estamos</td><td>descansamos</td><td>podemos</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>trabajan</td><td>hacen</td><td>ven</td><td>van</td><td>están</td><td>descansan</td><td>pueden</td></tr></table>
<p class="sm">굵게 표시한 yo 형태는 불규칙이에요. 과거 미리 보기: ser → <b>fue</b> (Ayer fue domingo) · descansar → <b>descansé</b> · hacer → <b>hiciste</b></p>
</section>""")

voc = ['<section class="lesson"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'단어장\' 탭과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 요일 교재 Ep23</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
