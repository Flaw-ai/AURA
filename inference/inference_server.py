from fastapi import FastAPI
from pydantic import BaseModel
from modeling.generation_flaw import (FlawGenerator, FlawGenerationConfig)
from modeling.modeling_flaw import (FlawForCausalLM)
from transformers import AutoTokenizer

app = FastAPI()

MODEL_PATH = "models/flaw"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = FlawForCausalLM.from_pretrained(MODEL_PATH)
generator = FlawGenerator(model, tokenizer)

class GenerationRequest(BaseModel):
    prompt: str
    mode: str = "chat"
    max_new_tokens: int = 256


@app.get("/")
def root():
    return {
        "model": "FLAW",
        "status": "online"
    }


@app.post("/generate")
def generate(request: GenerationRequest):
    config = FlawGenerationConfig(
        max_new_tokens=
        request.max_new_tokens
    )
    response = generator.generate(
        text=request.prompt,
        mode=request.mode,
        config=config
    )

    return {
        "response": response
    }