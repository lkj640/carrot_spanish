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
END = 18 * 60 + 18

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
<div class="ct"><h1>왕초보 스페인어<br>가족 소개하기</h1>
<div class="cs">Easy Spanish Podcast Ep.4 · A1 입문 · 3주차</div>
<div class="big">Mi familia es pequeña.</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · 남성/여성 · 단수/복수 · mi / tu / su</td></tr>
<tr><th>LESSON 1</th><td>가족의 크기와 부모님 이름 · Mi padre se llama …</td></tr>
<tr><th>LESSON 2</th><td>형제자매와 가족 수 · Tengo un hermano / Somos cuatro</td></tr>
<tr><th>LESSON 3</th><td>자녀 · 조부모 · 함께 살아요 · 사랑해요 (vivir con / querer a)</td></tr>
<tr><th>LESSON 4</th><td>듣기: 라우라와 하비에르의 가족</td></tr>
<tr><th>LESSON 5</th><td>질문에 답하기 · 나의 가족 소개 · 마지막 도전</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 11월 1일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>""")

# ---------- intro ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 발음과 가족 단어의 규칙</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. 이번 에피소드는 소피아가 말하면 마테오가 <b>따라 말하는</b> 부분이 많아요. 마테오와 같이 소리 내어 따라 하세요!</div>
""" + h("발음", "이번 에피소드에 나오는 주의할 소리") + """
<table class="t"><tr><th>글자</th><th>소리</th><th>예</th></tr>
<tr><td><b>h</b></td><td>소리 없음</td><td><b>hermano</b> 에르마노 · <b>hijo</b> 이호 · <b>hay</b> 아이</td></tr>
<tr><td><b>j</b></td><td>목에서 나는 강한 ㅎ</td><td><b>hijo</b> 이호 · <b>juntos</b> 훈또스 · <b>Javier</b> 하비에르</td></tr>
<tr><td><b>ll</b></td><td>'y'처럼 — 야/요</td><td><b>se llama</b> 세 야마 · <b>se llaman</b> 세 야만</td></tr>
<tr><td><b>ñ</b></td><td>냐·녜·뇨</td><td><b>pequeña</b> 뻬께냐 · <b>niño</b> 니뇨 · <b>niña</b> 니냐</td></tr>
<tr><td><b>qu</b></td><td>ㄲ (u는 읽지 않음)</td><td><b>pequeña</b> 뻬께냐 · <b>quiero</b> 끼에로</td></tr>
<tr><td><b>c + e, i</b></td><td>스페인: 영어 th / 중남미: ㅆ</td><td><b>cinco</b> 씽꼬 · <b>coincidencia</b> 꼬인씨덴씨아</td></tr>
<tr><td><b>강세</b></td><td>끝에서 두 번째 음절이 기본</td><td>fa<b>mi</b>lia · her<b>ma</b>no · a<b>bue</b>lo · pe<b>que</b>ña</td></tr>
</table>
<p class="sm">※ 한글 표기는 감을 잡기 위한 참고용이에요. 정확한 소리는 꼭 팟캐스트로 들어 보세요.</p>
""" + h("문법 0", "가족 단어의 세 가지 규칙") + """
<div class="two"><div class="box y"><b>① -o는 남자, -a는 여자</b>
<p><b>el</b> herman<b>o</b> / <b>la</b> herman<b>a</b><br><b>el</b> abuel<b>o</b> / <b>la</b> abuel<b>a</b><br><b>el</b> hij<b>o</b> / <b>la</b> hij<b>a</b> · <b>el</b> niñ<b>o</b> / <b>la</b> niñ<b>a</b></p></div>
<div class="box y"><b>② 남성 복수 = 섞인 무리 전체</b>
<p><b>los padres</b> = 아버지 + 어머니 (부모님)<br><b>los hermanos</b> = 형제자매 전체<br><b>los abuelos</b> = 할아버지 + 할머니<br><b>los hijos</b> = 아들 + 딸 (자녀)</p></div></div>
<table class="t"><tr><th>③ 누구의?</th><th>단수 명사 앞</th><th>복수 명사 앞</th><th>예</th></tr>
<tr><td>나의</td><td><b>mi</b></td><td><b>mis</b></td><td>mi padre · <b>mis</b> padres</td></tr>
<tr><td>너의</td><td><b>tu</b></td><td><b>tus</b></td><td>tu madre · <b>tus</b> abuelos</td></tr>
<tr><td>그(녀)의</td><td><b>su</b></td><td><b>sus</b></td><td>su familia · <b>sus</b> hermanos</td></tr></table>
<div class="note r"><b>tu ≠ tú</b> 강세 없는 <b>tu</b>는 '너의'(tu familia), 강세 있는 <b>tú</b>는 '너'(¿Y tú?)예요.</div>
<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 선생님 역할. 아버지 Carlos, 어머니 Ana, 남동생 David. · <b class="cM">Mateo</b> — 따라 말하며 배워요. 아버지 Juan, 어머니 María, 남자 형제 한 명, 4인 가족. · <b class="cT">Tú (나)</b> — 내 가족을 소개할 청취자!</p>
</section>""")

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 4), "가족의 크기와 부모님 이름", "팟캐스트 1. 오프닝 · 2. 크다/작다 · 3. 아버지 · 어머니",
    ["<b>Mi familia es grande / pequeña.</b>로 가족 크기를 말할 수 있다.", "<b>Mi padre se llama … / Mi madre se llama …</b>로 부모님 이름을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Hoy hablamos de la familia", "Tu padre, tu madre", "Mi familia es pequeña. O:", "¿Tu familia es grande, Mateo", "Mi familia es pequeña.", "Mi padre se llama Carlos.", "¿Cómo se llama tu padre", "Mi padre se llama Juan", "¿Y cómo se llama tu madre", "Mi madre se llama María")
 + h("문법", "llamarse — 이름이 ~이다")
 + """<table class="t"><tr><th>누구?</th><th>llamarse</th><th>예문</th></tr>
<tr><td>나</td><td><b>me llamo</b></td><td>Me llamo Sofía. 제 이름은 소피아예요.</td></tr>
<tr><td>너</td><td><b>te llamas</b></td><td>¿Cómo te llamas? 이름이 뭐예요?</td></tr>
<tr><td>그 / 그녀 / 아버지 / 어머니</td><td><b>se llama</b></td><td>Mi padre <b>se llama</b> Carlos. · ¿Cómo <b>se llama</b> tu madre?</td></tr>
<tr><td>그들 (여러 명)</td><td><b>se llaman</b></td><td>Mis hermanos <b>se llaman</b> Pablo y Luis.</td></tr></table>
<div class="note g"><b>grande / pequeña</b> familia가 여성 명사라서 <b>pequeña</b>(-a)예요. grande는 남녀 같은 형태.
<br>한국어 '대가족 / 단출한 가족'에 가까워요: <b>Mi familia es grande.</b> 우리 집은 식구가 많아요.
<br><b>también</b> = ~도: Mi familia <b>también</b> es pequeña. 우리 가족도 작아요.</div>
""" + h("단어", "부모님") + """
<div class="grid5"><div>👨 <b>el padre</b><br>아버지</div><div>👩 <b>la madre</b><br>어머니</div><div>👨‍👩 <b>los padres</b><br>부모님</div><div>🧔 <b>papá</b><br>아빠</div><div>👩‍🦰 <b>mamá</b><br>엄마</div></div>
<p class="sm"><b>los padres</b>는 '아버지들'이 아니라 '부모님'이에요. 친척은 <b>los parientes</b>(+보너스)라고 해요.</p>"""
 + h("연습 A", "알맞은 관사 el / la / los를 쓰세요.")
 + '<div class="grid4">' + "".join(f'<div>{BS} {w}</div>' for w in ["padre", "madre", "padres", "familia", "hermano", "hermana", "abuelos", "hija"]) + "</div>"
 + h("연습 B", "빈칸을 채우세요.")
 + blanks([f"Mi padre {BS} llama Juan.", f"¿Cómo se {BS} tu madre?", f"Mi familia es (작은) {B}.", f"Mi familia {BS} es pequeña. (우리 가족도)", f"Yo {BS} llamo Ana."])
 + h("말하기", "소피아의 질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Tu familia es grande o pequeña?"), ("Sofía", "¿Cómo se llama tu padre?"), ("Sofía", "¿Y cómo se llama tu madre?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(4, 6), "형제자매와 가족 수", "팟캐스트 4. 형제자매 · 5. 가족은 몇 명?",
    ["<b>¿Tienes hermanos?</b>에 <b>Tengo un hermano / No tengo hermanos</b>로 대답할 수 있다.", "<b>¿Cuántas personas hay en tu familia? — Somos cuatro.</b>로 가족 수를 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Si tienes uno, dices", "Si no tienes, dices", "¿Tienes hermanos, Mateo?", "¿Tienes un hermano o una", "Tengo un hermano.", "Ah, tienes un hermano", "No, no tengo hermanas", "Mi familia: somos cuatro", "¿Cuántas personas hay", "Tres… cuatro", "Somos cuatro. Perfecto")
 + h("문법 ①", "tener — 있어요 / 없어요")
 + """<div class="two"><div class="box y"><b>있어요 (Tengo + un/una)</b>
<p><b>Tengo un hermano.</b> 남자 형제가 한 명 있어요.<br><b>Tengo una hermana.</b> 여자 형제가 한 명 있어요.<br><b>Tengo dos hermanos.</b> 형제가 두 명 있어요.</p></div>
<div class="box y"><b>없어요 (No tengo + 복수)</b>
<p><b>No tengo hermanos.</b> 형제자매가 없어요.<br><b>No tengo hermanas.</b> 여자 형제는 없어요.<br>→ 없을 때는 un/una 없이 <b>복수형</b>!</p></div></div>
<table class="t"><tr><th>tener (가지다)</th><th>yo</th><th>tú</th><th>él / ella</th><th>nosotros</th></tr>
<tr><td>현재형</td><td><b>tengo</b></td><td><b>tienes</b></td><td><b>tiene</b></td><td><b>tenemos</b></td></tr></table>
""" + h("문법 ②", "몇 명이에요? — hay / somos") + """
<div class="two"><div class="box y"><b>묻기</b>
<p><b>¿Cuántas personas hay en tu familia?</b><br>가족이 몇 명이에요? (persona는 여성 → cuánt<b>as</b>)<br><b>¿Cuántos hermanos tienes?</b> 형제가 몇 명이에요?</p></div>
<div class="box y"><b>대답하기</b>
<p><b>Somos cuatro.</b> 우리는 네 명이에요. (ser → nosotros <b>somos</b>)<br>Mi padre, mi madre, mi hermano y yo. 아빠, 엄마, 형(동생), 그리고 나.</p></div></div>
<div class="note y"><b>한국어의 형·오빠·누나·언니는?</b> 스페인어는 나이로 부르지 않아요. 필요하면 <b>mayor</b>(나이 많은) / <b>menor</b>(어린)를 붙여요: <b>mi hermano mayor</b> 형/오빠 · <b>mi hermana menor</b> 여동생</div>"""
 + h("연습 A", "그림을 보고 문장을 완성하세요.")
 + blanks([f"👦 → Tengo {B}.", f"👧 → Tengo {B}.", f"👦👦 → Tengo {B}.", f"🙅 → {B}.", f"👨👩👦🧑 → Somos {B}."])
 + h("연습 B", "알맞은 말을 고르세요.")
 + blanks(["No tengo (un hermano / hermanos).", "¿(Cuántos / Cuántas) personas hay en tu familia?", "Mateo (tengo / tiene) un hermano.", "Mi familia: (somos / son) cinco."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Tienes hermanos?"), ("Sofía", "¿Cuántas personas hay en tu familia?"))
 + "</section>")

# ---------- Lesson 3 ----------
P.append(lesson(3, rng(6, 9), "자녀 · 조부모 · 함께 살아요", "팟캐스트 6. 자녀 · 7. 할아버지·할머니 · 8. 모아서 말하기",
    ["<b>hijo / hija / abuelo / abuela</b>를 써서 가족을 더 소개할 수 있다.", "<b>Vivo con mi familia. Quiero a mi familia.</b>를 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Tengo un hijo. Es un niño", "Tengo una hija. Es una", "Tengo dos hijos", "¿Tienes hijos, Mateo?", "No, no tengo hijos", "Mi abuelo se llama Pedro. Mi abuela se llama Carmen.", "¿Tienes abuelos", "Sí, tengo abuelos", "Mi familia es pequeña. Tengo", "Vivo con mi familia. Quiero a")
 + h("문법", "vivir con (함께 살다) · querer a (사랑하다)")
 + """<div class="two"><div class="box y"><b>vivir con + 사람</b>
<p><b>Vivo con mi familia.</b> 가족과 함께 살아요.<br>¿<b>Vives con</b> tu familia? 가족과 함께 살아요?<br>Javier <b>vive con</b> su familia. 하비에르는 가족과 살아요.<br>+ Vivo <b>solo / sola</b>. 혼자 살아요. (+보너스)</p></div>
<div class="box y"><b>querer a + 사람 = 사랑하다</b>
<p><b>Quiero a mi familia.</b> 가족을 사랑해요.<br><b>Quiero mucho a</b> mi familia. 아주 많이 사랑해요.<br>¿<b>Quieres a</b> tu familia? 가족을 사랑해요?</p></div></div>
<div class="note g"><b>사람 앞의 a</b> 사람을 목적어로 할 때는 앞에 <b>a</b>를 넣어요: Quiero <b>a</b> mi familia. (사물이면 a 없이: Quiero un café. 커피 한 잔 주세요/원해요)
<br><b>Me gusta mi familia.</b> (하비에르 이야기)도 자연스럽지만, 가족에게는 <b>Quiero a …</b>가 더 따뜻한 표현이에요.</div>
""" + h("단어", "자녀와 조부모") + """
<table class="t"><tr><td>👦 <b>el hijo</b></td><td>아들</td><td>👴 <b>el abuelo</b></td><td>할아버지</td></tr>
<tr><td>👧 <b>la hija</b></td><td>딸</td><td>👵 <b>la abuela</b></td><td>할머니</td></tr>
<tr><td>👧👦 <b>los hijos</b></td><td>자녀 (아들+딸)</td><td>👴👵 <b>los abuelos</b></td><td>조부모님</td></tr>
<tr><td><b>el niño / la niña</b></td><td>남자아이 / 여자아이</td><td><b>el esposo / la esposa</b></td><td>남편 / 아내 (+보너스)</td></tr></table>"""
 + h("연습 A", "동사를 알맞게 바꾸세요.")
 + blanks([f"Yo (vivir) {BS} con mi familia.", f"¿Tú (vivir) {BS} con tus padres?", f"Laura (vivir) {BS} con su familia.", f"Yo (querer) {BS} a mi familia.", f"¿Tú (tener) {BS} hijos?"])
 + h("연습 B", "빈칸에 a를 넣어야 하면 a, 아니면 ✗를 쓰세요.")
 + blanks([f"Quiero {BS} mi familia.", f"Quiero {BS} un café.", f"Quiero mucho {BS} mis abuelos."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Tienes hijos?"), ("Sofía", "¿Tienes abuelos?"), ("Sofía", "¿Vives con tu familia?"))
 + "</section>")

# ---------- Lesson 4 ----------
iL = find("Hola, me llamo Laura")
iJ = find("Hola, me llamo Javier")
P.append(lesson(4, rng(9, 11), "듣기: 라우라와 하비에르의 가족", "팟캐스트 9. 라우라 이야기 · 10. 하비에르 이야기",
    ["짧은 가족 이야기를 듣고 가족 수·이름·형제를 파악할 수 있다.", "<b>Se llama … / Tiene … / Vive con su familia</b>로 다른 사람의 가족을 말할 수 있다."])
 + h("듣기 ①", f"La familia de Laura — 라우라 이야기 ({fmt(T[iL])})")
 + '<div class="story">Hola, me llamo Laura. Mi familia es grande. Mi padre se llama Miguel. Mi madre se llama Sofía. Tengo dos hermanos. Se llaman Pablo y Luis. Tengo una hermana, se llama Elena. Vivo con mi familia. Quiero mucho a mi familia.</div>'
 + h("이해 확인", "라우라의 가족표를 채우세요.")
 + '<table class="t fill"><tr><th>가족 크기</th><th>아버지</th><th>어머니</th><th>남자 형제</th><th>여자 형제</th></tr><tr><td></td><td></td><td></td><td></td><td></td></tr></table>'
 + h("듣기 ②", f"La familia de Javier — 하비에르 이야기 ({fmt(T[iJ])})")
 + '<div class="story">Hola, me llamo Javier. Mi familia es pequeña. Mi padre se llama Roberto. Mi madre se llama Carmen. No tengo hermanos. No tengo hermanas. Tengo un hijo. Se llama Pedro. Vivo con mi familia. Me gusta mi familia.</div>'
 + h("이해 확인", "질문에 스페인어로 답하세요.")
 + blanks([f"¿La familia de Javier es grande o pequeña? {B}", f"¿Cuántos hermanos tiene Javier? {B}", f"¿Cómo se llama su madre? {B}", f"¿Tiene hijos Javier? ¿Cómo se llama? {B}", f"¿Vive con su familia? {B}"])
 + h("문법", "나 → 그/그녀로 바꾸기")
 + """<table class="t"><tr><th>본인이 말할 때 (yo)</th><th>남이 말할 때 (él / ella)</th></tr>
<tr><td><b>Me llamo</b> Laura.</td><td><b>Se llama</b> Laura.</td></tr>
<tr><td><b>Mi</b> familia es grande.</td><td><b>Su</b> familia es grande.</td></tr>
<tr><td><b>Tengo</b> dos hermanos.</td><td><b>Tiene</b> dos hermanos.</td></tr>
<tr><td><b>No tengo</b> hermanas.</td><td><b>No tiene</b> hermanas.</td></tr>
<tr><td><b>Vivo</b> con <b>mi</b> familia.</td><td><b>Vive</b> con <b>su</b> familia.</td></tr>
<tr><td><b>Quiero</b> mucho a <b>mi</b> familia.</td><td><b>Quiere</b> mucho a <b>su</b> familia.</td></tr></table>"""
 + h("응용", "라우라 이야기를 3인칭으로 바꿔 쓰세요.")
 + f'<p class="fillp">Ella {BS} Laura. {BS} familia es grande. {BS} padre se llama Miguel. {BS} dos hermanos. {BS} con su familia.</p>'
 + "</section>")

# ---------- Lesson 5 ----------
iR = find("Excelente, Mateo. Todo lo tienes")
P.append(lesson(5, rng(11, None), "나의 가족 소개하기", "팟캐스트 11. 네 차례 · 12. 이어 말하기 · 13. 혼자서 소개하기 · 14. 빠른 복습 · 15. 마지막 도전",
    ["가족에 대한 질문 6개에 멈추지 않고 대답할 수 있다.", "<b>6–8문장</b>으로 내 가족을 소개할 수 있다."])
 + h("예시", "소피아와 마테오의 가족 소개")
 + '<div class="two"><div class="story"><b class="cS">Sofía</b><br>Hola, me llamo Sofía. Mi familia es pequeña. Mi padre se llama Carlos. Mi madre se llama Ana. Tengo un hermano. Mi hermano se llama David. No tengo hermanas. Vivo con mi familia. Quiero mucho a mi familia.</div>'
 + '<div class="story"><b class="cM">Mateo</b><br>Hola, me llamo Mateo. Mi familia es pequeña. Mi padre se llama Juan. Mi madre se llama María. Tengo un hermano. No tengo hermanas. Vivo con mi familia. Quiero mucho a mi familia.</div></div>'
 + h("복습", "tu → mi로 바꿔 말하기 (팟캐스트 14번 구간)")
 + '<div class="grid4"><div>tu padre → <b>mi padre</b></div><div>tu madre → <b>mi madre</b></div><div>tus padres → <b>mis padres</b></div><div>tu familia → <b>mi familia</b></div></div>'
 + blanks([f"tu hermano → {B}", f"tus abuelos → {B}", f"tu hija → {B}", f"tus hermanas → {B}"])
 + h("최종 시험", f"Háblame de tu familia — 새로 만난 사람에게 대답하세요! ({fmt(T[iR])})")
 + '<p class="sm">플레이어에서 해당 문장부터 재생하고, 소피아가 질문한 뒤 마테오가 대답하기 전에 먼저 말해 보세요.</p>'
 + ask(("Sofía", "¿Tu familia es grande o pequeña?"), ("Sofía", "¿Tienes hermanos?"), ("Sofía", "¿Cómo se llama tu padre?"), ("Sofía", "¿Y tu madre?"), ("Sofía", "¿Vives con tu familia?"), ("Sofía", "¿Quieres a tu familia?"))
 + h("최종 미션", "나의 가족 소개 (Mi familia)")
 + """<table class="t mine"><tr><th>항목</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 인사 · 이름</td><td><b>Hola, me llamo …</b></td><td></td></tr>
<tr><td>② 가족 크기 · 수</td><td><b>Mi familia es … Somos …</b></td><td></td></tr>
<tr><td>③ 부모님</td><td><b>Mi padre se llama … Mi madre se llama …</b></td><td></td></tr>
<tr><td>④ 형제자매</td><td><b>Tengo … / No tengo hermanos.</b></td><td></td></tr>
<tr><td>⑤ 자녀 · 조부모 (선택)</td><td><b>Tengo un hijo / una hija … · Mis abuelos …</b></td><td></td></tr>
<tr><td>⑥ 함께 사는 사람</td><td><b>Vivo con …</b></td><td></td></tr>
<tr><td>⑦ 마무리</td><td><b>Quiero mucho a mi familia.</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> Hola, me llamo Jisu. Mi familia es grande. Somos cinco. Mi padre se llama Minho. Mi madre se llama Eunhee. Tengo dos hermanas. No tengo hermanos. Tengo una hija, se llama Yuna. Vivo con mi esposo y mi hija. Quiero mucho a mi familia.</div>
<p class="sm">한국 이름은 그대로 써요. 결혼했다면: <b>Vivo con mi esposo / mi esposa y mis hijos.</b> 남편/아내, 아이들과 함께 살아요.</p>
""" + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>우리 가족이 대가족인지 작은 가족인지, 몇 명인지 말할 수 있다.</li><li>부모님 이름을 se llama로 말할 수 있다.</li><li>형제자매가 있는지 없는지 tener로 말할 수 있다.</li><li>padre/padres, hermano/hermanos 등 남성 복수가 무리 전체를 뜻한다는 걸 안다.</li><li>mi/mis, tu/tus, su/sus를 구분할 수 있다.</li><li>Vivo con mi familia. Quiero a mi familia.를 말할 수 있다.</li><li>마지막 도전(' + fmt(T[iR]) + ')에서 멈추지 않고 대답할 수 있다.</li></ul>'
 + '<p class="sm">팟캐스트의 마지막 말: <b>Ya puedes hablar de tu familia en español. ¡Felicidades!</b> — 이제 스페인어로 가족 이야기를 할 수 있어요. 축하해요!</p>'
 + "</section>")

# ---------- Appendix ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: el padre · la madre · los padres · la familia · el hermano · la hermana · los abuelos · la hija &nbsp;|&nbsp; B: 1 se · 2 llama · 3 pequeña · 4 también · 5 me</p>
<p><b>Lesson 2</b> A: 1 un hermano · 2 una hermana · 3 dos hermanos · 4 No tengo hermanos · 5 cuatro &nbsp;|&nbsp; B: 1 hermanos · 2 Cuántas · 3 tiene · 4 somos</p>
<p><b>Lesson 3</b> A: 1 vivo · 2 vives · 3 vive · 4 quiero · 5 tienes &nbsp;|&nbsp; B: 1 a · 2 ✗ · 3 a</p>
<p><b>Lesson 4</b> 라우라 표: grande · Miguel · Sofía · dos (Pablo y Luis) · una (Elena)<br>
하비에르: 1 Es pequeña. · 2 No tiene hermanos. · 3 Se llama Carmen. · 4 Sí, tiene un hijo. Se llama Pedro. · 5 Sí, vive con su familia.<br>
응용: se llama · Su · Su · Tiene · Vive</p>
<p><b>Lesson 5</b> 복습: mi hermano · mis abuelos · mi hija · mis hermanas</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">이번 에피소드의 핵심 동사예요. 우선 yo / tú / él·ella 세 줄만 외워도 충분해요.</p>
<table class="t"><tr><th>주어</th><th>ser (이다)</th><th>tener (가지다)</th><th>llamarse (이름이 ~이다)</th><th>vivir (살다)</th><th>querer (사랑하다, 원하다)</th></tr>
<tr><td>yo</td><td>soy</td><td>tengo</td><td>me llamo</td><td>vivo</td><td>quiero</td></tr>
<tr><td>tú</td><td>eres</td><td>tienes</td><td>te llamas</td><td>vives</td><td>quieres</td></tr>
<tr><td>él / ella / usted</td><td>es</td><td>tiene</td><td>se llama</td><td>vive</td><td>quiere</td></tr>
<tr><td>nosotros/as</td><td>somos</td><td>tenemos</td><td>nos llamamos</td><td>vivimos</td><td>queremos</td></tr>
<tr><td>vosotros/as</td><td>sois</td><td>tenéis</td><td>os llamáis</td><td>vivís</td><td>queréis</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>son</td><td>tienen</td><td>se llaman</td><td>viven</td><td>quieren</td></tr></table>
<p class="sm">tener와 querer는 e가 ie로 바뀌어요(tienes, quiero). 단, nosotros·vosotros에서는 안 바뀌어요.</p>
</section>""")

voc = ['<section class="lesson"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'단어장\' 탭과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 가족 교재 Ep4</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
