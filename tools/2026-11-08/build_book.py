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
END = 13 * 60 + 2

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
<div class="ct"><h1>왕초보 스페인어<br>나에 대해 말하기</h1>
<div class="cs">Easy Spanish Podcast Ep.18 · A1 입문 · 4주차</div>
<div class="big">¿Quién eres? — Me llamo…</div>
<table class="toc">
<tr><th>시작</th><td>발음 포인트 · 의문사 7개 한눈에 보기</td></tr>
<tr><th>LESSON 1</th><td>이름과 나이 · Me llamo / Tengo … años</td></tr>
<tr><th>LESSON 2</th><td>출신과 사는 곳 · Soy de / Vivo en</td></tr>
<tr><th>LESSON 3</th><td>일 · 공부 · 언어 (-ar 동사 trabajar / estudiar / hablar)</td></tr>
<tr><th>LESSON 4</th><td>형제자매와 취미 · Tengo un hermano / Me gusta leer</td></tr>
<tr><th>LESSON 5</th><td>좋아하는 음식과 성격 · Soy tranquilo/a</td></tr>
<tr><th>LESSON 6</th><td>새로운 사람에게 자기소개 · 기억력 퀴즈 · 마지막 도전</td></tr>
<tr><th>부록</th><td>정답 · 동사표 · 단어장 한눈에 보기</td></tr>
</table>
<div class="foot">함께 듣기: lkj640.github.io/carrot_spanish → 11월 8일 모임 (문장을 누르면 그 부분부터 재생, 한국어 번역 보기 지원)<br>
각 레슨 구성: 오늘의 목표 → 팟캐스트 대화 → 핵심 문법 → 단어 → 연습 문제 → 말하기</div></div>
<div class="stripe"></div></section>''')

# ---------- intro ----------
P.append('''<section class="lesson"><div class="hd"><div class="k">EMPEZAMOS</div><h1>시작하기 전에: 발음과 의문사</h1></div>
<div class="note g"><b>이 교재로 공부하는 방법</b>① 레슨의 대화를 먼저 읽고 → ② 플레이어에서 해당 문장을 눌러 듣고 → ③ <b>"현재 문장 반복"</b> 기능으로 따라 말하고 → ④ 연습 문제를 풀어요. 이번 에피소드는 소피아와 마테오가 <b>¿Y tú?</b>(여러분은요?)라고 자주 물어봐요. 그때마다 영상을 멈추고 내 대답을 소리 내어 말해 보세요!</div>
''' + h("발음", "이번 에피소드에 나오는 주의할 소리") + '''
<table class="t"><tr><th>글자</th><th>소리</th><th>예</th></tr>
<tr><td><b>h</b></td><td>소리 없음</td><td><b>hablo</b> 아블로 · <b>hermano</b> 에르마노 · <b>hijo</b> 이호</td></tr>
<tr><td><b>j</b></td><td>목에서 나는 강한 ㅎ</td><td><b>joven</b> 호벤 · <b>hijo</b> 이호 · <b>trabajo</b> 뜨라바호</td></tr>
<tr><td><b>ñ</b></td><td>냐·녜·뇨</td><td><b>España</b> 에스빠냐 · <b>años</b> 아뇨스 · <b>diseño</b> 디세뇨</td></tr>
<tr><td><b>v</b> = <b>b</b></td><td>둘 다 'ㅂ'에 가까워요</td><td><b>vivo</b> 비보 · <b>vives</b> 비베스</td></tr>
<tr><td><b>qu</b></td><td>ㄲ (u는 읽지 않음)</td><td><b>¿qué?</b> 께 · <b>tranquilo</b> 뜨랑낄로</td></tr>
<tr><td><b>c + e, i</b> / <b>z</b></td><td>스페인: 영어 th / 중남미: ㅆ</td><td><b>ciudad</b> 씨우닫 · <b>cinco</b> 씽꼬 · <b>sociable</b> 소씨아블레</td></tr>
<tr><td><b>ll</b></td><td>'y'처럼 — 야/요</td><td><b>me llamo</b> 메 야모 · <b>¿Cómo te llamas?</b> 꼬모 떼 야마스</td></tr>
<tr><td><b>r</b> / <b>rr</b></td><td>혀를 한 번 / 여러 번 굴림</td><td><b>librería</b> 리브레리아 · <b>reto</b> 레또(첫 r은 길게)</td></tr>
</table>
<p class="sm">※ 한글 표기는 감을 잡기 위한 참고용이에요. 정확한 소리는 꼭 팟캐스트로 들어 보세요.</p>
''' + h("문법 0", "의문사 7개 — 자기소개 질문은 이걸로 다 만들어요") + '''
<table class="t"><tr><th>의문사</th><th>뜻</th><th>이번 에피소드의 질문</th></tr>
<tr><td><b>¿Quién?</b></td><td>누구</td><td>¿Quién eres? 당신은 누구예요?</td></tr>
<tr><td><b>¿Cómo?</b></td><td>어떻게, 어떤</td><td>¿Cómo te llamas? 이름이 뭐예요? · ¿Cómo eres? 어떤 사람이에요?</td></tr>
<tr><td><b>¿Cuántos / Cuántas?</b></td><td>몇 개, 얼마나 많이</td><td>¿Cuántos años tienes? 몇 살이에요?</td></tr>
<tr><td><b>¿De dónde?</b></td><td>어디에서(출신)</td><td>¿De dónde eres? 어디 출신이에요?</td></tr>
<tr><td><b>¿Dónde?</b></td><td>어디에</td><td>¿Dónde vives? 어디 살아요?</td></tr>
<tr><td><b>¿Qué?</b></td><td>무엇</td><td>¿Qué idiomas hablas? · ¿Qué te gusta hacer?</td></tr>
<tr><td><b>¿Cuál / Cuáles?</b></td><td>어느 것, 무엇 (정해진 것 중에서)</td><td>¿Cuál es tu comida favorita? · ¿Cuáles son tus pasatiempos?</td></tr>
</table>
<div class="note r"><b>의문사에는 항상 강세 부호!</b> qué, cómo, dónde, cuál, quién, cuántos — 질문할 때는 늘 강세(´)가 붙어요. 그리고 스페인어는 물음표를 앞뒤에 써요: <b>¿</b>…<b>?</b></div>
<h2><span class="tag">등장인물</span></h2>
<p><b class="cS">Sofía</b> — 28살, 스페인 출신, 마드리드의 서점에서 일해요. 책 읽기를 좋아하는 차분하고 밝은 사람. · <b class="cM">Mateo</b> — 25살, 멕시코 출신, 마드리드에서 그래픽 디자인을 공부해요. 축구·영화·요리, 그리고 먹는 걸 좋아하는 사교적인 외동. · <b class="cT">Tú (나)</b> — ¿Y tú?에 대답하는 청취자!</p>
</section>''')

# ---------- Lesson 1 ----------
P.append(lesson(1, rng(1, 3), "이름과 나이 말하기", "팟캐스트 1. 오프닝 · 2. 나이",
    ["<b>¿Quién eres? / ¿Cómo te llamas?</b>에 <b>Me llamo …</b>로 대답할 수 있다.", "<b>¿Cuántos años tienes?</b>에 <b>Tengo … años</b>로 대답할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Sofía, tengo una pregunta", "Dime, Mateo", "Es una pregunta muy fácil", "Bueno, me llamo Sofía", "¿Cuántos años tienes, Sofía?", "Tengo 28 años", "¿28? Mmm", "Yo tengo 25 años", "¡Ah! Mmm, ¿25?")
 + h("문법", "나이는 tener(가지다)로 말해요")
 + '''<div class="two"><div class="box y"><b>이름</b>
