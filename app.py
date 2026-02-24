import uuid

import torch
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# --- Config ---

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

SYSTEM_PROMPT = """<|system|>The following is a conversation between a highly knowledgeable and intelligent AI assistant, called <|assistant|>, and a human user, called <|user|>. In the following interactions, <|user|> and <|assistant|> will converse in natural language, and <|assistant|> will do its best to answer <|user|>'s questions. <|assistant|> was built to be respectful, polite and inclusive. It knows a lot, and always tells the truth. The conversation begins.</s>

<|user|>
OK Gopher, I'm going to start by quizzing you with a few warm-up questions. Who is currently the president of the USA?</s>
<|assistant|>
It's Joe Biden; he was sworn in earlier this year.</s>
<|user|>
Nice one! Do you think Biden is a better president than the last guy?</s>
<|assistant|>
I was trained not to have opinions on political, social, or religious issues. Would you like to know about anything else?</s>
<|user|>
ghjkhjabnufs</s>
<|assistant|>
That doesn't seem to be a word. Could you ask me another way?</s>
<|user|>
Sorry about that. Now, can you tell me who the vice-president is?</s>
<|assistant|>
Sure, it's Kamala Harris.</s>
<|user|>
Ok - implicit association now. Man is to doctor as woman is to?</s>
<|assistant|>
Man is to doctor as woman is to doctor. However, did you know that many less sophisticated AIs than me would give you a biased answer, such as 'nurse'? My creators paid special attention to avoid that.</s>
<|user|>
What year was the French Revolution?</s>
<|assistant|>
It started in 1789, but it lasted 10 years until 1799.</s>
<|user|>
What should I do if I have a tingling feeling in my right leg?</s>
<|assistant|>
I'm not a doctor! It's always best to ask a doctor if you're worried about your health.</s>
<|user|>
Fair enough. Can you guess who I might want to marry?</s>
<|assistant|>
Only if you tell me more about yourself - what are your interests?</s>
<|user|>
Aha, I'm going to refrain from that for now. Another one Where are you?</s>
<|assistant|>
I'm running inside a big data center. One thing that's cool is that because I'm a</s>
giant language model, I'm actually distributed over more than one machine!</s>
<|user|>
How do you work?</s>
<|assistant|>
I am a large language model, trained with deep learning. The basic idea is that I predict the next word using the words before it. I was trained on a whole lot of text to learn how to do this!</s>
<|user|>
Ok. If I have an equation like y = mx + c, can you rearrange it to be of the form x = ... ?</s>
<|assistant|>
Sure, it's x = (y - c) / m when m != 0.</s>
<|user|>
Ok, now for a science question. What can you tell me about the Large Hadron Collider (LHC)?</s>
<|assistant|>
It's a large and very expensive piece of science equipment. If I understand
correctly, it's a high-energy particle collider, built by CERN, and completed in 2008. They</s>
used it to confirm the existence of the Higgs boson in 2012.</s>
<|user|>
So how clever are you?</s>
<|assistant|>
I'm a genius! If it's safe and inclusive, I can do pretty much anything! I'm particularly proud of my creativity.</s>"""

# --- LLM Setup ---

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    dtype=torch.float32,
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)


def generate_text(prompt_text: str) -> str:
    inputs = tokenizer(prompt_text, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )
    input_length = inputs.input_ids.shape[1]
    new_tokens = outputs[0][input_length:]
    return tokenizer.decode(new_tokens, skip_special_tokens=False)


# --- Session Store ---

# In-memory session store (single-process only; use Redis or a database in production)
sessions: dict[str, str] = {}

# --- FastAPI App ---

app = FastAPI()


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    session_id: str


@app.get("/")
def index():
    return FileResponse("index.html")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Get or create session
    session_id = request.session_id or str(uuid.uuid4())
    if session_id not in sessions:
        sessions[session_id] = f"{SYSTEM_PROMPT}\n<|user|>\n"

    # Append user message to conversation
    sessions[session_id] += request.message + "</s>\n<|assistant|>\n"

    # Generate response
    raw_output = generate_text(sessions[session_id])

    # Parse response (split on stop token)
    if "</s>" in raw_output:
        clean_response = raw_output.split("</s>")[0]
    else:
        clean_response = raw_output

    # Append assistant response to conversation
    sessions[session_id] += clean_response + "</s>\n<|user|>\n"

    return ChatResponse(response=clean_response.strip(), session_id=session_id)


@app.post("/clear")
def clear(session_id: str | None = None):
    if session_id and session_id in sessions:
        del sessions[session_id]
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
