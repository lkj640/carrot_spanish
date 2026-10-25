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
END = 23 * 60 + 9

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
<div class="ct"><h1>왕초보 스페인어<br>가장 친한 친구 소개하기</h1>
<div class="cs">Easy Spanish Podcast Ep.7 · A1 입문 · 4주차</div>
<div class="big">Mi mejor amigo se llama Pablo.</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · 남성/여성 맞추기 (amigo / amiga)</td></tr>
<tr><th>LESSON 1</th><td>이름 · 나이 · 사는 곳 · se llama / tiene / vive</td></tr>
<tr><th>LESSON 2</th><td>성격과 외모 · Es muy amable / Es alto</td></tr>
<tr><th>LESSON 3</th><td>함께 하는 일과 이유 · Vemos películas / porque me escucha</td></tr>
<tr><th>LESSON 4</th><td>듣기: 라우라와 아나 · 후안과 루이스</td></tr>
<tr><th>LESSON 5</th><td>한 단계씩 완성 · 나의 친구 소개 · 마지막 도전</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 11월 8일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기 · 23분으로 길어서 두 번에 나눠 들어도 좋아요 (1–7번 / 8–14번 구간)</div></div>
<div class="stripe"></div></section>""")

# ---------- intro ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 발음과 남성·여성 맞추기</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. 이번 에피소드는 마테오가 친구 <b>파블로</b>를 소개해요. 들으면서 내 친구로 바꿔 말해 보세요!</div>
""" + h("발음", "이번 에피소드에 나오는 주의할 소리") + """
<table class="t"><tr><th>글자</th><th>소리</th><th>예</th></tr>
<tr><td><b>j</b></td><td>목에서 나는 강한 ㅎ</td><td><b>juntos</b> 훈또스 · <b>joven</b> 호벤 · <b>trabajador</b> 뜨라바하도르</td></tr>
<tr><td><b>ll</b></td><td>'y'처럼 — 야/요</td><td><b>se llama</b> 세 야마 · <b>ella</b> 에야</td></tr>
<tr><td><b>v</b> = <b>b</b></td><td>둘 다 'ㅂ'에 가까워요</td><td><b>vive</b> 비베 · <b>Valencia</b> 발렌씨아 · <b>vemos</b> 베모스</td></tr>
<tr><td><b>c + e, i</b> / <b>z</b></td><td>스페인: 영어 th / 중남미: ㅆ</td><td><b>cenar</b> 쎄나르 · <b>Barcelona</b> 바르쎌로나 · <b>Valencia</b></td></tr>
<tr><td><b>gu + e, i</b></td><td>'게·기' (u는 읽지 않음)</td><td><b>amigue</b>(X) → <b>amigo</b> 아미고 · <b>guitarra</b> 기따라 +보너스</td></tr>
<tr><td><b>강세 부호</b></td><td>표시된 곳을 세게</td><td>simp<b>á</b>tico · pel<b>í</b>culas · m<b>ú</b>sica · f<b>ú</b>tbol</td></tr>
</table>
<p class="sm">※ 한글 표기는 감을 잡기 위한 참고용이에요. 정확한 소리는 꼭 팟캐스트로 들어 보세요.</p>
""" + h("문법 0", "남자 친구면 -o, 여자 친구면 -a") + """
<table class="t"><tr><th></th><th>남자 (él)</th><th>여자 (ella)</th></tr>
<tr><td>가장 친한 친구</td><td>mi mejor amig<b>o</b></td><td>mi mejor amig<b>a</b></td></tr>
<tr><td>상냥한</td><td>Es muy simpátic<b>o</b>.</td><td>Es muy simpátic<b>a</b>.</td></tr>
<tr><td>재미있는</td><td>Es muy divertid<b>o</b>.</td><td>Es muy divertid<b>a</b>.</td></tr>
<tr><td>키가 큰</td><td>Es alt<b>o</b>.</td><td>Es alt<b>a</b>.</td></tr>
<tr><td>함께</td><td>Vemos películas junt<b>os</b>.</td><td>Vemos películas junt<b>as</b>. (여자끼리)</td></tr>
<tr><td>-e · 자음 끝 (같은 형태)</td><td colspan="2">amable · inteligente · joven · mayor</td></tr></table>
<div class="note g"><b>mejor</b> = 가장 좋은. <b>mejor</b>는 남녀 형태가 같아요: mi <b>mejor</b> amigo / mi <b>mejor</b> amiga.
<br><b>Amigo para chico, amiga para chica.</b> — 마테오가 정리한 규칙 (남자는 amigo, 여자는 amiga)</div>
<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 질문하고 시범을 보여 줘요. · <b class="cM">Mateo</b> — 가장 친한 친구 <b>Pablo</b>를 소개해요. 파블로는 30살, 발렌시아에 살고, 친절하고 재미있는 사람. · <b class="cT">Tú (나)</b> — 내 친구를 소개할 청취자!</p>
</section>""")

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 4), "친구의 이름 · 나이 · 사는 곳", "팟캐스트 1. 오프닝 · 2. 이름 · 3. 나이와 사는 곳",
    ["<b>Mi mejor amigo/a se llama …</b>로 친구 이름을 말할 수 있다.", "<b>Tiene … años. Vive en …</b>으로 친구의 나이와 사는 곳을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("¿Tienes un mejor amigo o", "Sí. Sí, tengo un mejor", "Muy bien. Para empezar", "Mi mejor amigo se llama Pablo.", "Ahora, si tuvieras", "Sí, sí. Amigo para chico", "Perfecto. Pablo…", "Pablo tiene 30 años", "¿Y dónde vive Pablo?", "No, no. Vive en Valencia")
 + h("문법", "친구(그/그녀)에 대해 말할 때는 3인칭")
 + """<table class="t"><tr><th>무엇?</th><th>나 (yo)</th><th>친구 (él / ella)</th><th>묻기 (그 친구는?)</th></tr>
<tr><td>이름</td><td>Me llamo …</td><td><b>Se llama</b> Pablo.</td><td>¿Cómo se llama?</td></tr>
<tr><td>나이</td><td>Tengo … años.</td><td><b>Tiene</b> 30 años.</td><td>¿Cuántos años tiene?</td></tr>
<tr><td>사는 곳</td><td>Vivo en …</td><td><b>Vive</b> en Valencia.</td><td>¿Dónde vive?</td></tr></table>
<div class="note g"><b>tu ciudad</b> = 너의 도시 · ¿Vive en tu ciudad? 너랑 같은 도시에 살아?
<br>감탄 표현: <b>¡Qué + 명사 + tan + 형용사!</b> ¡Qué nombre <b>tan</b> bonito! 정말 예쁜 이름이네! · ¡Qué ciudad <b>tan</b> bonita! 정말 아름다운 도시네!</div>
""" + h("숫자", "나이 말하기 (20–50)") + """
<div class="grid5"><div><b>20</b> veinte</div><div><b>25</b> veinticinco</div><div><b>30</b> treinta</div><div><b>35</b> treinta y cinco</div><div><b>40</b> cuarenta</div></div>
<p class="sm">45 cuarenta y cinco · 50 cincuenta · 60 sesenta — 31부터는 십의 자리 + <b>y</b> + 일의 자리</p>"""
 + h("연습 A", "amigo / amiga 중 알맞은 것을 쓰세요.")
 + blanks([f"Mi mejor {BS} se llama Ana.", f"Mi mejor {BS} se llama Pablo.", f"Laura es mi mejor {BS}.", f"Luis es el mejor {BS} de Juan."])
 + h("연습 B", "친구 카드를 보고 문장을 쓰세요.")
 + blanks([f"Pablo · 30 · Valencia → Mi mejor amigo se llama Pablo. {B}. {B}.", f"Ana · 25 · Madrid → Mi mejor amiga {B}. {B}. {B}.", f"Luis · 40 · Barcelona → {B}."])
 + h("말하기", "소피아의 질문에 내 친구로 답하세요")
 + ask(("Sofía", "¿Tienes un mejor amigo o una mejor amiga?"), ("Sofía", "¿Cómo se llama?"), ("Sofía", "¿Cuántos años tiene? ¿Dónde vive?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(4, 6), "성격과 외모", "팟캐스트 4. 성격 · 5. 외모",
    ["<b>¿Cómo es? — Es muy amable / simpático / divertido …</b>로 친구의 성격을 말할 수 있다.", "<b>Es alto / bajo / joven / mayor</b>로 외모를 말하고, 친구 성에 맞게 형용사를 바꿀 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Ahora vamos a hablar de cómo es", "Muy bien. Amable significa", "Otro ejemplo", "Genial. Si fuera una chica", "Sí, sí. Pablo es muy amable", "¡Qué bien, dos adjetivos", "Sí, es muy divertido", "Muy bien. ¿Es tranquilo", "Ahora, un poco sobre su aspecto", "Genial. ¿Y es joven", "Es joven. 30 años")
 + h("문법", "성격·외모 = ser + 형용사")
 + """<table class="t"><tr><th>성격</th><th>뜻</th><th>외모</th><th>뜻</th></tr>
<tr><td><b>amable</b></td><td>친절한</td><td><b>alto / alta</b></td><td>키가 큰</td></tr>
<tr><td><b>simpático / simpática</b></td><td>상냥한, 호감 가는</td><td><b>bajo / baja</b></td><td>키가 작은</td></tr>
<tr><td><b>divertido / divertida</b></td><td>재미있는</td><td><b>joven</b></td><td>젊은</td></tr>
<tr><td><b>inteligente</b></td><td>똑똑한</td><td><b>mayor</b></td><td>나이가 많은</td></tr>
<tr><td><b>tranquilo / tranquila</b></td><td>차분한</td><td><b>guapo / guapa</b> +보너스</td><td>잘생긴 / 예쁜</td></tr>
<tr><td><b>activo / activa</b></td><td>활동적인</td><td></td><td></td></tr></table>
<div class="note g"><b>여러 개 이어 말하기</b> Pablo es amable, simpático, divertido, inteligente <b>y</b> tranquilo. — 마지막 앞에만 <b>y</b>(그리고)
<br><b>muy</b> = 아주: Es <b>muy</b> amable. · <b>¿A o B?</b>로 묻기: ¿Es tranquilo <b>o</b> es muy activo? ¿Es alto <b>o</b> es bajo?</div>
<div class="note r"><b>simpático ≠ sympathetic</b> 스페인어 simpático는 '동정하는'이 아니라 '상냥하고 호감 가는'이에요. 한국어로는 '사람 좋다'에 가까워요.</div>"""
 + h("연습 A", "친구 성에 맞게 형용사를 바꾸세요.")
 + blanks([f"Ana es muy (simpático) → {B}", f"Pablo es muy (divertido) → {B}", f"Mi mejor amiga es (alto) → {B}", f"Luis es (tranquilo) y (trabajador) → {B}", f"Laura es (amable) → {B}"])
 + h("연습 B", "반대말끼리 연결하세요.")
 + '<table class="t match"><tr><td>① alto</td><td>ⓐ mayor</td></tr><tr><td>② joven</td><td>ⓑ activo</td></tr><tr><td>③ tranquilo</td><td>ⓒ bajo</td></tr></table>'
 + h("말하기", "질문에 내 친구로 답하세요")
 + ask(("Sofía", "¿Cómo es tu mejor amigo/a? Dime tres adjetivos."), ("Sofía", "¿Es alto/a o bajo/a? ¿Es joven o mayor?"))
 + "</section>")

# ---------- Lesson 3 ----------
P.append(lesson(3, rng(6, 8), "함께 하는 일과 이유", "팟캐스트 6. 함께 하는 일 · 7. 왜 가장 친한 친구예요?",
    ["<b>nosotros</b>(우리) 동사로 친구와 함께 하는 일을 말할 수 있다.", "<b>Es mi mejor amigo porque …</b>로 이유를 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Mmm, nos gusta mucho hablar", "No jugamos al fútbol", "Sí. Vemos películas. Nos gusta", "Sí. Salimos juntos. Vamos", "Mmm, es mi mejor amigo porque", "Es mi mejor amigo porque es amable, me escucha y me ayuda mucho.")
 + h("문법 ①", "우리는 ~해요 — nosotros 동사")
 + """<table class="t"><tr><th>동사원형</th><th>우리는 (nosotros)</th><th>너희는 / 그들은 (ustedes · ellos)</th><th>예문</th></tr>
<tr><td>hablar 말하다</td><td><b>hablamos</b></td><td>hablan</td><td>Hablamos mucho.</td></tr>
<tr><td>escuchar 듣다</td><td><b>escuchamos</b></td><td>escuchan</td><td>Escuchamos música.</td></tr>
<tr><td>estudiar 공부하다</td><td><b>estudiamos</b></td><td>estudian</td><td>No estudiamos juntos.</td></tr>
<tr><td>ver 보다</td><td><b>vemos</b></td><td>ven</td><td>Vemos películas.</td></tr>
<tr><td>salir 나가다</td><td><b>salimos</b></td><td>salen</td><td>Salimos juntos.</td></tr>
<tr><td>jugar 놀다, 운동하다</td><td><b>jugamos</b></td><td>juegan</td><td>No jugamos al fútbol.</td></tr>
<tr><td>ir 가다</td><td><b>vamos</b></td><td>van</td><td>Vamos a cenar. · Vamos a tomar café.</td></tr></table>
<div class="note g"><b>nos gusta</b> = 우리는 ~을 좋아해요: <b>Nos gusta</b> hablar. <b>Nos gusta</b> ver películas de acción.
<br>남이 말할 때는 <b>les gusta</b>: A Juan y Luis <b>les gusta</b> cenar. · <b>ir a + 동사원형</b> = ~하러 가다: Vamos <b>a</b> cenar.</div>
""" + h("문법 ②", "이유 말하기 — porque + 문장") + """
<div class="two"><div class="box y"><b>¿Por qué …? 왜?</b>
<p><b>¿Por qué</b> es Pablo tu mejor amigo?<br>파블로는 왜 가장 친한 친구예요?</p></div>
<div class="box y"><b>porque … ~때문에</b>
<p>Es mi mejor amigo <b>porque</b> es muy amable.<br>… <b>porque me escucha</b> 내 말을 들어 주니까<br>… <b>porque me ayuda mucho</b> 나를 많이 도와주니까</p></div></div>
<p class="sm"><b>¿Por qué?</b>(왜, 띄어 쓰고 강세)와 <b>porque</b>(왜냐하면, 붙여 씀)는 다른 말이에요. · me = 나를/나에게: Me escucha. Me ayuda.</p>"""
 + h("연습 A", "nosotros 형태로 바꾸세요.")
 + blanks([f"(escuchar) {BS} música.", f"(ver) {BS} películas juntos.", f"(salir) {BS} a cenar.", f"(hablar) {BS} mucho.", f"(ir) {BS} a tomar café."])
 + h("연습 B", "이유를 완성하세요.")
 + blanks([f"Es mi mejor amiga porque {B}. (상냥해서)", f"Es mi mejor amigo porque {B}. (내 말을 들어 줘서)", f"Es mi mejor amigo porque {B}. (나를 많이 도와줘서)"])
 + h("말하기", "질문에 내 친구로 답하세요")
 + ask(("Sofía", "¿Qué hacen juntos? Dime dos cosas."), ("Sofía", "¿Por qué es tu mejor amigo/a?"))
 + "</section>")

# ---------- Lesson 4 ----------
iL = find("Hola, me llamo Laura")
iJ = find("Hola, soy Juan")
P.append(lesson(4, rng(8, 10), "듣기: 라우라와 아나 · 후안과 루이스", "팟캐스트 8. 라우라와 아나 · 9. 작은 도전",
    ["친구 소개를 듣고 이름·나이·사는 곳·성격·함께 하는 일을 파악할 수 있다.", "<b>Se llama … / Tiene … / Es … / Les gusta …</b>로 대답할 수 있다."])
 + h("듣기 ①", f"La mejor amiga de Laura — 라우라 이야기 ({fmt(T[iL])})")
 + '<div class="story">Hola, me llamo Laura. Mi mejor amiga se llama Ana. Tiene 25 años. Vive en Madrid. Ana es muy simpática, es inteligente, también es divertida. Nos gusta escuchar música. Vemos películas juntas. Pasamos mucho tiempo juntas. Me gusta estar con ella.</div>'
 + h("이해 확인", "아나에 대한 표를 채우세요.")
 + '<table class="t fill"><tr><th>이름</th><th>나이</th><th>사는 곳</th><th>성격 (3개)</th><th>함께 하는 일</th></tr><tr><td></td><td></td><td></td><td></td><td></td></tr></table>'
 + h("듣기 ②", f"Un pequeño reto — 후안 이야기 ({fmt(T[iJ])})")
 + '<div class="story">Hola, soy Juan. Mi mejor amigo se llama Luis. Tiene 40 años. Vive en Barcelona. Luis es muy tranquilo y es muy trabajador. También es muy bueno. Nos gusta salir a caminar y nos gusta cenar. Pasamos un buen rato. Me gusta mucho su compañía.</div>'
 + h("이해 확인", "질문에 스페인어로 답하세요.")
 + blanks([f"¿Cómo se llama el mejor amigo de Juan? {B}", f"¿Cuántos años tiene Luis? {B}", f"¿Dónde vive Luis? {B}", f"¿Cómo es Luis? {B}", f"¿Qué hacen juntos Juan y Luis? {B}"])
 + h("문법", "우리 → 그들로 바꾸기")
 + """<table class="t"><tr><th>본인이 말할 때 (nosotros)</th><th>남이 말할 때 (ellos / ellas)</th></tr>
<tr><td><b>Nos gusta</b> escuchar música.</td><td><b>Les gusta</b> escuchar música.</td></tr>
<tr><td><b>Vemos</b> películas juntas.</td><td><b>Ven</b> películas juntas.</td></tr>
<tr><td><b>Pasamos</b> mucho tiempo juntas.</td><td><b>Pasan</b> mucho tiempo juntas.</td></tr>
<tr><td><b>Salimos</b> a caminar.</td><td><b>Salen</b> a caminar.</td></tr></table>"""
 + h("응용", "라우라 이야기를 3인칭으로 바꿔 쓰세요.")
 + f'<p class="fillp">La mejor amiga de Laura {BS} Ana. {BS} 25 años. {BS} en Madrid. Es muy {BS}. A Laura y Ana {BS} gusta escuchar música. {BS} películas juntas.</p>'
 + "</section>")

# ---------- Lesson 5 ----------
iP = find("Ahora vamos a construir")
iR = find("Ahora, el último desafío")
P.append(lesson(5, rng(10, None), "나의 가장 친한 친구 소개하기", "팟캐스트 10. 네 차례 · 11. 한 단계씩 · 12. 마지막 발표 · 13. 빠른 복습 · 14. 마지막 도전",
    ["친구에 대한 질문 6개에 멈추지 않고 대답할 수 있다.", "<b>6–8문장</b>으로 가장 친한 친구를 소개할 수 있다."])
 + h("예시", "소피아의 모델과 마테오의 발표")
 + '<div class="two"><div class="story"><b class="cS">Sofía (modelo)</b><br>Hola, mi mejor amigo se llama Carlos. Tiene 25 años. Vive en Madrid. Es muy simpático, es inteligente. Nos gusta escuchar música. Pasamos mucho tiempo juntos. Me gusta estar con él.</div>'
 + '<div class="story"><b class="cM">Mateo</b><br>Hola. Mi mejor amigo se llama Pablo. Tiene 30 años. Vive en Valencia. Es muy amable. Es muy divertido. También es inteligente. Nos gusta hablar mucho y vemos películas juntos. Salimos a cenar. Es mi mejor amigo porque me escucha y me ayuda siempre. Me gusta mucho estar con él.</div></div>'
 + h("단계별", f"Paso a paso — 친구 소개 만들기 6단계 ({fmt(T[iP])})")
 + """<table class="t"><tr><th>단계</th><th>패턴</th><th>질문하기</th></tr>
<tr><td>① 이름</td><td><b>Mi mejor amigo/a se llama …</b></td><td>¿Cómo se llama?</td></tr>
<tr><td>② 나이</td><td><b>Tiene … años.</b></td><td>¿Cuántos años tiene?</td></tr>
<tr><td>③ 사는 곳</td><td><b>Vive en …</b></td><td>¿Dónde vive?</td></tr>
<tr><td>④ 성격 · 외모</td><td><b>Es muy … También es …</b></td><td>¿Cómo es?</td></tr>
<tr><td>⑤ 함께 하는 일</td><td><b>Nos gusta … · Vemos … · Salimos …</b></td><td>¿Qué hacen juntos?</td></tr>
<tr><td>⑥ 이유 · 마무리</td><td><b>Es mi mejor amigo/a porque … Me gusta estar con él / ella.</b></td><td>¿Por qué es tu mejor amigo?</td></tr></table>"""
 + h("최종 시험", f"¿Quién es tu mejor amigo? — 새로 만난 사람에게 대답하세요! ({fmt(T[iR])})")
 + '<p class="sm">플레이어에서 해당 문장부터 재생하고, 마테오가 대답하기 전에 먼저 내 친구로 말해 보세요.</p>'
 + ask(("Sofía", "¿Quién es tu mejor amigo?"), ("Sofía", "¿Cuántos años tiene?"), ("Sofía", "¿Dónde vive?"), ("Sofía", "¿Cómo es?"), ("Sofía", "¿Qué hacen juntos?"), ("Sofía", "¿Por qué es tu mejor amigo?"))
 + h("최종 미션", "나의 가장 친한 친구 소개 (Mi mejor amigo / Mi mejor amiga)")
 + """<table class="t mine"><tr><th>항목</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 이름</td><td><b>Hola. Mi mejor amigo/a se llama …</b></td><td></td></tr>
<tr><td>② 나이</td><td><b>Tiene … años.</b></td><td></td></tr>
<tr><td>③ 사는 곳</td><td><b>Vive en …</b></td><td></td></tr>
<tr><td>④ 성격 · 외모</td><td><b>Es muy … y … Es alto/a …</b></td><td></td></tr>
<tr><td>⑤ 함께 하는 일</td><td><b>Nos gusta … · Salimos a …</b></td><td></td></tr>
<tr><td>⑥ 이유 · 마무리</td><td><b>Es mi mejor amigo/a porque … Me gusta estar con él / ella.</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> Hola. Mi mejor amiga se llama Sujin. Tiene 34 años. Vive en Goyang. Es muy simpática y es muy divertida. También es inteligente. Nos gusta tomar café y salimos a caminar por el lago. Es mi mejor amiga porque me escucha y me ayuda siempre. Me gusta mucho estar con ella.</div>
<p class="sm">por el lago = 호숫가를 (일산 호수공원!) · 여자 친구면 <b>amiga · simpática · con ella</b>, 남자 친구면 <b>amigo · simpático · con él</b> · 팟캐스트의 마지막 말: <b>Ya puedes hablar de tu mejor amigo en español.</b></p>
""" + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>친구의 이름·나이·사는 곳을 se llama / tiene / vive로 말할 수 있다.</li><li>성격 형용사 3개 이상을 친구 성에 맞게 말할 수 있다.</li><li>alto / bajo / joven / mayor로 외모를 말할 수 있다.</li><li>hablamos · vemos · salimos · vamos a로 함께 하는 일을 말할 수 있다.</li><li>porque로 이유를 말할 수 있다. (me escucha, me ayuda)</li><li>마지막 도전(' + fmt(T[iR]) + ')에서 멈추지 않고 대답할 수 있다.</li></ul>'
 + "</section>")

# ---------- Appendix ----------
P.append("""<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: 1 amiga · 2 amigo · 3 amiga · 4 amigo &nbsp;|&nbsp; B: 1 Tiene 30 años. Vive en Valencia. · 2 se llama Ana. Tiene 25 años. Vive en Madrid. · 3 Mi mejor amigo se llama Luis. Tiene 40 años. Vive en Barcelona.</p>
<p><b>Lesson 2</b> A: 1 simpática · 2 divertido · 3 alta · 4 tranquilo y trabajador · 5 amable &nbsp;|&nbsp; B: ①ⓒ ②ⓐ ③ⓑ</p>
<p><b>Lesson 3</b> A: 1 Escuchamos · 2 Vemos · 3 Salimos · 4 Hablamos · 5 Vamos &nbsp;|&nbsp; B: 1 es muy simpática · 2 me escucha · 3 me ayuda mucho</p>
<p><b>Lesson 4</b> 아나 표: Ana · 25 años · Madrid · simpática, inteligente, divertida · escuchan música, ven películas<br>
후안: 1 Se llama Luis. · 2 Tiene 40 años. · 3 Vive en Barcelona. · 4 Es tranquilo, trabajador y bueno. · 5 Les gusta salir a caminar y cenar.<br>
응용: se llama · Tiene · Vive · simpática (inteligente, divertida) · les · Ven</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">이번 에피소드의 핵심 동사예요. 이번 주는 <b>él / ella</b>(친구)와 <b>nosotros</b>(우리) 줄을 꼭 외워요.</p>
<table class="t"><tr><th>주어</th><th>ser</th><th>tener</th><th>vivir</th><th>hablar</th><th>ver</th><th>salir</th><th>ir</th></tr>
<tr><td>yo</td><td>soy</td><td>tengo</td><td>vivo</td><td>hablo</td><td>veo</td><td>salgo</td><td>voy</td></tr>
<tr><td>tú</td><td>eres</td><td>tienes</td><td>vives</td><td>hablas</td><td>ves</td><td>sales</td><td>vas</td></tr>
<tr><td>él / ella / usted</td><td><b>es</b></td><td><b>tiene</b></td><td><b>vive</b></td><td>habla</td><td>ve</td><td>sale</td><td>va</td></tr>
<tr><td>nosotros/as</td><td>somos</td><td>tenemos</td><td>vivimos</td><td><b>hablamos</b></td><td><b>vemos</b></td><td><b>salimos</b></td><td><b>vamos</b></td></tr>
<tr><td>vosotros/as</td><td>sois</td><td>tenéis</td><td>vivís</td><td>habláis</td><td>veis</td><td>salís</td><td>vais</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>son</td><td>tienen</td><td>viven</td><td>hablan</td><td>ven</td><td>salen</td><td>van</td></tr></table>
<p class="sm">gustar: me gusta (나) · le gusta (그/그녀) · <b>nos gusta</b> (우리) · <b>les gusta</b> (그들)</p>
</section>""")

voc = ['<section class="lesson"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'단어장\' 탭과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 친구 교재 Ep7</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