<p><b>Me llamo Sofía.</b> 제 이름은 소피아예요.<br><b>Soy Mateo.</b> 저는 마테오예요. (Ep.1 복습)<br><b>¿Cómo te llamas?</b> 이름이 뭐예요?</p></div>
<div class="box y"><b>나이 = 몇 해를 "가지고" 있다</b>
<p><b>Tengo 28 años.</b> 저는 28살이에요.<br><b>¿Cuántos años tienes?</b> 몇 살이에요?<br>✗ <s>Soy 28 años.</s> → 나이에는 ser가 아니라 <b>tener</b>!</p></div></div>
<table class="t"><tr><th>tener (가지다)</th><th>yo</th><th>tú</th><th>él / ella</th></tr>
<tr><td>현재형</td><td><b>tengo</b></td><td><b>tienes</b></td><td><b>tiene</b></td></tr></table>
<div class="note g"><b>비교하기</b> <b>más joven que yo</b> = 나보다 더 젊은(어린) · Mateo es <b>más joven que</b> Sofía. 마테오는 소피아보다 어려요.
<br><b>ño</b>에 주의: <b>años</b>(나이, 해) ≠ anos. 물결(~)을 꼭 써요!</div>
''' + h("숫자", "20–30 (Ep.1 숫자 복습)") + '''
<div class="grid5"><div><b>20</b> veinte</div><div><b>21</b> veintiuno</div><div><b>22</b> veintidós</div><div><b>23</b> veintitrés</div><div><b>24</b> veinticuatro</div>
<div><b>25</b> veinticinco</div><div><b>26</b> veintiséis</div><div><b>27</b> veintisiete</div><div><b>28</b> veintiocho</div><div><b>30</b> treinta</div></div>
<p class="sm">31부터는 <b>treinta y uno</b>, 42는 <b>cuarenta y dos</b>처럼 y로 이어요. 40 cuarenta · 50 cincuenta · 60 sesenta</p>'''
 + h("연습 A", "숫자를 스페인어로 쓰고 문장을 완성하세요.")
 + blanks([f"🎂 25 → Tengo {B} años.", f"🎂 28 → Sofía tiene {B} años.", f"🎂 30 → Mi hermano tiene {B} años.", f"🎂 나이 → Yo tengo {B} años."])
 + h("연습 B", "알맞은 말을 고르세요.")
 + blanks(["(Soy / Tengo) 25 años.", "¿Cuántos años (tienes / tiene), Mateo?", "Me (llamo / llamas) Sofía.", "¿Cómo te (llamo / llamas)?"])
 + h("말하기", "마테오의 질문에 소리 내어 답하세요")
 + ask(("Mateo", "¿Quién eres? Cuéntame."), ("Mateo", "¿Cuántos años tienes?"))
 + "</section>")

# ---------- Lesson 2 ----------
P.append(lesson(2, rng(3, 5), "출신과 사는 곳 말하기", "팟캐스트 3. 출신 · 4. 사는 곳",
    ["<b>¿De dónde eres? — Soy de …</b>로 출신을 말할 수 있다.", "<b>¿Dónde vives? — Vivo en …</b>으로 사는 곳을 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Sofía, ¿de dónde eres?", "Soy de España.", "¿De España? Es un país", "Sí. Me encanta España", "Por ejemplo: «Soy de México»", "Sofía, ¿dónde vives?", "Vivo en Madrid", "En Madrid. The capital", "Sí, me gusta mucho vivir")
 + h("문법", "ser de (출신) vs vivir en (사는 곳)")
 + '''<div class="two"><div class="box y"><b>출신 = ser + de</b>
