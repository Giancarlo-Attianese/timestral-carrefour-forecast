"""Collect series + all model results into one JSON bundle for the web app."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import json, glob
import numpy as np
from evalcore import QS, H, load, metrics

df = load()
vals = df.values.T.astype(float)
B, T = vals.shape
ORDER = ["Seasonal Naive (7g)", "AutoETS", "AutoTheta", "AutoARIMA",
         "Timestral-5M", "Timestral-28M", "Timestral-123M", "Timestral-209M"]

def gmean(x):
    x = np.asarray(x, float)
    return float(np.exp(np.mean(np.log(np.maximum(x, 1e-9)))))

models = {}
for f in glob.glob(str(ROOT / "results" / "*.json")):
    if f.endswith("bundle.json"):
        continue
    d = json.load(open(f))
    r = d["results"]
    hold = np.array(r["holdout28"]["q"])
    roll = np.concatenate([np.array(r[f"rolling7_{k}"]["q"]) for k in range(4)], axis=1)
    fut = np.array(r["future28"]["q"])
    o = T - H
    y = vals[:, o:]
    m = {"holdout": [metrics(y[b], hold[b], vals[b, :o]) for b in range(B)],
         "rolling": [metrics(y[b], roll[b], vals[b, :o]) for b in range(B)]}
    models[d["model"]] = {"q": {"holdout": hold.round(1).tolist(), "rolling": roll.round(1).tolist(),
                                "future": fut.round(1).tolist()}, "metrics": m}

names = sorted(models, key=lambda n: (ORDER.index(n.split(" + ")[0]) if n.split(" + ")[0] in ORDER else 99, n))
ref = "Seasonal Naive (7g)"
leader = {}
for sc in ["holdout", "rolling"]:
    rows = []
    for n in names:
        mm, rm = models[n]["metrics"][sc], models[ref]["metrics"][sc]
        rows.append({
            "model": n,
            "relMASE": gmean([a["MASE"] / b["MASE"] for a, b in zip(mm, rm)]),
            "relWQL": gmean([a["WQL"] / b["WQL"] for a, b in zip(mm, rm)]),
            "sMAPE": float(np.mean([a["sMAPE"] for a in mm])),
            "Cov80": float(np.mean([a["Cov80"] for a in mm])),
            "wins": int(sum(a["MASE"] < b["MASE"] for a, b in zip(mm, rm))),
        })
    leader[sc] = rows

bundle = {
    "dates": [d.strftime("%Y-%m-%d") for d in df.index],
    "series": list(df.columns),
    "values": vals.round(2).tolist(),
    "H": H, "quantiles": QS, "models": names,
    "forecasts": {n: models[n] for n in names},
    "leaderboard": leader,
    "n_rows": 286392,
}
json.dump(bundle, open(ROOT / "results" / "bundle.json", "w", encoding="utf-8"), separators=(",", ":"), ensure_ascii=False)
for sc in leader:
    print(sc)
    for r in sorted(leader[sc], key=lambda r: r["relWQL"]):
        print(f"  {r['model']:32s} relMASE={r['relMASE']:.3f} relWQL={r['relWQL']:.3f} sMAPE={r['sMAPE']:.1f} Cov80={r['Cov80']:.0f} wins={r['wins']}/{B}")
