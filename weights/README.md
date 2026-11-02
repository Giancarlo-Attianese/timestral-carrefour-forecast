# Model weights / Pesi del modello

**EN** — Download `config.json` and `model.safetensors` for one or more Timestral sizes from Hugging Face and put each pair in its own folder:

```
weights/
├── Timestral-28M/
│   ├── config.json
│   └── model.safetensors
└── Timestral-209M/        (optional, any size works)
    ├── config.json
    └── model.safetensors
```

| Size | Hugging Face | Weights (fp32) |
|---|---|---|
| 5M | [mistralai/Timestral-5M](https://huggingface.co/mistralai/Timestral-5M) | 21 MB |
| 28M | [mistralai/Timestral-28M](https://huggingface.co/mistralai/Timestral-28M) | 111 MB |
| 123M | [mistralai/Timestral-123M](https://huggingface.co/mistralai/Timestral-123M) | 490 MB |
| 209M | [mistralai/Timestral-209M](https://huggingface.co/mistralai/Timestral-209M) | 837 MB |

`src/run_timestral.py` runs every size it finds here. The weights are not in the repository: they are released by Mistral AI under a Modified MIT license.

**IT** — Scarica `config.json` e `model.safetensors` di una o più taglie di Timestral da Hugging Face (link nella tabella) e metti ogni coppia in una cartella a sé, come nello schema sopra. `src/run_timestral.py` esegue tutte le taglie che trova qui. I pesi non sono nel repository: sono distribuiti da Mistral AI con licenza MIT modificata.
