"""Build the web app in Italian and English from one template + results/bundle.json.

Output (GitHub Pages ready):
  docs/index.html      language picker (redirects by browser language)
  docs/it/index.html   Italian app
  docs/en/index.html   English app
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TPL = (ROOT / "app" / "app_template.html").read_text(encoding="utf-8")
BUNDLE = json.loads((ROOT / "results" / "bundle.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- page text (it -> en)
# Longer strings first, generic identifiers last. Every pair must match the template.
EN = [
    ("Carrefour Egitto · e-commerce · ott 2020 – set 2021", "Carrefour Egypt · e-commerce · Oct 2020 – Sep 2021"),
    ("Quanto prevede bene Timestral, il foundation model per serie temporali di Mistral, eseguito in locale su CPU e senza addestramento sui dati? Le ultime 4 settimane sono tenute fuori dal modello e servono a verificare le previsioni contro modelli statistici classici.",
     "How well does Timestral, Mistral's time-series foundation model, forecast when it runs locally on a CPU with no training on the data? The last 4 weeks are held out from the model and used to check its forecasts against classical statistical models."),
    ('aria-label="Sintesi"', 'aria-label="Summary"'),
    ('<label for="sel-series">Serie</label>', '<label for="sel-series">Series</label>'),
    ("Holdout 28 giorni</button>", "28-day holdout</button>"),
    ("Rolling 7 giorni</button>", "Rolling 7-day</button>"),
    ("Futuro (ott 2021)", "Future (Oct 2021)"),
    ("Banda di incertezza", "Uncertainty band"),
    ('<span class="lab">Livello</span>', '<span class="lab">Level</span>'),
    ('aria-label="Livello banda"', 'aria-label="Band level"'),
    ("Modelli nel grafico", "Models on chart"),
    ('aria-label="Serie storica con previsioni"', 'aria-label="Time series with forecasts"'),
    ("Metriche sulla serie selezionata", "Metrics for the selected series"),
    ("Classifica su tutte le 11 serie", "Leaderboard across all 11 series"),
    ("Errori relativi al Seasonal Naive (ripete la settimana precedente), media geometrica sulle serie. Sotto 1 il modello batte il riferimento; 0,80 significa errore più basso del 20%.",
     "Errors relative to Seasonal Naive (repeats the previous week), geometric mean across series. Below 1 the model beats the baseline; 0.80 means a 20% lower error."),
    ('aria-label="Scenario classifica"', 'aria-label="Leaderboard scenario"'),
    ("Holdout 28g</button>", "28-day holdout</button>"),
    ("Rolling 7g</button>", "Rolling 7-day</button>"),
    ("<h2>Serie per serie</h2>", "<h2>Series by series</h2>"),
    ("MASE relativo al Seasonal Naive per ogni serie e modello, nello scenario della classifica. Verde: meglio del riferimento; rosso: peggio. Clic su una riga per aprirla nel grafico.",
     "MASE relative to Seasonal Naive for every series and model, in the leaderboard scenario. Green: better than the baseline; red: worse. Click a row to open it in the chart."),
    (">Metodo</h2>", ">Method</h2>"),
    ("<h3>Dati</h3>", "<h3>Data</h3>"),
    ("<h3>Valutazione</h3>", "<h3>Evaluation</h3>"),
    ("<h3>Metriche</h3>", "<h3>Metrics</h3>"),
    ("<h3>Modelli</h3>", "<h3>Models</h3>"),
    ("<b>Holdout 28 giorni:</b> i modelli vedono i dati fino al 2 settembre 2021 e prevedono in un colpo solo i 28 giorni successivi.",
     "<b>28-day holdout:</b> the models see the data up to 2 September 2021 and forecast the next 28 days in one shot."),
    ("<b>Rolling 7 giorni:</b> quattro previsioni a una settimana, ognuna con tutti i dati disponibili fino a quel momento, sulle stesse 4 settimane.",
     "<b>Rolling 7-day:</b> four one-week forecasts over the same 4 weeks, each using all the data available up to that point."),
    ("<b>Futuro:</b> previsione dei 28 giorni dopo la fine del dataset, usando tutto l'anno. Non c'è un dato reale con cui confrontarla.",
     "<b>Future:</b> forecast of the 28 days after the end of the dataset, using the whole year. There is no actual data to compare it with."),
    ("Errore medio assoluto e quadratico della mediana, nell'unità della serie.", "Mean absolute and root mean squared error of the median, in the series' unit."),
    ("Errore percentuale simmetrico (0–200%).", "Symmetric percentage error (0–200%)."),
    ("MAE diviso l'errore del naive stagionale sui dati di training.", "MAE divided by the seasonal naive error on the training data."),
    ("Perdita quantile pesata su 7 quantili (5–95%): misura tutta la distribuzione prevista, non solo la mediana.",
     "Weighted quantile loss over 7 quantiles (5–95%): it scores the whole forecast distribution, not just the median."),
    ("<dt>Copertura 80%</dt>", "<dt>80% coverage</dt>"),
    ("Quota di giorni reali dentro l'intervallo 10–90%. Il valore ideale è 80%.", "Share of actual days inside the 10–90% interval. The ideal value is 80%."),
    ('toLocaleString("it-IT"', 'toLocaleString("en-GB"'),
    ('s.startsWith("Fatturato") ? "EGP" : "righe"', 's.startsWith("Net revenue") ? "EGP" : "lines"'),
    ('["gen","feb","mar","apr","mag","giu","lug","ago","set","ott","nov","dic"]', '["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]'),
    ("</b> righe d'ordine</span>", "</b> order lines</span>"),
    ("</b> giorni</span>", "</b> days</span>"),
    ("</b> serie giornaliere</span>", "</b> daily series</span>"),
    ("</b> modelli a confronto</span>", "</b> models compared</span>"),
    ("righe d'ordine del negozio online Carrefour in Egitto (Kaggle), aggregate per giorno. Il fatturato netto esclude gli ordini cancellati o rimborsati ed è in sterline egiziane (EGP). Le serie per categoria sono le 8 con più fatturato; \"Others\" è esclusa perché è un contenitore residuo che si azzera proprio nel periodo di test. Le serie hanno picchi molto alti nei giorni di promozione (es. 11.11, White Friday), che nessun modello senza calendario promozionale può prevedere.",
     "order lines from Carrefour's online store in Egypt (Kaggle), aggregated by day. Net revenue excludes cancelled or refunded orders and is in Egyptian pounds (EGP). The category series are the 8 with the highest revenue; \"Others\" is excluded because it is a residual bucket that drops to zero right in the test period. The series have very high spikes on promotion days (e.g. 11.11, White Friday) that no model can forecast without a promotion calendar."),
    (": zero-shot, pesi ufficiali Mistral eseguiti in locale su CPU, nessun addestramento su questi dati. La variante <i>+ calendario</i> riceve il giorno della settimana come covariata nota in futuro.<br><b>Classici</b> (statsforecast): Seasonal Naive, AutoETS, AutoTheta e AutoARIMA con stagionalità settimanale, stimati su ogni serie. Tutte le previsioni sono limitate a valori ≥ 0.",
     ": zero-shot, official Mistral weights run locally on CPU, no training on this data. The <i>+ calendar</i> variant receives the day of the week as a known-future covariate.<br><b>Classical</b> (statsforecast): Seasonal Naive, AutoETS, AutoTheta and AutoARIMA with weekly seasonality, fitted on each series. All forecasts are clipped at ≥ 0."),
    ("Bozza: per ora ci sono solo i modelli classici. I risultati di Timestral arrivano appena i pesi sono disponibili.",
     "Draft: only the classical models are included so far. Timestral results will be added once the weights are available."),
    ("Miglior Timestral · holdout", "Best Timestral · holdout"),
    ("e MASE ${pct(t.relMASE)} rispetto al Seasonal Naive. Batte il riferimento su ${t.wins} serie su ${D.series.length}.",
     "and MASE ${pct(t.relMASE)} vs Seasonal Naive. Beats the baseline on ${t.wins} of ${D.series.length} series."),
    ("Contro il miglior classico", "Against the best classical model"),
    ('"Timestral avanti" : c.model+" avanti"', '"Timestral ahead" : c.model+" ahead"'),
    ("Differenza WQL: ${fmt(Math.abs(t.relWQL-c.relWQL)*100,1)} punti.", "WQL gap: ${fmt(Math.abs(t.relWQL-c.relWQL)*100,1)} points."),
    ("Settimana per settimana", "Week by week"),
    ("con previsioni a 7 giorni aggiornate ogni settimana. Copertura dell'intervallo 80%:", "with 7-day forecasts updated every week. 80% interval coverage:"),
    ("Miglior classico · holdout", "Best classical · holdout"),
    ("MASE ${pct(c.relMASE)} rispetto al Seasonal Naive.</span>", "MASE ${pct(c.relMASE)} vs Seasonal Naive.</span>"),
    ('name:"Dati reali"', 'name:"Actual"'),
    ('name:"Futuro"', 'name:"Future"'),
    ('name:"Dati tenuti fuori"', 'name:"Held-out data"'),
    ("`Banda ${state.level}% · ${state.band}`", "`${state.level}% band · ${state.band}`"),
    ("Previsione unica fatta il 2 settembre 2021 per i 28 giorni successivi, che i modelli non hanno visto.",
     "Single forecast made on 2 September 2021 for the next 28 days, which the models have not seen."),
    ("Quattro previsioni a 7 giorni, una per settimana, ognuna con i dati disponibili fino al giorno prima.",
     "Four 7-day forecasts, one per week, each using the data available up to the day before."),
    ("Previsione dei 28 giorni dopo la fine del dataset (1–28 ottobre 2021), basata su tutto l'anno. Non ci sono dati reali per verificarla.",
     "Forecast of the 28 days after the end of the dataset (1–28 October 2021), based on the whole year. There is no actual data to check it against."),
    ("Trascina la barra in basso per vedere tutta la serie.", "Drag the bar at the bottom to see the whole series."),
    ("Previsione per le prossime 4 settimane", "Forecast for the next 4 weeks"),
    (": somma delle mediane giornaliere per settimana (${unit(name)}). Per confronto, l'ultima settimana reale e la media settimanale dell'anno.",
     ": sum of daily medians per week (${unit(name)}). For comparison, the last actual week and the year's weekly average."),
    ("<th>Totale 28g</th>", "<th>28-day total</th>"),
    ("Ultima settimana reale · media settimanale anno", "Last actual week · yearly weekly average"),
    (', scenario ${sc==="holdout"?"holdout 28 giorni":"rolling 7 giorni"}. In verde il valore migliore per colonna. MAE e RMSE in ${unit(name)}.',
     ', ${sc==="holdout"?"28-day holdout":"rolling 7-day"} scenario. Best value per column in green. MAE and RMSE in ${unit(name)}.'),
    ("<th>Modello</th>", "<th>Model</th>"),
    ("<th>Copertura 80%</th>", "<th>80% coverage</th>"),
    ('<th style="text-align:left">Modello</th><th>WQL relativo</th><th>MASE relativo</th><th>sMAPE medio</th>',
     '<th style="text-align:left">Model</th><th>Relative WQL</th><th>Relative MASE</th><th>Mean sMAPE</th>'),
    ("<th>Serie vinte vs naive</th>", "<th>Series won vs naive</th>"),
    ("<thead><tr><th>Serie</th>", "<thead><tr><th>Series</th>"),
    # identifiers shared with the data (renamed in the English bundle too)
    ('" + calendario"', '" + calendar"'),
    ('"calendario"', '"calendar"'),
    ('"Seasonal Naive (7g)"', '"Seasonal Naive (7d)"'),
]

NAME_EN = {"Righe d'ordine (totale)": "Order lines (total)", "Fatturato netto (totale)": "Net revenue (total)",
           "Righe d'ordine valide": "Valid order lines"}

def series_en(s):
    return NAME_EN.get(s, s.replace("Fatturato netto · ", "Net revenue · "))

def model_en(m):
    return m.replace("Seasonal Naive (7g)", "Seasonal Naive (7d)").replace(" + calendario", " + calendar")

def bundle_en(b):
    b = json.loads(json.dumps(b))
    b["series"] = [series_en(s) for s in b["series"]]
    b["models"] = [model_en(m) for m in b["models"]]
    b["forecasts"] = {model_en(k): v for k, v in b["forecasts"].items()}
    for rows in b["leaderboard"].values():
        for r in rows:
            r["model"] = model_en(r["model"])
    return b

def translate(tpl):
    for it, en in EN:
        assert it in tpl, f"missing in template: {it[:60]}"
        tpl = tpl.replace(it, en)
    return tpl

def page(body, lang, other_lang, other_label):
    switch = f'<a class="lang" href="../{other_lang}/" hreflang="{other_lang}">{other_label}</a>'
    return ("<!doctype html>\n"
            f'<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            "<style>:root{color-scheme:light dark}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>\n"
            "</head>\n<body>\n" + body.replace("<!--LANG-->", switch) + "\n</body>\n</html>\n")

def main():
    docs = ROOT / "docs"
    (docs / "it").mkdir(parents=True, exist_ok=True)
    (docs / "en").mkdir(parents=True, exist_ok=True)

    it_html = TPL.replace("/*DATA*/null", json.dumps(BUNDLE, separators=(",", ":"), ensure_ascii=False))
    (docs / "it" / "index.html").write_text(page(it_html, "it", "en", "English"), encoding="utf-8")

    en_tpl = translate(TPL)
    en_html = en_tpl.replace("/*DATA*/null", json.dumps(bundle_en(BUNDLE), separators=(",", ":"), ensure_ascii=False))
    (docs / "en" / "index.html").write_text(page(en_html, "en", "it", "Italiano"), encoding="utf-8")

    (docs / "index.html").write_text("""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Timestral Forecast Lab</title>
<script>location.replace((navigator.language || "en").toLowerCase().startsWith("it") ? "it/" : "en/");</script>
<style>body{font:16px system-ui,sans-serif;display:grid;place-items:center;min-height:90vh;margin:0;padding:0 16px}a{margin:0 8px}</style>
</head><body><p>Timestral Forecast Lab · <a href="it/">Italiano</a> · <a href="en/">English</a></p></body></html>
""", encoding="utf-8")
    print("built docs/index.html, docs/it/index.html, docs/en/index.html")

if __name__ == "__main__":
    main()
