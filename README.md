# TinyLlama Web Chat

Web chat interface using the TinyLlama-1.1B model with FastAPI.

## Running

Install dependencies and run:
```bash
uv run uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.

The first run will download the model (~2.2GB).

## API

- `GET /` - Serves the chat UI
- `POST /chat` - Send a message, returns response
- `POST /clear` - Clear session history
