"""lines.py 각 문장의 시작 시각을 유튜브 자동 자막 단어 시각(asr_words.txt)에 맞춰 times.json으로 저장."""
import json, re, sys, unicodedata, difflib, os
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from lines import L

def norm(s):
    s = re.sub(r"\([^)]*\)", " ", s)
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-zñ0-9]+", s)

W = []
for ln in open(f"{here}/asr_words.txt", encoding="utf-8"):
    t, w = ln.split(" ", 1)
    W += [(tok, float(t)) for tok in norm(w)]
wt = [t for t, _ in W]
lt, owner = [], []
for i, x in enumerate(L):
    if x[0] != "H":
        toks = norm(x[1]); lt += toks; owner += [i] * len(toks)
m = {}
for a, b, n in difflib.SequenceMatcher(None, lt, wt, autojunk=False).get_matching_blocks():
    for k in range(n): m[a + k] = b + k
T, pos = {}, 0
for i, x in enumerate(L):
    if x[0] == "H": continue
    n = len(norm(x[1]))
    hit = next((k for k in range(pos, pos + n) if k in m), None)
    if hit is not None:
        # 첫 단어가 안 맞으면 맞은 단어 시각에서 앞 단어 수만큼 대략 빼기
        T[i] = round(max(0, W[m[hit]][1] - 0.35 * (hit - pos) - 0.25), 2)
    pos += n
# 못 맞춘 줄은 앞뒤 사이로 채우고, 순서가 뒤집히지 않게
idx = [i for i, x in enumerate(L) if x[0] != "H"]
for j, i in enumerate(idx):
    if i not in T:
        prev = T[idx[j-1]] if j else 0
        nxt = next((T[k] for k in idx[j+1:] if k in T), prev + 3)
        T[i] = round((prev + nxt) / 2, 2); print("interp", i, L[i][1][:40], T[i])
for a, b in zip(idx, idx[1:]):
    if T[b] <= T[a]: print("ORDER", a, b, L[a][1][:30], T[a], T[b])
json.dump({str(k): T[k] for k in idx}, open(f"{here}/times.json", "w"), indent=0)
print(len(idx), "lines")
