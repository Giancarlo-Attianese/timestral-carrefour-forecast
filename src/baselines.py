"""Classical baselines via statsforecast, evaluated with the same splits as Timestral."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import os, time
import numpy as np
import pandas as pd
from statsforecast import StatsForecast
from statsforecast.models import SeasonalNaive, AutoETS, AutoARIMA, AutoTheta
from evalcore import QS, load, run, save, SEASON

os.makedirs(ROOT / "results", exist_ok=True)
df = load()

LEVELS = [50, 80, 90]  # -> quantiles 0.25/0.75, 0.1/0.9, 0.05/0.95

def make_fn(model_factory, alias):
    def fn(ctx, h):
        B, T = ctx.shape
        dates = pd.date_range("2000-01-01", periods=T, freq="D")
        long = pd.DataFrame({"unique_id": np.repeat(np.arange(B), T),
                             "ds": np.tile(dates, B), "y": ctx.ravel()})
        sf = StatsForecast(models=[model_factory()], freq="D", n_jobs=1)
        fc = sf.forecast(df=long, h=h, level=LEVELS)
        out = np.zeros((B, h, len(QS)))
        for b in range(B):
            g = fc[fc.unique_id == b]
            col = {0.5: g[alias].values}
            for L in LEVELS:
                a = (1 - L / 100) / 2
                col[round(a, 3)] = g[f"{alias}-lo-{L}"].values
                col[round(1 - a, 3)] = g[f"{alias}-hi-{L}"].values
            out[b] = np.stack([col[q] for q in QS], axis=-1)
        return np.nan_to_num(out)
    return fn

MODELS = {
    "Seasonal Naive (7g)": (lambda: SeasonalNaive(season_length=SEASON), "SeasonalNaive"),
    "AutoETS": (lambda: AutoETS(season_length=SEASON), "AutoETS"),
    "AutoARIMA": (lambda: AutoARIMA(season_length=SEASON), "AutoARIMA"),
    "AutoTheta": (lambda: AutoTheta(season_length=SEASON), "AutoTheta"),
}

for name, (fac, alias) in MODELS.items():
    t = time.time()
    res = run(make_fn(fac, alias), df)
    save(name, res, ROOT / "results" / f"{alias}.json")
    m = pd.DataFrame(res["holdout28"]["metrics"], index=df.columns)
    print(f"{name}: {time.time()-t:.1f}s  holdout median MASE={m.MASE.median():.3f} WQL={m.WQL.median():.3f} Cov80={m.Cov80.mean():.0f}%")