<p><b>Soy de</b> Corea. 저는 한국 출신이에요.<br><b>¿De dónde eres?</b> 어디 출신이에요?<br>Sofía <b>es de</b> España. · Mateo <b>es de</b> México.</p></div>
<div class="box y"><b>사는 곳 = vivir + en</b>
<p><b>Vivo en</b> Goyang. 저는 고양에 살아요.<br><b>¿Dónde vives?</b> 어디 살아요?<br>Sofía y Mateo <b>viven en</b> Madrid.</p></div></div>
<table class="t"><tr><th>vivir (살다, -ir 동사)</th><th>yo</th><th>tú</th><th>él / ella</th><th>nosotros</th><th>ellos</th></tr>
<tr><td>현재형</td><td><b>vivo</b></td><td><b>vives</b></td><td><b>vive</b></td><td><b>vivimos</b></td><td><b>viven</b></td></tr></table>
<div class="note g"><b>출신과 사는 곳은 다를 수 있어요</b> 마테오는 <b>Soy de México</b>(멕시코 출신)이지만 <b>Vivo en Madrid</b>(마드리드에 살아요). 나도: <b>Soy de Busan, pero vivo en Ilsan.</b> 부산 출신이지만 일산에 살아요.
<br><b>me gusta + 동사원형</b>: Me gusta mucho <b>vivir</b> en Madrid. 마드리드에 사는 게 아주 좋아요.</div>
''' + h("단어", "나라 · 도시") + '''
<table class="t"><tr><td><b>Corea (del Sur)</b></td><td>한국</td><td><b>Seúl</b></td><td>서울</td></tr>
<tr><td><b>España</b></td><td>스페인</td><td><b>Madrid</b></td><td>마드리드 (la capital 수도)</td></tr>
<tr><td><b>México</b></td><td>멕시코 (x는 ㅎ 소리: 메히꼬)</td><td><b>Colombia</b></td><td>콜롬비아</td></tr>
<tr><td><b>el país</b></td><td>나라</td><td><b>la ciudad</b></td><td>도시 · otra ciudad 다른 도시</td></tr></table>'''
 + h("연습 A", "ser de / vivir en을 알맞게 바꾸세요.")
 + blanks([f"Yo {BS} de Corea. (ser)", f"Sofía {BS} en Madrid. (vivir)", f"¿Tú {BS} en Seúl? (vivir)", f"Mateo {BS} de México. (ser)", f"Nosotros {BS} en Ilsan. (vivir)"])
 + h("연습 B", "등장인물 카드를 보고 문장을 쓰세요.")
 + blanks([f"Sofía · 🇪🇸 · Madrid → Sofía es {B} y vive {B}.", f"Mateo · 🇲🇽 · Madrid → {B}.", f"나 → {B}."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Mateo", "¿De dónde eres?"), ("Mateo", "¿Dónde vives?"))
 + "</section>")

# ---------- Lesson 3 ----------
P.append(lesson(3, rng(5, 7), "일 · 공부 · 언어", "팟캐스트 5. 직업과 공부 · 6. 할 줄 아는 언어",
    ["<b>¿A qué te dedicas? ¿Trabajas o estudias?</b>에 대답할 수 있다.", "-ar 동사 <b>trabajar · estudiar · hablar</b>를 yo / tú / él로 바꿀 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Sofía, ¿a qué te dedicas?", "Yo trabajo. Trabajo en", "¡Qué bien! Me encantan", "A mí también. ¿Y tú, Mateo?", "Yo estudio. Estudio", "Sofía, ¿qué idiomas", "Hablo español y hablo", "Yo hablo español y también")
 + h("문법", "-ar 동사 현재형 — 끝만 바꾸면 돼요")
 + '''<table class="t"><tr><th>주어</th><th>어미</th><th>trabajar (일하다)</th><th>estudiar (공부하다)</th><th>hablar (말하다)</th></tr>
