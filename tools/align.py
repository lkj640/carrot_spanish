import json, re, unicodedata, difflib, sys
sys.path.insert(0, sys.argv[1])
from lines import L

def norm(s):
    s = re.sub(r"\([^)]*\)", " ", s)
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-zñ0-9]+", s)

asr = json.load(open(sys.argv[2]))
W = []  # (token, start)
for seg in asr:
    for st, en, w in seg["w"]:
        for t in norm(w):
            W.append((t, st))
wt = [t for t, _ in W]

lt, owner = [], []
for i, x in enumerate(L):
    if x[0] == "H":
        continue
    toks = norm(x[1])
    lt += toks
    owner += [i] * len(toks)

sm = difflib.SequenceMatcher(None, lt, wt, autojunk=False)
m = {}
for a, b, n in sm.get_matching_blocks():
    for k in range(n):
        m[a + k] = b + k

starts = {}
pos = 0
for i, x in enumerate(L):
    if x[0] == "H":
        continue
    n = len(norm(x[1]))
    idx = range(pos, pos + n)
    hit = next((k for k in idx if k in m), None)
    if hit is not None:
        # estimate start: matched word time minus ~0.35s per preceding unmatched token
        starts[i] = max(0, W[m[hit]][1] - 0.35 * (hit - pos))
    pos += n

# fill gaps + enforce monotonic
keys = [i for i, x in enumerate(L) if x[0] != "H"]
prev = 0.0
out = {}
for j, i in enumerate(keys):
    t = starts.get(i)
    if t is None or t < prev:
        nxt = next((starts[k] for k in keys[j + 1:] if k in starts and starts[k] > prev), prev + 2)
        t = prev + min(2.0, (nxt - prev) / 2)
        print("fill", i, L[i][1][:40], file=sys.stderr)
    out[i] = round(t - 0.15 if t > 0.15 else t, 2)
    prev = t
json.dump(out, open(sys.argv[3], "w"))
for i in keys:
    print(f"{out[i]:7.2f} {L[i][0]} {L[i][1][:60]}")
