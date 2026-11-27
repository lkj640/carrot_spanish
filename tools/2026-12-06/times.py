"""이 영상은 단어별 자동 자막 시각이 없어요. captions.json(자막 덩어리 시작 ms, 글)에서
덩어리 안 글자 위치 비율로 각 줄의 시작 시각을 계산해 times.json으로 저장."""
import json, os, re, sys, unicodedata
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from lines import L
NUM = {"4": "cuatro", "10": "diez", "11": "once"}
def norm(s):
    s = re.sub(r"\d+", lambda m: NUM.get(m.group(), m.group()), s)
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if c.isalnum() and not unicodedata.combining(c))
ev = json.load(open(f"{here}/captions.json"))
S, TT = "", []
for i, (ms, txt) in enumerate(ev):
    n = norm(txt); t0 = ms / 1000
    span = (ev[i + 1][0] / 1000 if i + 1 < len(ev) else t0 + 6) - t0
    rate = min(span / max(len(n), 1), 1 / 11)   # 초/글자 (빠르게 말해도 최대 11글자/초)
    S += n; TT += [t0 + k * rate for k in range(len(n))]
T, pos = {}, 0
for i, x in enumerate(L):
    if x[0] == "H": continue
    n = norm(x[1])
    for k in (16, 10, 6, 4):
        f = S.find(n[:k], pos, pos + 250)
        if f >= 0: break
    else:
        raise SystemExit(f"못 찾음: {i} {x[1]}")
    T[str(i)] = round(max(TT[f] - 0.3, 0), 1)
    pos = f + max(len(n) - 8, 1)
v = list(T.values()); assert v == sorted(v), "시간 순서가 뒤집혔어요"
json.dump(T, open(f"{here}/times.json", "w"), indent=0); print(len(T), "lines")
for i, x in enumerate(L):
    if x[0] != "H": print(T[str(i)], x[1][:50])
