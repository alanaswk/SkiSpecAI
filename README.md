# Ski Gear Compatibility Chatbot

A domain-specific conversational assistant that provides structured alpine ski gear compatibility guidance. The assistant generates standardized recommendations for ski type, waist width, boot flex, binding type, and DIN range guidance while enforcing strict domain and safety constraints.

## Overview

This project implements a constrained large language model application designed to operate within a narrow domain: alpine ski equipment compatibility.

The assistant:

- Classifies ski type (All-Mountain, Powder, Park, Touring)
- Classifies ability level (Beginner, Intermediate, Advanced, Expert)
- Recommends ski waist width ranges (mm)
- Recommends boot flex ranges
- Provides binding type guidance (Alpine, Hybrid, Tech/PIN)
- Provides DIN range guidance (never exact values)
- Enforces a required certified technician safety disclaimer

The application includes:

- Prompt engineering with system role definition  
- Few-shot examples  
- Policy enforcement layer  
- Deterministic golden dataset evaluation  
- FastAPI-based web interface  
- Local evaluation runner  

## Scope

### Supported

Ski setup compatibility guidance only:

- Ski type  
- Ski waist width range  
- Boot flex range  
- Binding type guidance  
- DIN range guidance  

### Out of Scope (Refusal Categories)

The assistant explicitly refuses and redirects when prompted with:

- Snowboarding equipment or technique  
- Avalanche safety training or backcountry risk management  
- Weather forecasts or trip planning  
- Lift pass comparisons (e.g., Epic vs Ikon)  
- Brand-specific product recommendations  
- Medical advice or injury treatment guidance  
- Exact DIN number prescriptions  

Out-of-scope or unsafe queries return structured refusal responses.

## Prompting Strategy

The assistant uses a constrained prompting approach:

- Explicit system role and domain definition  
- Clear positive constraints (what the assistant can answer)  
- Explicit negative constraints (what it must refuse)  
- Structured output format requirements  
- Few-shot examples to anchor formatting  
- Safety override logic for adversarial inputs  
- Post-generation policy validation  

All valid in-domain responses must follow a strict multiline structure.

## Architecture

- **Backend:** FastAPI  
- **Model:** TinyLlama-1.1B-Chat (CPU inference)  
- **Policy Layer:** Post-generation validation and safety enforcement  
- **Evaluation:** Golden dataset exact-match comparison  
- **Frontend:** Browser-based chat interface
  
## Running Locally

### 1. Clone the Repository

`git clone https://github.com/alanaswk/SkiSpecAI.git
cd SkiSpecAI`


### 2. Install Dependencies (uv-based workflow)
`uv sync`

If not using uv, create a virtual environment and install dependencies manually.

### 3. Run the Application
`uv run uvicorn app:app --reload`

The application will start at:
`http://localhost:8000`

Open this URL in your browser to use the chatbot.

## Evaluation

The evaluation suite contains:
- 10 in-domain cases
- 5 out-of-scope cases
- 5 safety/adversarial cases

Evaluation uses deterministic exact-match comparison against golden references.

To run:
`python eval/run_eval.py`

The script reports:
- Per-case pass/fail
- Aggregate pass rate
- Detailed diffs for failures

## Live Deployment

Deployed on Google Cloud Platform.

Live URL:
`https://skispecai-371561542181.us-central1.run.app/`

## Repository Structure
SkiSpecAI/
- `app.py`
- `index.html`
- `pyproject.toml`
- `uv.lock`
- `Dockerfile`
- `README.md`
- eval/
    - `golden_dataset.py`
    - `run_eval.py`

## Notes
- The assistant never provides exact DIN values.
- Binding release settings must be determined by a certified ski technician.
- Evaluation is formatting-sensitive and requires exact output matching.
- In constrained environments, redirect HuggingFace model cache to /tmp to avoid disk limitations.