<tr><td>yo</td><td>-o</td><td><b>trabajo</b></td><td><b>estudio</b></td><td><b>hablo</b></td></tr>
<tr><td>tú</td><td>-as</td><td><b>trabajas</b></td><td><b>estudias</b></td><td><b>hablas</b></td></tr>
<tr><td>él / ella</td><td>-a</td><td><b>trabaja</b></td><td><b>estudia</b></td><td><b>habla</b></td></tr>
<tr><td>nosotros/as</td><td>-amos</td><td><b>trabajamos</b></td><td><b>estudiamos</b></td><td><b>hablamos</b></td></tr>
<tr><td>ellos / ellas</td><td>-an</td><td><b>trabajan</b></td><td><b>estudian</b></td><td><b>hablan</b></td></tr></table>
<div class="note g"><b>주어는 생략해도 돼요</b> 동사 끝(-o)만 봐도 '나'인 걸 알 수 있어서 <b>Trabajo en una librería.</b>처럼 yo를 빼고 말해요. 강조할 때만 <b>Yo</b> trabajo. <b>Yo</b> estudio.
<br><b>trabajar en + 장소</b> 서점에서 일해요 = Trabajo <b>en</b> una librería. · <b>estudiar + 과목</b> Estudio diseño gráfico. Estudio español.</div>
<div class="note r"><b>헷갈리는 단어</b> <b>librería</b> = 서점 (책을 파는 곳) · 도서관은 <b>biblioteca</b>예요!
<br>언어 이름은 소문자: <b>español, inglés, coreano</b> · <b>un poco de</b> inglés = 영어 조금</div>'''
 + h("연습 A", "동사를 알맞게 바꾸세요.")
 + blanks([f"Yo (trabajar) {BS} en una oficina.", f"¿Tú (estudiar) {BS} español?", f"Mateo (estudiar) {BS} diseño gráfico.", f"Sofía (hablar) {BS} un poco de inglés.", f"Nosotros (hablar) {BS} coreano y un poco de español."])
 + h("연습 B", "질문과 대답을 연결하세요.")
 + '<table class="t match"><tr><td>① ¿A qué te dedicas?</td><td>ⓐ Hablo coreano y un poco de inglés.</td></tr><tr><td>② ¿Qué idiomas hablas?</td><td>ⓑ Trabajo en un hospital.</td></tr><tr><td>③ ¿Qué estudias?</td><td>ⓒ Estudio español.</td></tr></table>'
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Trabajas o estudias?"), ("Mateo", "¿Qué idiomas hablas?"))
 + "</section>")

# ---------- Lesson 4 ----------
P.append(lesson(4, rng(7, 9), "형제자매와 취미", "팟캐스트 7. 형제자매 · 8. 취미",
    ["<b>¿Tienes hermanos?</b>에 <b>Tengo … / No tengo …</b>로 대답할 수 있다.", "<b>Me gusta + 동사원형</b>으로 취미를 2–3개 말할 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Sofía, ¿tienes hermanos?", "Sí, tengo un hermano", "¿Un hermano? ¿Es mayor", "Es menor.", "No, no tengo hermanos", "Sofía, ¿qué te gusta hacer?", "Mmm. Me gusta mucho leer", "A mí me gusta jugar", "Sí. Y también me gusta comer", "¿Comer? ¿Es un pasatiempo?")
 + h("문법 ①", "가족은 tener로 — 있어요 / 없어요")
 + '''<div class="two"><div class="box y"><b>있어요</b>
