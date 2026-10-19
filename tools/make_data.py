"""모임 자료를 사이트용 data.json으로 변환합니다.

사용법
  # (A) lines.py + vocab.py + times.json 으로 만들기 (Ep.6 이후 방식)
  python3 tools/make_data.py src  tools/2026-10-25  meetings/2026-10-25/data.json

  # (B) 예전 단일 플레이어 HTML에서 뽑아내기 (Ep.1)
  python3 tools/make_data.py html  <플레이어.html>  meetings/2026-10-18/data.json
"""
import html, json, re, sys


def from_src(d):
    sys.path.insert(0, d)
    import lines
    from lines import L
    from vocab import VOCAB
    T = {int(k): v for k, v in json.load(open(f"{d}/times.json")).items()}
    secs = []
    for i, x in enumerate(L):
        if x[0] == "H":
            secs.append({"title": x[1], "lines": []})
        else:
            secs[-1]["lines"].append({"s": x[0], "t": T[i], "es": x[1], "ko": x[2]})
    vocab = [{"title": t, "rows": [list(r) for r in rows]} for t, rows in VOCAB]
    return secs, vocab, getattr(lines, "SPEAKERS", None)


def from_html(p):
    src = open(p, encoding="utf-8").read()
    main, voc = src.split('<section id="vocab">', 1)
    secs = []
    tok = re.compile(r'<h2>(.*?)</h2>|<div class="line (\w)"[^>]*data-t="([\d.]+)".*?<div class="es">(.*?)</div><div class="ko">(.*?)</div>', re.S)
    for m in tok.finditer(main):
        if m.group(1):
            secs.append({"title": html.unescape(m.group(1)), "lines": []})
        else:
            secs[-1]["lines"].append({"s": m.group(2), "t": float(m.group(3)),
                                      "es": html.unescape(m.group(4)), "ko": html.unescape(m.group(5))})
    vocab = []
    for t, tb in re.findall(r"<h3>(.*?)</h3><table>(.*?)</table>", voc, re.S):
        rows = [[html.unescape(a), html.unescape(b)] for a, b in
                re.findall(r'<td class="w">(.*?)</td><td class="">(.*?)</td>', tb)]
        vocab.append({"title": html.unescape(t), "rows": rows})
    return secs, vocab, None


if __name__ == "__main__":
    mode, src, out = sys.argv[1:4]
    secs, vocab, speakers = from_src(src) if mode == "src" else from_html(src)
    # 화자 이름(기본 S=Sofía, M=Mateo)을 바꾸려면 lines.py에 SPEAKERS = {"S": "…", "M": "…"}
    json.dump({**({"speakers": speakers} if speakers else {}), "sections": secs, "vocab": vocab}, open(out, "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    print(out, sum(len(s["lines"]) for s in secs), "lines,", len(secs), "sections,", sum(len(v["rows"]) for v in vocab), "words")
