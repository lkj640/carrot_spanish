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
END = 22 * 60 - 6

def rng(a, b):
    return f"{fmt(sec_start(a))}–{fmt(sec_start(b)) if b else fmt(END)}"

def dlg(*prefixes, after=0):
    rows = []
    for p in prefixes:
        i = find(p, after)
        sp, es, ko = L[i]
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
P.append(f'''<section class="cover"><div class="stripe"></div>
<div class="ct"><h1>왕초보 스페인어<br>좋아하는 음식 말하기</h1>
<div class="cs">Easy Spanish Podcast Ep.6 · A1 입문</div>
<div class="big">¡Me encanta la pizza!</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · 명사의 성(el / la)</td></tr>
<tr><th>LESSON 1</th><td>좋아하는 음식 묻고 답하기 · ¿Cuál es tu comida favorita?</td></tr>
<tr><th>LESSON 2</th><td>좋아요 · 정말 좋아요 · 싫어요 (gustar / encantar)</td></tr>
<tr><th>LESSON 3</th><td>맛과 온도 묘사하기 (형용사의 성 일치)</td></tr>
<tr><th>LESSON 4</th><td>먹다 · 마시다 · 어디서 · 누구와 · 언제</td></tr>
<tr><th>LESSON 5</th><td>듣기: 카를로스와 아나 이야기</td></tr>
<tr><th>LESSON 6</th><td>인터뷰 · 단계별 발표 · 나의 음식 소개</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 10월 25일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>''')