<p><b>Tengo un hermano.</b> 남자 형제가 한 명 있어요.<br><b>Tengo una hermana.</b> 여자 형제가 한 명 있어요.<br><b>Tengo dos hermanos.</b> 형제가 두 명 있어요.</p></div>
<div class="box y"><b>없어요</b>
<p><b>No tengo hermanos.</b> 형제자매가 없어요.<br><b>Soy hijo único / hija única.</b> 외동아들 / 외동딸이에요.<br>→ 없을 때는 un / una 없이 복수형!</p></div></div>
<div class="note g"><b>mayor / menor</b> 한국어처럼 '형·오빠·누나·언니'를 따로 부르지 않아요. <b>hermano mayor</b> 형/오빠 · <b>hermano menor</b> 남동생 · <b>hermana mayor</b> 누나/언니 · <b>hermana menor</b> 여동생
<br><b>¿Es mayor o menor que tú?</b> 너보다 나이가 많아, 어려? — <b>Es menor.</b> 동생이야.</div>
''' + h("문법 ②", "취미 = Me gusta + 동사원형") + '''
<table class="t"><tr><td>📖 <b>leer</b></td><td>읽다</td><td>🎧 <b>escuchar música</b></td><td>음악을 듣다</td></tr>
<tr><td>🌳 <b>pasear por el parque</b></td><td>공원을 산책하다</td><td>⚽ <b>jugar al fútbol</b></td><td>축구를 하다</td></tr>
<tr><td>🎬 <b>ver películas</b></td><td>영화를 보다</td><td>🍳 <b>cocinar</b></td><td>요리하다</td></tr>
<tr><td>🍽️ <b>comer</b></td><td>먹다</td><td>💬 <b>hablar con la gente</b></td><td>사람들과 이야기하다</td></tr></table>
<div class="note y"><b>여러 개 말하기</b> Me gusta leer. <b>También</b> me gusta escuchar música. <b>Y</b> me gusta pasear por el parque.
<br>동사원형은 몇 개가 와도 <b>gusta</b>(단수): ✓ Me gusta leer y cocinar. (Ep.6: 명사 복수면 gustan — Me gustan los libros.)</div>'''
 + h("연습 A", "그림을 보고 문장을 완성하세요.")
 + blanks([f"👦 (형제 1명) → Tengo {B}.", f"👧👧 (자매 2명) → Tengo {B}.", f"🙅 (형제 없음) → {B}. Soy hijo único.", f"📖 + 🎬 → Me gusta {B} y {B}."])
 + h("연습 B", "gusta / gustan 중 알맞은 것을 고르세요.")
 + blanks(["Me (gusta / gustan) jugar al fútbol.", "Me (gusta / gustan) los libros.", "¿Te (gusta / gustan) cocinar?", "A Sofía le (gusta / gustan) leer y escuchar música."])
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Mateo", "¿Tienes hermanos?"), ("Sofía", "¿Qué te gusta hacer? ¿Cuáles son tus pasatiempos?"))
 + "</section>")

# ---------- Lesson 5 ----------
P.append(lesson(5, rng(9, 11), "좋아하는 음식과 성격", "팟캐스트 9. 좋아하는 음식 · 10. 성격",
    ["2주차에 배운 <b>Mi comida favorita es …</b>를 다시 써 볼 수 있다.", "<b>¿Cómo eres? — Soy …</b>로 내 성격을 말하고, 형용사를 성에 맞출 수 있다."])
 + h("대화", "팟캐스트에서")
 + dlg("Mateo, ¿cuál es tu comida favorita?", "Mmm. Mi comida favorita es la comida", "A mí me gusta mucho la paella", "Mateo, ¿cómo eres?", "Mmm. Soy una persona divertida", "Sí, eres muy sociable", "¿Y cómo soy yo?", "Tú eres tranquila")
 + h("문법", "성격은 ser + 형용사 (여자면 -a로)")
 + '''<table class="t"><tr><th>형용사</th><th>남성 (Mateo)</th><th>여성 (Sofía)</th><th>뜻</th></tr>
