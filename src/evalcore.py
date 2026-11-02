"""Shared evaluation setup: splits, quantile levels, metrics."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import json
import numpy as np
import pandas as pd

QS = [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95]   # quantiles stored & scored for every model
H = 28                                         # holdout length (days) / future horizon
ROLL_H = 7                                     # rolling backtest horizon
SEASON = 7

def load():
    s = pd.read_csv(ROOT / "results" / "series.csv", parse_dates=["date"], index_col="date")
    return s

def settings(df):
    """Yield (setting_name, origin_index, horizon). origin = number of observed days used."""
    T = len(df)
    out = [("holdout28", T - H, H)]
    for k in range(H // ROLL_H):
        out.append((f"rolling7_{k}", T - H + k * ROLL_H, ROLL_H))
    out.append(("future28", T, H))
    return out

def metrics(y, q, train):
    """y: (h,), q: (h, len(QS)) quantile forecasts, train: in-sample history."""
    med = q[:, QS.index(0.5)]
    err = y - med
    scale = np.mean(np.abs(train[SEASON:] - train[:-SEASON]))
    pin = []
    for j, a in enumerate(QS):
        d = y - q[:, j]
        pin.append(np.sum(np.maximum(a * d, (a - 1) * d)))
    wql = 2 * np.mean(pin) / max(np.sum(np.abs(y)), 1e-9)
    lo, hi = q[:, QS.index(0.1)], q[:, QS.index(0.9)]
    return dict(
        MAE=float(np.mean(np.abs(err))),
        RMSE=float(np.sqrt(np.mean(err ** 2))),
        sMAPE=float(np.mean(2 * np.abs(err) / np.maximum(np.abs(y) + np.abs(med), 1e-9)) * 100),
        MASE=float(np.mean(np.abs(err)) / scale),
        WQL=float(wql),
        Cov80=float(np.mean((y >= lo) & (y <= hi)) * 100),
    )

def run(forecast_fn, df):
    """forecast_fn(ctx: np.ndarray (B, T), h) -> np.ndarray (B, h, len(QS))."""
    vals = df.values.T.astype(float)  # (B, T)
    res = {}
    for name, origin, h in settings(df):
        q = forecast_fn(vals[:, :origin], h)
        q = np.sort(np.clip(q, 0, None), axis=-1)  # sales are non-negative; guard against crossing
        entry = {"origin": origin, "h": h, "q": q.round(3).tolist()}
        if origin + h <= vals.shape[1]:
            entry["metrics"] = [metrics(vals[b, origin:origin + h], q[b], vals[b, :origin])
                                for b in range(vals.shape[0])]
        res[name] = entry
    return res

def save(name, res, path):
    with open(path, "w") as f:
        json.dump({"model": name, "results": res}, f)