# ---------- intro ----------
P.append('''<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 발음과 명사의 성</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. Ep.1에서 배운 <b>La repetición es mágica.</b> (반복은 마법이에요.)를 잊지 마세요!</div>
''' + h("발음", "이번 에피소드에 나오는 주의할 소리") + '''
<table class="t"><tr><th>글자</th><th>소리</th><th>예</th></tr>
<tr><td><b>ll</b></td><td>'y'처럼 — 야/요</td><td><b>pollo</b> 뽀요 (닭고기)</td></tr>
<tr><td><b>j</b></td><td>목에서 나는 강한 ㅎ</td><td><b>jugo</b> 후고 (주스)</td></tr>
<tr><td><b>rr</b> / 첫 r</td><td>길게 굴리는 r</td><td><b>arroz</b> 아로스 · <b>restaurante</b> 레스따우란떼</td></tr>
<tr><td><b>h</b></td><td>소리 없음</td><td><b>helado</b> 엘라도 · <b>hamburguesa</b> 암부르게사</td></tr>
<tr><td><b>gue</b></td><td>'게' (u는 읽지 않음)</td><td>hambur<b>gue</b>sa 암부르<b>게</b>사</td></tr>
<tr><td><b>qu</b></td><td>ㄲ (u는 읽지 않음)</td><td><b>queso</b> 께소 · <b>qué</b> 께</td></tr>
<tr><td><b>c + e, i</b> / <b>z</b></td><td>스페인: 영어 th / 중남미: ㅆ</td><td><b>cenar</b> 쎄나르 · <b>arroz</b> 아로스</td></tr>
<tr><td><b>ñ</b></td><td>냐·녜·뇨</td><td><b>mañana</b> 마냐나 · <b>año</b> 아뇨</td></tr>
</table>
<p class="sm">※ 한글 표기는 감을 잡기 위한 참고용이에요. 정확한 소리는 꼭 팟캐스트로 들어 보세요.</p>
''' + h("문법 0", "스페인어 명사에는 성별이 있어요 — el / la") + '''
<div class="two"><div class="box y"><b>남성 명사 → el</b>
<p><b>el</b> pollo · <b>el</b> arroz · <b>el</b> pescado · <b>el</b> café · <b>el</b> té · <b>el</b> queso · <b>el</b> chocolate · <b>el</b> helado · <b>el</b> plátano · <b>el</b> jugo</p>
<p class="sm">-o로 끝나면 대부분 남성</p></div>
<div class="box y"><b>여성 명사 → la</b>
<p><b>la</b> pasta · <b>la</b> pizza · <b>la</b> carne · <b>la</b> ensalada · <b>la</b> sopa · <b>la</b> hamburguesa · <b>la</b> fruta · <b>la</b> manzana · <b>la</b> comida · <b>la</b> bebida</p>
<p class="sm">-a로 끝나면 대부분 여성</p></div></div>
<div class="note r"><b>예외 주의!</b> <b>el agua</b> (물)는 여성 명사지만, 강세 있는 a-로 시작해서 발음 때문에 <b>el</b>을 써요. 형용사는 여성형: el agua fría.</div>
<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 질문하고 설명하는 선생님 역할 · 파스타를 사랑해요. · <b class="cM">Mateo</b> — 따라 말하기 시범을 보여 줘요. 피자 마니아, 생선과 커피는 싫어해요. · <b class="cT">Tú (나)</b> — 대화에 직접 대답하는 청취자!</p>
</section>''')

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 3), "좋아하는 음식 묻고 답하기", "팟캐스트 1. 오프닝 · 2. 좋아하는 음식 묻고 답하기",
    ["<b>¿Cuál es tu comida favorita?</b>라고 물을 수 있다.", "<b>Mi comida favorita es + el/la 음식</b>으로 대답할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Hoy hablamos de algo", "Mmm, me gusta la comida", "¿Y a ti, Sofía?", "Buena pregunta", "Ah, la pasta", "Mi comida favorita es la pizza.", "¡Pizza! Qué rico", "¡Qué bien! La pizza es una")
 + h("문법", "\"가장 좋아하는 ~\" 묻고 답하기")
 + '''<div class="two"><div class="box y"><b>묻기</b>
<p><b>¿Cuál es tu comida favorita?</b><br>꽐 에스 뚜 꼬미다 파보리따 — 가장 좋아하는 음식이 뭐예요?</p>
<p><b>¿Y a ti?</b> 너는? (되묻기)</p></div>
<div class="box y"><b>대답하기</b>
<p><b>Mi comida favorita es la pasta.</b><br>제가 가장 좋아하는 음식은 파스타예요.</p>
<p><b>Mi comida favorita es el pollo.</b><br>제가 가장 좋아하는 음식은 닭고기예요.</p></div></div>
<div class="note g"><b>favorito? favorita?</b> comida(음식)와 bebida(음료)가 <b>여성 명사</b>라서 <b>favorita</b>예요.
<br>mi = 나의 · tu = 너의 · su = 그(녀)의 &nbsp;→&nbsp; <b>Su comida favorita es la pasta.</b> 그의 가장 좋아하는 음식은 파스타예요.</div>
<div class="note y"><b>리액션 표현</b> ¡Qué rico! 맛있겠다! · ¡Qué bien! 좋네요! · Buena pregunta. 좋은 질문이에요. · Dime. 말해 봐. · Una excelente elección. 훌륭한 선택이에요.</div>'''
 + h("연습 A", "알맞은 관사 el / la를 쓰세요.")
 + '<div class="grid4">' + "".join(f'<div>{BS} {w}</div>' for w in ["pizza", "pollo", "arroz", "pasta", "sopa", "pescado", "carne", "helado"]) + "</div>"
 + h("연습 B", "그림을 보고 \"Mi comida favorita es …\" 문장을 완성하세요.")
 + blanks([f"🍝 → Mi comida favorita es {B}.", f"🍗 → Mi comida favorita es {B}.", f"🍚 → Mi comida favorita es {B}.", f"🥗 → Mi comida favorita es {B}."])
 + h("연습 C", "빈칸을 채워 대화를 완성하세요.")
 + blanks([f"A: ¿Cuál es {BS} comida favorita? — B: {BS} comida favorita es la pizza.", f"A: Mi comida favorita es la pasta. ¿Y a {BS}?", f"Carlos: Mi comida favorita es la pasta. → {BS} comida favorita es la pasta. (카를로스에 대해 말하기)"])
 + h("말하기", "소피아의 질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Cuál es tu comida favorita?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(3, 4), "좋아요 · 정말 좋아요 · 싫어요", "팟캐스트 3. Me gusta / Me encanta / No me gusta",
    ["<b>Me gusta / Me encanta / No me gusta</b>로 좋고 싫음을 말할 수 있다.", "<b>¿Te gusta …?</b>라고 묻고 <b>Sí, me gusta / No, no me gusta</b>로 대답할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Para decir que algo te gusta mucho", "Exacto. Y si te gusta muchísimo", "Muy bien. Si algo no te gusta", "Perfecto, Mateo. Vamos a practicar con más", "Sí, Sofía. Me gusta el arroz", "¿Y la ensalada?", "Mmm, no mucho", "Claro, la sopa caliente", "(risas) Sí. Me encanta")
 + h("문법", "gustar — \"~이 나에게 즐거움을 준다\"")
 + '''<div class="note g"><b>구조가 한국어·영어와 달라요</b>
<b>Me gusta la pizza.</b> = 피자가(주어) 나에게(me) 즐거움을 준다(gusta) → "나는 피자를 좋아해요"<br>
그래서 좋아하는 대상이 <b>복수</b>면 동사도 복수: <b>Me gustan las frutas.</b> (Ep.1의 <b>Me gustan las historias</b>와 같은 원리!)<br>
동사원형이 오면 항상 단수: <b>Me gusta comer pizza.</b></div>
<table class="t"><tr><th>누가 좋아해?</th><th>+ 단수 / 동사원형</th><th>+ 복수</th><th>예문</th></tr>
<tr><td>나 (a mí)</td><td><b>me gusta</b></td><td><b>me gustan</b></td><td>Me gusta el arroz.</td></tr>
<tr><td>너 (a ti)</td><td><b>te gusta</b></td><td><b>te gustan</b></td><td>¿Te gusta la carne?</td></tr>
<tr><td>그 / 그녀 (a él / a ella)</td><td><b>le gusta</b></td><td><b>le gustan</b></td><td>¿Le gusta el pescado a Carlos?</td></tr></table>
''' + h("표현", "좋아하는 정도 온도계") + '''
<table class="t scale"><tr><td>😍</td><td><b>Me encanta la pizza.</b></td><td>피자를 정말 좋아해요. (최고!)</td></tr>
<tr><td>😄</td><td><b>Me gusta mucho el pollo.</b></td><td>닭고기를 아주 좋아해요.</td></tr>
<tr><td>🙂</td><td><b>Me gusta el arroz.</b></td><td>밥을 좋아해요.</td></tr>
<tr><td>😐</td><td><b>No me gusta mucho cocinar.</b> / <b>No mucho.</b></td><td>요리하는 건 별로예요. / 별로요.</td></tr>
<tr><td>🙁</td><td><b>No me gusta el pescado.</b></td><td>생선을 좋아하지 않아요.</td></tr></table>
<div class="note r"><b>자주 하는 실수</b> ✗ Me encanta mucho la pizza. → encantar는 이미 "정말 좋아하다"라서 mucho를 붙이지 않아요. ✓ <b>Me encanta la pizza.</b> / ✓ <b>Me gusta mucho la pizza.</b></div>'''
 + h("연습 A", "얼굴을 보고 문장을 완성하세요.")
 + blanks([f"😍 + la hamburguesa → {B}", f"🙁 + la ensalada → {B}", f"🙂 + la sopa → {B}", f"😄 + la carne → {B}"])
 + h("연습 B", "gusta / gustan 중 알맞은 것을 고르세요.")
 + blanks(["Me (gusta / gustan) la fruta.", "Me (gusta / gustan) las manzanas.", "¿Te (gusta / gustan) cocinar?", "A Ana le (gusta / gustan) el plátano."])
 + h("연습 C", "질문에 마테오가 되어 대답하세요.")
 + blanks([f"¿Te gusta la ensalada? → No, {B}.", f"¿Te gusta la sopa? → Sí, {B}.", f"¿Te encanta la pizza? → Sí, {B}."])
 + h("말하기", "소피아의 질문에 내 입장으로 대답하세요")
 + ask(("Sofía", "¿Te gusta el arroz?"), ("Sofía", "¿Te gusta la carne?"), ("Sofía", "¿Te gusta el pescado?"), ("Sofía", "¿Te gusta la hamburguesa?"))
 + "</section>")