<tr><td>-o → -a</td><td>Soy <b>tranquilo</b>.</td><td>Soy <b>tranquila</b>.</td><td>차분한</td></tr>
<tr><td></td><td>Soy <b>divertido</b>.</td><td>Soy <b>divertida</b>.</td><td>재미있는</td></tr>
<tr><td></td><td>Soy <b>simpático</b>. +보너스</td><td>Soy <b>simpática</b>.</td><td>상냥한, 친절한</td></tr>
<tr><td>-e / 자음 (형태 같음)</td><td>Soy <b>alegre</b>.</td><td>Soy <b>alegre</b>.</td><td>밝은, 명랑한</td></tr>
<tr><td></td><td>Soy <b>sociable</b>.</td><td>Soy <b>sociable</b>.</td><td>사교적인</td></tr>
<tr><td></td><td>Soy <b>joven</b>.</td><td>Soy <b>joven</b>.</td><td>젊은</td></tr></table>
<div class="note g"><b>una persona + 형용사</b> persona(사람)는 항상 여성 명사라서 남자도 <b>una persona divertida</b>라고 해요. 마테오: <b>Soy una persona divertida.</b>
<br><b>muy</b> = 아주 → Eres <b>muy</b> sociable. · 2주차 복습: <b>Me encanta</b> la comida mexicana. · La paella es <b>muy rica</b>.</div>
<div class="note y"><b>ser vs estar 미리 보기</b> 성격(원래 그런 사람)은 <b>ser</b>: Soy tranquila. · 지금 기분은 <b>estar</b>: Estoy cansado. 피곤해요. (뒤 주차에서 자세히 배워요)</div>'''
 + h("연습 A", "형용사를 알맞은 형태로 바꾸세요.")
 + blanks([f"Sofía es (tranquilo) → {B}", f"Mateo es (divertido) → {B}", f"Ana es (alegre) → {B}", f"Yo soy una persona (sociable) → {B}", f"Mi hermana es (simpático) → {B}"])
 + h("연습 B", "마테오와 소피아를 비교해 표를 채우세요.")
 + '<table class="t fill"><tr><th></th><th>나이</th><th>출신</th><th>일/공부</th><th>좋아하는 음식</th><th>성격</th></tr><tr><td><b>Sofía</b></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td><b>Mateo</b></td><td></td><td></td><td></td><td></td><td></td></tr></table>'
 + h("말하기", "질문에 소리 내어 답하세요")
 + ask(("Sofía", "¿Cuál es tu comida favorita?"), ("Sofía", "¿Cómo eres? ¿Eres una persona tranquila?"))
 + "</section>")

# ---------- Lesson 6 ----------
iQ = find("Ahora, un pequeño reto")
iR = find("Ahora, el último reto")
P.append(lesson(6, rng(11, None), "새로운 사람에게 자기소개하기", "팟캐스트 11. 자기소개 · 12. 따라 하기 · 13. 기억력 퀴즈 · 14. 마지막 도전",
    ["<b>5–7문장 자기소개</b>를 멈추지 않고 말할 수 있다.", "처음 만난 사람에게 <b>¿Cómo te llamas? ¿De dónde eres? ¿Qué te gusta hacer?</b>를 되물을 수 있다."])
 + h("예시", "마테오와 소피아의 자기소개")
 + '<div class="two"><div class="story"><b class="cM">Mateo</b><br>Hola, me llamo Mateo. Soy de México. Vivo en Madrid. Estudio diseño gráfico. Me gusta el fútbol.</div>'
 + '<div class="story"><b class="cS">Sofía</b><br>Hola, me llamo Sofía. Soy de España. Vivo en Madrid. Trabajo en una librería. Me gusta leer.</div></div>'
 + h("단계별", "Paso a paso — 자기소개 만들기 (팟캐스트 12번 구간)")
 + '''<table class="t"><tr><th>단계</th><th>패턴</th><th>질문하기</th></tr>
