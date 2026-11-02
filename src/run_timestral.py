"""Run Timestral (local weights, CPU) with the same splits/metrics as the baselines.

Usage: python src/run_timestral.py [weights_root] [--test]
weights_root defaults to ./weights; it holds one folder per size:
  weights/Timestral-28M/{config.json, model.safetensors}
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import sys, time, os
import numpy as np
import pandas as pd
import torch
from timestral import TimestralForecaster
from evalcore import QS, load, run, save, H

torch.set_num_threads(os.cpu_count())
df = load()
args = [a for a in sys.argv[1:] if not a.startswith("--")]
root = Path(args[0]) if args else ROOT / "weights"
test = "--test" in sys.argv
os.makedirs(ROOT / "results", exist_ok=True)

dow_full = np.array([d.dayofweek for d in pd.date_range(df.index[0], periods=len(df) + H, freq="D")], float)

def make_fn(fc, calendar):
    def fn(ctx, h):
        B, T = ctx.shape
        kw = {}
        if calendar:
            kw["categorical_known_covariates"] = np.broadcast_to(dow_full[: T + h], (B, 1, T + h)).copy()
        out = fc.forecast(ctx[:, None, :], prediction_length=h, **kw)
        levels = list(out.quantile_levels)
        q = out.quantiles[:, 0].cpu().numpy()  # (B, h, Q)
        return np.stack([q[..., levels.index(min(levels, key=lambda l: abs(l - a)))] for a in QS], -1)
    return fn

if test:
    from timestral import TimestralConfig
    from timestral.model import TimestralModel
    knots = (0.01, 0.05, 0.1, 0.2, 0.25, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.9, 0.95, 0.99)
    cfg = TimestralConfig(patch_size=8, d_model=32, num_heads=4, mlp_hidden_dim=64,
                          block_schedule=("time", "time_variate", "time", "time_variate"),
                          quantile_knots=knots, block_size=4, context_length=512)
    models = {"Timestral-TEST": TimestralForecaster(TimestralModel(cfg).eval())}
else:
    models = {}
    def size(p):  # "Timestral-28M" -> 28.0, unknown names last
        try:
            return float(p.name.split("-")[1].rstrip("Mm"))
        except (IndexError, ValueError):
            return float("inf")
    for d in sorted((p for p in root.iterdir() if (p / "model.safetensors").exists()), key=size):
        models[d.name] = TimestralForecaster.from_pretrained(str(d))
    if not models:
        sys.exit(f"No weights found in {root}. See weights/README.md.")

largest = list(models)[-1]
for name, fc in models.items():
    variants = [(name, False)] + ([(f"{name} + calendario", True)] if name == largest else [])
    for label, cal in variants:
        t = time.time()
        res = run(make_fn(fc, cal), df)
        save(label, res, ROOT / "results" / f"{label.replace(' ', '_').replace('+', 'cal')}.json")
        m = pd.DataFrame(res["holdout28"]["metrics"], index=df.columns)
        print(f"{label}: {time.time()-t:.1f}s  MASE med={m.MASE.median():.3f} WQL med={m.WQL.median():.3f} Cov80={m.Cov80.mean():.0f}%")
