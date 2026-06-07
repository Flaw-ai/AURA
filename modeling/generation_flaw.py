from dataclasses import dataclass
from typing import List
from typing import Optional
from typing import Generator
import torch

@dataclass
class FlawGenerationConfig:
    max_new_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9
    top_k: int = 50
    repetition_penalty: float = 1.1
    do_sample: bool = True
    num_beams: int = 1
    early_stopping: bool = True
    use_cache: bool = True
    stream: bool = False
    stop_strings: Optional[List[str]] = None

class GenerationModes:
    CHAT = "chat"
    TUTOR = "tutor"
    EXAM = "exam"
    SMS = "sms"
    TEACHER = "teacher"
    RAG = "rag"

class PromptTemplates:

    @staticmethod
    def tutor(question):

        return f"""
You are FLAW Tutor.

Explain concepts clearly.

Question:
{question}

Answer:
"""

    @staticmethod
    def exam(question):

        return f"""
You are FLAW Exam Mode.

Provide:

1. Direct Answer
2. Explanation
3. Formula
4. Final Result

Question:
{question}

Answer:
"""

    @staticmethod
    def sms(question):

        return f"""
Provide a concise answer.

Keep response short.

Question:
{question}

Answer:
"""

    @staticmethod
    def teacher(question):

        return f"""
You are an expert teacher.

Teach deeply and accurately.

Question:
{question}

Answer:
"""

    @staticmethod
    def rag(question, context):

        return f"""
Context:

{context}

Question:

{question}

Answer:
"""

class FlawGenerator:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.device = next(model.parameters()).device

    def build_prompt(self, text, mode):
        if mode == GenerationModes.TUTOR:
            return PromptTemplates.tutor(text)

        if mode == GenerationModes.EXAM:
            return PromptTemplates.exam(text)

        if mode == GenerationModes.SMS:
            return PromptTemplates.sms(text)

        if mode == GenerationModes.TEACHER:
            return PromptTemplates.teacher(text)

        return text

    def apply_stop_strings(self, text, stop_strings):
        if not stop_strings:
            return text

        for stop in stop_strings:
            index = text.find(stop)
            if index != -1:
                text = text[:index]

        return text

    @torch.no_grad()
    def generate(self, text, mode=GenerationModes.CHAT, config=None):
        if config is None:
            config = FlawGenerationConfig()

        prompt = self.build_prompt(text, mode)
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        )

        inputs = {
            k: v.to(self.device)
            for k, v in inputs.items()
        }

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=config.max_new_tokens,
            temperature=config.temperature,
            top_p=config.top_p,
            top_k=config.top_k,
            repetition_penalty=config.repetition_penalty,
            do_sample=config.do_sample,
            num_beams=config.num_beams,
            early_stopping=config.early_stopping,
            use_cache=config.use_cache
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        response = self.apply_stop_strings(
            response,
            config.stop_strings
        )

        return response

    @torch.no_grad()
    def batch_generate(self, prompts, mode=GenerationModes.CHAT, config=None):
        outputs = []

        for prompt in prompts:
            outputs.append(self.generate(prompt, mode, config))
        return outputs

    def stream_generate(self, text, mode=GenerationModes.CHAT, config=None) -> Generator[str, None, None]:
        response = self.generate(text, mode, config)
        tokens = response.split()

        for token in tokens:
            yield token + " "

    def generate_hint(self, question):
        prompt = f"""
Provide only a hint.

Do NOT give the answer.

Question:
{question}

Hint:
"""
        return self.generate(prompt)

    def generate_exam_solution(self, question):
        return self.generate(
            question,
            mode=GenerationModes.EXAM
        )

    def generate_sms_response(self, question):
        response = self.generate(question, mode=GenerationModes.SMS)
        return response[:160]

    def generate_with_context(self, question, retrieved_chunks):
        context = "\n\n".join(retrieved_chunks)
        prompt = PromptTemplates.rag(question, context)
        return self.generate(
            prompt,
            mode=GenerationModes.RAG
        )

    def generate_weekly_test(self, topic, questions=5):
        prompt = f"""
Generate {questions}
exam questions on:

{topic}
"""
        return self.generate(prompt)

    def generate_quiz(self, topic, questions=5):
        prompt = f"""
Generate a multiple choice quiz.

Topic:
{topic}

Questions:
{questions}
"""
        return self.generate(prompt)

    def generate_flashcards(self, topic):
        prompt = f"""
Create flashcards.

Topic:
{topic}
"""
        return self.generate(prompt)

    def summarize_notes(self, notes):
        prompt = f"""
Summarize:

{notes}
"""
        return self.generate(prompt)

    def explain_concept(self, concept):

        prompt = f"""
Explain clearly:

{concept}
"""
        return self.generate(
            prompt,
            mode=GenerationModes.TUTOR
        )

    def detect_subject(self, question):
        prompt = f"""
Identify subject.

Question:

{question}

Return one of:

Math
Science
English
History
Computer Science
"""
        return self.generate(prompt)

    def format_output(self, text):
        return text.strip()

    def beam_search_generate(self, *args, **kwargs):
        raise NotImplementedError("Beam Search coming in future.")

    def speculative_generate(self, *args, **kwargs):
        raise NotImplementedError("Speculative decoding coming in future.")

__all__ = [
    "FlawGenerator",
    "FlawGenerationConfig",
    "GenerationModes"
]