<tr><td>① 이름</td><td><b>Hola, me llamo …</b></td><td>¿Cómo te llamas?</td></tr>
<tr><td>② 나이</td><td><b>Tengo … años.</b></td><td>¿Cuántos años tienes?</td></tr>
<tr><td>③ 출신</td><td><b>Soy de …</b></td><td>¿De dónde eres?</td></tr>
<tr><td>④ 사는 곳</td><td><b>Vivo en …</b></td><td>¿Dónde vives?</td></tr>
<tr><td>⑤ 일 · 공부</td><td><b>Trabajo en … / Estudio …</b></td><td>¿A qué te dedicas?</td></tr>
<tr><td>⑥ 언어 · 가족</td><td><b>Hablo … / Tengo un hermano.</b></td><td>¿Qué idiomas hablas? ¿Tienes hermanos?</td></tr>
<tr><td>⑦ 좋아하는 것</td><td><b>Me gusta … / Soy …</b></td><td>¿Qué te gusta hacer? ¿Cómo eres?</td></tr></table>'''
 + h("퀴즈", f"Un pequeño reto — 기억력 퀴즈 ({fmt(T[iQ])})")
 + '<p class="sm">플레이어에서 해당 문장부터 재생하고, 정답이 나오기 전에 먼저 말해 보세요.</p>'
 + blanks([f"¿De dónde es Sofía? {B}", f"¿Dónde vive Mateo? {B}", f"¿Qué le gusta hacer a Sofía? {B}", f"보너스: ¿Cuántos años tiene Mateo? {B}", f"보너스: ¿Tiene hermanos Mateo? {B}"])
 + h("최종 미션", f"El último reto — 나의 자기소개 (Mi presentación) ({fmt(T[iR])})")
 + '''<table class="t mine"><tr><th>항목</th><th>패턴</th><th>나의 문장</th></tr>