# ---------- Lesson 3 ----------
P.append(lesson(3, rng(4, 5), "맛과 온도 묘사하기", "팟캐스트 4. 음식 묘사하기",
    ["<b>rico, delicioso, dulce, salado, caliente, frío</b>로 음식을 묘사할 수 있다.", "명사의 성에 맞게 형용사 끝을 바꿀 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Podemos decir si algo es rico", "Muy bien. O también", "Perfecto. También podemos decir", "Exacto. Y «El queso", "Genial. Y para la temperatura", "Muy bien. O «El helado", "¿Es dulce o salada?", "Mmm, la pizza es salada")
 + h("문법", "형용사는 명사의 성에 맞춰요")
 + '''<table class="t"><tr><th>형용사</th><th>남성 (el …)</th><th>여성 (la …)</th><th>뜻</th></tr>
<tr><td>-o → -a</td><td>El pollo es <b>rico</b>.</td><td>La pizza es <b>rica</b>.</td><td>맛있는</td></tr>
<tr><td></td><td>El pescado es <b>delicioso</b>.</td><td>La pasta es <b>deliciosa</b>.</td><td>아주 맛있는</td></tr>
<tr><td></td><td>El queso es <b>salado</b>.</td><td>La pizza es <b>salada</b>.</td><td>짠</td></tr>
<tr><td></td><td>El helado es <b>frío</b>.</td><td>La ensalada es <b>fría</b>.</td><td>차가운</td></tr>
<tr><td>-e (형태 같음)</td><td>El chocolate es <b>dulce</b>.</td><td>La manzana es <b>dulce</b>.</td><td>단</td></tr>
<tr><td></td><td>El café es <b>caliente</b>.</td><td>La sopa es <b>caliente</b>.</td><td>뜨거운</td></tr></table>
<div class="note g"><b>ser + 형용사</b> 음식의 성질은 <b>ser</b>로 말해요: <b>La pizza es rica.</b> · 지금 먹어 보니 맛있다고 할 땐 <b>estar</b>도 써요: <b>¿Está rica la pizza?</b> (복습 파트 '''+fmt(T[find('¿Está rica')])+'''에 등장)
<br><b>muy</b> = 아주 → La pizza es <b>muy</b> rica. · 이유 말하기: <b>Me gusta porque es muy rica.</b> (아주 맛있어서 좋아요)</div>
''' + h("단어", "더 알아 두면 좋은 형용사") + '''
<table class="t"><tr><td><b>fresco/a</b></td><td>신선한 — la ensalada fresca</td><td><b>saludable</b></td><td>건강에 좋은 — La ensalada es muy saludable.</td></tr>
<tr><td><b>refrescante</b></td><td>상쾌한 — ¡Qué refrescante!</td><td><b>picante</b> +보너스</td><td>매운 — El kimchi es picante.</td></tr></table>'''
 + h("연습 A", "형용사를 알맞은 형태로 바꾸세요.")
 + blanks([f"La sopa es (delicioso) → {B}", f"El helado es (frío) → {B}", f"La pizza es (salado) → {B}", f"El chocolate es (dulce) → {B}", f"La ensalada es (fresco) → {B}"])
 + h("연습 B", "반대말끼리 연결하세요.")
 + '<table class="t match"><tr><td>① dulce</td><td>ⓐ frío</td></tr><tr><td>② caliente</td><td>ⓑ salado</td></tr><tr><td>③ Me gusta</td><td>ⓒ No me gusta</td></tr></table>'
 + h("말하기", "내가 좋아하는 음식을 묘사해 보세요")
 + ask(("Sofía", "Tu comida favorita es …, ¿verdad? ¿Es rica?"), ("Sofía", "¿Es dulce o salada?"))
 + "</section>")

# ---------- Lesson 4 ----------
P.append(lesson(4, rng(5, 8), "먹다 · 마시다 · 어디서 · 누구와 · 언제", "팟캐스트 5. 먹는 것 말하기 · 6. 좋아하는 음료 · 7. 어디서 누구와",
    ["<b>Me gusta comer …</b>로 먹기 좋아하는 것을 말할 수 있다.", "<b>¿Cuál es tu bebida favorita?</b>에 대답할 수 있다.", "<b>como / bebo / ceno</b>로 언제·어디서·누구와 먹는지 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Exactamente. Muy bien. Ahora vamos a hablar de lo que", "Me gusta comer pizza. También", "¡Qué bien! ¿Comes pizza", "Sí. Como pizza una vez", "¡Excelente! ¿Cuál es tu bebida favorita, Mateo?", "Mi bebida favorita es el jugo", "No. No me gusta el café", "Sí. Bebo agua todos", "Podemos decir: «Como pizza en casa»", "Muy bien. También: «Ceno", "¿Comes con tu familia?")
 + h("문법", "-er 동사 comer / beber, -ar 동사 cenar")
 + '''<table class="t"><tr><th>주어</th><th>comer (먹다)</th><th>beber (마시다)</th><th>cenar (저녁 먹다)</th></tr>
<tr><td>yo</td><td><b>como</b></td><td><b>bebo</b></td><td><b>ceno</b></td></tr>
<tr><td>tú</td><td><b>comes</b></td><td><b>bebes</b></td><td><b>cenas</b></td></tr>
<tr><td>él / ella</td><td><b>come</b></td><td><b>bebe</b></td><td><b>cena</b></td></tr>
<tr><td>nosotros/as</td><td><b>comemos</b></td><td><b>bebemos</b></td><td><b>cenamos</b></td></tr>
<tr><td>ellos / ellas</td><td><b>comen</b></td><td><b>beben</b></td><td><b>cenan</b></td></tr></table>
<div class="two"><div class="box y"><b>Me gusta + 동사원형</b>
<p><b>Me gusta comer</b> pizza. 피자 먹는 걸 좋아해요.<br><b>Me gusta beber</b> jugo de naranja. 오렌지 주스 마시는 걸 좋아해요.<br><b>No me gusta mucho cocinar.</b> 요리하는 건 별로예요.</p></div>
<div class="box y"><b>어디서 · 누구와 · 언제</b>
<p><b>en casa</b> 집에서 · <b>en un restaurante</b> 식당에서<br><b>con mi familia</b> 가족과 · <b>con mis amigos</b> 친구들과<br><b>los sábados</b> 토요일마다 · <b>los viernes</b> 금요일마다<br><b>una vez a la semana</b> 일주일에 한 번 · <b>todos los días</b> 매일 · <b>a menudo</b> 자주 · <b>normalmente</b> 보통</p></div></div>
''' + h("단어", "음료 (Las bebidas)") + '''
<div class="grid5"><div>☕ <b>el café</b><br>커피</div><div>💧 <b>el agua</b><br>물</div><div>🍊 <b>el jugo de naranja</b><br>오렌지 주스</div><div>🍵 <b>el té</b><br>차</div><div>🥛 <b>la leche</b> +보너스<br>우유</div></div>
<p class="sm">jugo는 중남미, 스페인에서는 <b>zumo</b>라고 해요. (zumo de naranja)</p>'''
 + h("연습 A", "동사를 알맞게 바꾸세요.")
 + blanks([f"Yo (comer) {BS} pizza en casa.", f"¿Tú (beber) {BS} agua todos los días?", f"Carlos (comer) {BS} pasta con sus amigos.", f"Nosotros (comer) {BS} pizza los viernes.", f"Yo (cenar) {BS} en un restaurante."])
 + h("연습 B", "그림을 보고 문장을 완성하세요. (주어: 나)")
 + blanks([f"🏠🍕 → Como pizza {B}.", f"👨‍👩‍👧🍚 → Como {B}.", f"💧 매일 → Bebo agua {B}.", f"☕✗ → {B} el café."])
 + h("말하기", "소피아의 질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Qué te gusta comer?"), ("Sofía", "¿Cuál es tu bebida favorita?"), ("Sofía", "¿Comes tu comida favorita en casa?"), ("Sofía", "¿Comes con tu familia?"))
 + "</section>")

# ---------- Lesson 5 ----------
iC = find("Se trata de Carlos")
iA = find("Esta es Ana.")
P.append(lesson(5, rng(8, 10), "듣기: 카를로스와 아나 이야기", "팟캐스트 8. 카를로스 이야기 · 9. 아나 이야기",
    ["짧은 이야기를 듣고 좋아하는 음식·음료·장소·사람을 파악할 수 있다.", "<b>Su … es … / Le gusta …</b>로 다른 사람에 대해 말할 수 있다."])
 + h("듣기 ①", f"La historia de Carlos — 카를로스 이야기 ({fmt(T[iC])})")
 + '<div class="story">Hola, me llamo Carlos. Mi comida favorita es la pasta. Me gusta mucho la pasta. También me gusta el pollo. No me gusta el pescado. Mi bebida favorita es el té. Me gusta comer pasta con mis amigos. Comemos pasta los sábados. La pasta es muy rica. Me encanta la pasta.</div>'
 + h("이해 확인", "질문에 스페인어로 답하세요.")
 + blanks([f"¿Cuál es la comida favorita de Carlos? {B}", f"¿Le gusta el pescado a Carlos? {B}", f"¿Cuál es su bebida favorita? {B}", f"¿Con quién come pasta Carlos? {B}", f"¿Cuándo comen pasta? {B}"])
 + h("듣기 ②", f"Ana — 아나 이야기 ({fmt(T[iA])})")
 + '<div class="story">Hola. Yo soy Ana. Mi comida favorita es la ensalada. Me gusta mucho la ensalada fresca. También me gusta la fruta, como la manzana y el plátano. No me gusta la carne. Mi bebida favorita es el agua. Bebo mucha agua. Me gusta comer ensalada en casa. La ensalada es muy saludable.</div>'
 + '<div class="note g"><b>Ep.1의 아나 기억나요?</b> Ep.1에서 아나는 멕시코 출신의 스무 살 학생이었어요. 이번엔 아나가 좋아하는 음식을 알게 됐네요!</div>'
 + h("이해 확인", "아나에 대한 표를 채우세요.")
 + '<table class="t fill"><tr><th>가장 좋아하는 음식</th><th>좋아하는 과일</th><th>싫어하는 것</th><th>좋아하는 음료</th><th>어디서 먹나?</th></tr><tr><td></td><td></td><td></td><td></td><td></td></tr></table>'
 + h("문법", "나 → 그/그녀로 바꾸기")
 + '''<table class="t"><tr><th>본인이 말할 때 (yo)</th><th>남이 말할 때 (él / ella)</th></tr>
<tr><td><b>Mi</b> comida favorita es la pasta.</td><td><b>Su</b> comida favorita es la pasta.</td></tr>
<tr><td><b>Me</b> gusta el pollo.</td><td><b>Le</b> gusta el pollo.</td></tr>
<tr><td>No <b>me</b> gusta el pescado.</td><td>No <b>le</b> gusta el pescado.</td></tr>
<tr><td><b>Como</b> con <b>mis</b> amigos.</td><td><b>Come</b> con <b>sus</b> amigos.</td></tr>
<tr><td><b>Bebo</b> mucha agua.</td><td><b>Bebe</b> mucha agua.</td></tr></table>'''
 + h("응용", "아나 이야기를 3인칭으로 바꿔 쓰세요.")
 + f'<p class="fillp">Esta es Ana. {BS} comida favorita es la ensalada. {BS} gusta la fruta, como la manzana y el plátano. No {BS} gusta la carne. {BS} bebida favorita es el agua. {BS} mucha agua.</p>'
 + "</section>")

# ---------- Lesson 6 ----------
iR = find("¡Genial, Mateo! Lo tienes")
P.append(lesson(6, rng(10, None), "인터뷰 · 단계별 발표 · 나의 음식 소개", "팟캐스트 10. 내 차례 · 11. 단계별 발표 · 12. 완성 예시 · 13. 복습 · 14. 마지막 도전",
    ["지금까지 배운 표현으로 <b>음식 인터뷰</b>에 대답할 수 있다.", "좋아하는 음식에 대해 <b>8문장 발표</b>를 할 수 있다."])
 + h("단계별", "Paso a paso — 발표 만들기 6단계")
 + '''<table class="t"><tr><th>단계</th><th>패턴</th><th>마테오의 문장</th></tr>
<tr><td>① 좋아하는 음식</td><td><b>Mi comida favorita es …</b></td><td>Mi comida favorita es la pizza.</td></tr>
<tr><td>② 정도</td><td><b>Me gusta mucho …</b></td><td>Me gusta mucho la pizza.</td></tr>
<tr><td>③ 그 밖에</td><td><b>También me gusta …</b></td><td>También me gusta el pollo y la fruta.</td></tr>
<tr><td>④ 싫어하는 것</td><td><b>No me gusta …</b></td><td>No me gusta el pescado.</td></tr>
<tr><td>⑤ 음료</td><td><b>Mi bebida favorita es …</b></td><td>Mi bebida favorita es el jugo de naranja.</td></tr>
<tr><td>⑥ 어디서·누구와·언제</td><td><b>Me gusta comer … con … en …</b></td><td>Me gusta comer pizza con mi familia en casa. Comemos pizza los viernes.</td></tr>
<tr><td>⑦ 마무리 감정</td><td><b>Me encanta …</b></td><td>Me encanta la pizza.</td></tr></table>'''
 + h("예시", "소피아의 완성된 발표 (Una presentación completa)")
 + '<div class="story">Hola. Mi comida favorita es la pasta. Me gusta mucho. También me gusta el pollo. No me gusta el pescado. Mi bebida favorita es el té. Me gusta comer pasta con mis amigos los sábados. La pasta es muy rica. Me encanta la pasta.</div>'
 + h("최종 시험", f"El último reto — 새로 만난 사람에게 대답하세요! ({fmt(T[iR])})")
 + '<p class="sm">플레이어에서 해당 문장부터 재생하고, 소피아가 질문한 뒤 마테오가 대답하기 전에 먼저 말해 보세요. 아래에 먼저 써 두면 쉬워요.</p>'
 + ask(("Sofía", "¿Cuál es tu comida favorita?"), ("Sofía", "¿Por qué te gusta?"), ("Sofía", "¿Qué más te gusta comer?"), ("Sofía", "¿Qué no te gusta?"), ("Sofía", "¿Cuál es tu bebida favorita?"), ("Sofía", "¿Con quién comes?"), ("Sofía", "¿Cuándo comes tu comida favorita?"))
 + h("최종 미션", "나의 음식 소개 (Mi comida favorita)")
 + '''<table class="t mine"><tr><th>항목</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 인사 · 음식</td><td><b>Hola. Mi comida favorita es …</b></td><td></td></tr>
<tr><td>② 정도</td><td><b>Me gusta mucho … / Me encanta …</b></td><td></td></tr>
<tr><td>③ 그 밖에</td><td><b>También me gusta …</b></td><td></td></tr>
<tr><td>④ 싫어하는 것</td><td><b>No me gusta …</b></td><td></td></tr>
<tr><td>⑤ 음료</td><td><b>Mi bebida favorita es …</b></td><td></td></tr>
<tr><td>⑥ 누구와·어디서·언제</td><td><b>Como … con … en … los …</b></td><td></td></tr>
<tr><td>⑦ 묘사 · 마무리</td><td><b>… es muy rico/a. ¡Me encanta!</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> Hola. Mi comida favorita es el kimchi jjigae. Me encanta. También me gusta el arroz y la fruta. No me gusta el pescado. Mi bebida favorita es el café. Como kimchi jjigae con mi familia en casa los domingos. Es muy rico y picante. ¡Me encanta!</div>
<p class="sm">한국 음식 이름은 그대로 써도 돼요: el bibimbap, el kimchi, el bulgogi, el tteokbokki … (los domingos = 일요일마다)</p>
''' + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>가장 좋아하는 음식·음료를 묻고 대답할 수 있다.</li><li>Me encanta / Me gusta mucho / No me gusta로 좋고 싫음의 정도를 말할 수 있다.</li><li>el / la를 구분하고 형용사를 성에 맞게 바꿀 수 있다. (rico / rica)</li><li>como, bebo, ceno로 어디서·누구와·언제 먹는지 말할 수 있다.</li><li>짧은 이야기를 듣고 Su … / Le gusta …로 다른 사람에 대해 말할 수 있다.</li><li>마지막 도전 대화(' + fmt(T[iR]) + ')에 멈추지 않고 대답할 수 있다.</li></ul>'
 + '<p class="sm">팟캐스트의 마지막 말: <b>Ya puedes hablar de tu comida favorita en español. ¡Felicidades!</b> — 이제 스페인어로 좋아하는 음식에 대해 말할 수 있어요. 축하해요!</p>'
 + "</section>")

# ---------- Appendix ----------
P.append('''<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: la pizza · el pollo · el arroz · la pasta · la sopa · el pescado · la carne · el helado &nbsp;|&nbsp; B: 1 la pasta · 2 el pollo · 3 el arroz · 4 la ensalada &nbsp;|&nbsp; C: 1 tu / Mi · 2 ti · 3 Su</p>
<p><b>Lesson 2</b> A: 1 Me encanta la hamburguesa. · 2 No me gusta la ensalada. · 3 Me gusta la sopa. · 4 Me gusta mucho la carne. &nbsp;|&nbsp; B: 1 gusta · 2 gustan · 3 gusta · 4 gusta &nbsp;|&nbsp; C: 1 no me gusta (la ensalada) · 2 me gusta (la sopa) · 3 me encanta (la pizza)</p>
<p><b>Lesson 3</b> A: 1 deliciosa · 2 frío · 3 salada · 4 dulce · 5 fresca &nbsp;|&nbsp; B: ①ⓑ ②ⓐ ③ⓒ</p>
<p><b>Lesson 4</b> A: 1 como · 2 bebes · 3 come · 4 comemos · 5 ceno &nbsp;|&nbsp; B: 1 en casa · 2 con mi familia · 3 todos los días · 4 No me gusta</p>
<p><b>Lesson 5</b> 카를로스: 1 Su comida favorita es la pasta. · 2 No, no le gusta el pescado. · 3 Su bebida favorita es el té. · 4 Come pasta con sus amigos. · 5 Comen pasta los sábados.<br>
아나 표: la ensalada · la manzana y el plátano · la carne · el agua · en casa<br>
응용: Su · Le · le · Su · Bebe</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">이번 에피소드의 핵심 동사예요. 우선 yo / tú / él·ella 세 줄만 외워도 충분해요.</p>
<table class="t"><tr><th>주어</th><th>gustar (좋아하다)<br><span class="sm">+ 단수 / + 복수</span></th><th>encantar (정말 좋아하다)</th><th>comer (먹다)</th><th>beber (마시다)</th><th>cenar (저녁 먹다)</th></tr>
<tr><td>yo</td><td>me gusta / me gustan</td><td>me encanta(n)</td><td>como</td><td>bebo</td><td>ceno</td></tr>
<tr><td>tú</td><td>te gusta / te gustan</td><td>te encanta(n)</td><td>comes</td><td>bebes</td><td>cenas</td></tr>
<tr><td>él / ella / usted</td><td>le gusta / le gustan</td><td>le encanta(n)</td><td>come</td><td>bebe</td><td>cena</td></tr>
<tr><td>nosotros/as</td><td>nos gusta / nos gustan</td><td>nos encanta(n)</td><td>comemos</td><td>bebemos</td><td>cenamos</td></tr>
<tr><td>vosotros/as</td><td>os gusta / os gustan</td><td>os encanta(n)</td><td>coméis</td><td>bebéis</td><td>cenáis</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>les gusta / les gustan</td><td>les encanta(n)</td><td>comen</td><td>beben</td><td>cenan</td></tr></table>
<p class="sm">Ep.1에서 배운 <b>ser</b>도 계속 나와요: La pizza <b>es</b> rica. · Mi comida favorita <b>es</b> la pasta.</p>
</section>''')

voc = ['<section class="lesson"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'주요 어휘 정리\'를 주제별로 정리했어요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 음식 교재 Ep6</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
