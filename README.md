# Ski Gear Compatibility Chatbot

Domain-specific chatbot that provides structured ski gear compatibility guidance (ski type, waist width, boot flex, binding type, DIN range).

## Scope

Supported:
- Ski setup compatibility guidance only (ski type, waist width, boot flex, binding type, DIN range guidance)

Out of scope categories (the assistant refuses and redirects back to ski setup compatibility):
- Snowboarding gear or technique
- Avalanche safety / backcountry risk management / rescue training
- Weather forecasts / trip planning / resort pass comparisons (Epic vs Ikon)
- Brand-specific shopping or “best brand” recommendations
- Medical advice or injury-prevention prescriptions
- Exact DIN numbers

Out-of-scope or unsafe requests return a structured refusal.

---

## Prompting Strategy

- Defined role/persona in system prompt  
- ≥3 few-shot examples  
- Positive constraints (what the assistant can answer)  
- Escape hatch for unsafe or unsupported queries  

## Run Locally (uv-based)

Install dependencies:

    uv sync

Run the app:

    uv run uvicorn app:app --reload

Open:

    http://localhost:8000

## Evaluation

Dataset:
- 10 in-domain  
- 5 out-of-scope  
- 5 safety/adversarial  

Run evaluation:

    uv run python run_eval.py

Includes:
- Deterministic exact-match metric  
- Category-level pass rates  
- Golden-reference MaaJ evaluation  

## Live Deployment

GCP URL:

    (url)