<tr><td>① 인사 · 이름</td><td><b>Hola, me llamo …</b></td><td></td></tr>
<tr><td>② 나이</td><td><b>Tengo … años.</b></td><td></td></tr>
<tr><td>③ 출신 · 사는 곳</td><td><b>Soy de … Vivo en …</b></td><td></td></tr>
<tr><td>④ 일 · 공부</td><td><b>Trabajo en … / Estudio …</b></td><td></td></tr>
<tr><td>⑤ 언어</td><td><b>Hablo … y un poco de …</b></td><td></td></tr>
<tr><td>⑥ 가족</td><td><b>Tengo … / No tengo hermanos.</b></td><td></td></tr>
<tr><td>⑦ 취미 · 성격</td><td><b>Me gusta … Soy …</b></td><td></td></tr></table>
<div class="note y"><b>예시</b> Hola, me llamo Minji. Tengo 35 años. Soy de Busan, pero vivo en Ilsan. Trabajo en una oficina. Hablo coreano y un poco de español. Tengo una hermana menor. Me gusta ver películas y caminar. Soy una persona tranquila y alegre. ¡Encantada!</div>
<p class="sm">처음 만났을 때 마무리 인사: <b>Encantado</b>(남) / <b>Encantada</b>(여) 만나서 반가워요 · <b>Mucho gusto</b> (Ep.1 복습)</p>
''' + h("자기 점검", "이제 할 수 있나요?")
 + '<ul class="chk"><li>이름과 나이를 말할 수 있다. (Me llamo … · Tengo … años)</li><li>출신과 사는 곳을 구분해 말할 수 있다. (Soy de … · Vivo en …)</li><li>trabajar · estudiar · hablar를 yo / tú / él로 바꿀 수 있다.</li><li>형제자매가 있는지 없는지 말할 수 있다.</li><li>Me gusta + 동사원형으로 취미를 2개 이상 말할 수 있다.</li><li>성격 형용사를 내 성에 맞게 쓸 수 있다. (tranquilo / tranquila)</li><li>마지막 도전(' + fmt(T[iR]) + ')에서 5–7문장으로 자기소개를 할 수 있다.</li></ul>'
 + '<p class="sm">팟캐스트의 마지막 말: <b>Puedes hablar de ti en español. Sigue practicando.</b> — 이제 스페인어로 자기 자신에 대해 말할 수 있어요. 계속 연습하세요!</p>'
 + "</section>")

# ---------- Appendix ----------
P.append('''<section class="lesson"><div class="hd"><div class="k">APÉNDICE A</div><h1>정답</h1></div>
<div class="ans-list">
<p><b>Lesson 1</b> A: 1 veinticinco · 2 veintiocho · 3 treinta · 4 (나의 나이) &nbsp;|&nbsp; B: 1 Tengo · 2 tienes · 3 llamo · 4 llamas</p>
<p><b>Lesson 2</b> A: 1 soy · 2 vive · 3 vives · 4 es · 5 vivimos &nbsp;|&nbsp; B: 1 de España / en Madrid · 2 Mateo es de México y vive en Madrid. · 3 (예) Soy de Corea y vivo en Ilsan.</p>
<p><b>Lesson 3</b> A: 1 trabajo · 2 estudias · 3 estudia · 4 habla · 5 hablamos &nbsp;|&nbsp; B: ①ⓑ ②ⓐ ③ⓒ</p>
<p><b>Lesson 4</b> A: 1 un hermano · 2 dos hermanas · 3 No tengo hermanos · 4 leer / ver películas &nbsp;|&nbsp; B: 1 gusta · 2 gustan · 3 gusta · 4 gusta</p>
<p><b>Lesson 5</b> A: 1 tranquila · 2 divertido · 3 alegre · 4 sociable · 5 simpática<br>
표: Sofía — 28 años · España · trabaja en una librería · la paella · tranquila y alegre / Mateo — 25 años · México · estudia diseño gráfico · la comida mexicana · divertido y sociable</p>
<p><b>Lesson 6</b> 퀴즈: 1 Sofía es de España. · 2 Mateo vive en Madrid. · 3 A Sofía le gusta leer. · 4 Tiene 25 años. · 5 No, no tiene hermanos. Es hijo único.</p>
</div>
<div class="hd" style="margin-top:28px"><div class="k">APÉNDICE B</div><h1>동사표 한눈에 보기</h1></div>
<p class="sm">이번 에피소드의 핵심 동사예요. 우선 yo / tú / él·ella 세 줄만 외워도 충분해요.</p>
<table class="t"><tr><th>주어</th><th>ser (이다)</th><th>tener (가지다)</th><th>vivir (살다)</th><th>trabajar (일하다)</th><th>estudiar (공부하다)</th><th>hablar (말하다)</th><th>llamarse (이름이 ~이다)</th></tr>
<tr><td>yo</td><td>soy</td><td>tengo</td><td>vivo</td><td>trabajo</td><td>estudio</td><td>hablo</td><td>me llamo</td></tr>
<tr><td>tú</td><td>eres</td><td>tienes</td><td>vives</td><td>trabajas</td><td>estudias</td><td>hablas</td><td>te llamas</td></tr>
<tr><td>él / ella / usted</td><td>es</td><td>tiene</td><td>vive</td><td>trabaja</td><td>estudia</td><td>habla</td><td>se llama</td></tr>
<tr><td>nosotros/as</td><td>somos</td><td>tenemos</td><td>vivimos</td><td>trabajamos</td><td>estudiamos</td><td>hablamos</td><td>nos llamamos</td></tr>
<tr><td>vosotros/as</td><td>sois</td><td>tenéis</td><td>vivís</td><td>trabajáis</td><td>estudiáis</td><td>habláis</td><td>os llamáis</td></tr>
<tr><td>ellos / ellas / ustedes</td><td>son</td><td>tienen</td><td>viven</td><td>trabajan</td><td>estudian</td><td>hablan</td><td>se llaman</td></tr></table>
<p class="sm">gustar은 2주차와 같아요: me gusta / te gusta / le gusta (+ 복수 명사면 gustan)</p>
</section>''')

voc = ['<section class="lesson"><div class="hd"><div class="k">APÉNDICE C</div><h1>단어장</h1><div class="s">플레이어의 \'단어장\' 탭과 같은 내용이에요. 외운 단어는 □에 체크하세요.</div></div><div class="vcols">']
for title, rows in VOCAB:
    voc.append(f'<table class="t v"><tr><th colspan="2">{e(title)}</th></tr>' + "".join(
        f'<tr><td><span class="cb"></span><b>{e(a)}</b></td><td>{e(b)}</td></tr>' for a, b in rows) + "</table>")
voc.append("</div></section>")
P.append("".join(voc))

CSS = open(f"{work}/../book.css", encoding="utf-8").read()
open(out, "w", encoding="utf-8").write(f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>스페인어 자기소개 교재 Ep18</title><style>{CSS}</style></head><body>{"".join(P)}</body></html>')
print("ok")
