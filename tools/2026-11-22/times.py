"""lines.py의 4번째 값(시작 초)을 times.json으로 저장."""
import json, os, sys
here = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, here)
from lines import L
T = {str(i): x[3] for i, x in enumerate(L) if x[0] != "H"}
v = list(T.values()); assert v == sorted(v), "시간 순서가 뒤집혔어요"
json.dump(T, open(f"{here}/times.json", "w"), indent=0); print(len(T), "lines")
