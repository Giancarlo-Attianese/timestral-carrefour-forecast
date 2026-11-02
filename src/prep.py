"""Aggregate Carrefour order lines into daily time series."""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import pandas as pd

SRC = ROOT / "data" / "Carrefour.csv"
df = pd.read_csv(SRC, low_memory=False, encoding="cp1252")
df["date"] = pd.to_datetime(df.order_date, format="%m/%d/%Y")
df["valid"] = ~df.status.isin(["canceled", "order_refunded"])
df["net"] = df["Selling price"].where(df.valid, 0.0)

idx = pd.date_range(df.date.min(), df.date.max(), freq="D")
series = {}
series["Righe d'ordine (totale)"] = df.groupby("date").size()
series["Fatturato netto (totale)"] = df.groupby("date").net.sum()
series["Righe d'ordine valide"] = df[df.valid].groupby("date").size()

cat_rev = df[df.valid].groupby("category").net.sum().sort_values(ascending=False)
print(cat_rev)
top = [c for c in cat_rev.index if c != "Others"][:8]  # "Others" is a residual bucket that dies out in Sep 2021
for c in top:
    series[f"Fatturato netto · {c}"] = df[df.valid & (df.category == c)].groupby("date").net.sum()

out = pd.DataFrame({k: v.reindex(idx).fillna(0.0) for k, v in series.items()})
out.index.name = "date"
(ROOT / "results").mkdir(exist_ok=True)
out.to_csv(ROOT / "results" / "series.csv")
print(out.shape)
print(out.describe().T[["mean", "std", "min", "max"]])
