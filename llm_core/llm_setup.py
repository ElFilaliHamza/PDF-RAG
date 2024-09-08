from groq import Groq
from typing import Any, Iterator
from pydantic import Field
import os

from llama_index.core.llms import CustomLLM, CompletionResponse, LLMMetadata
from llama_index.core.llms.callbacks import llm_completion_callback
from llama_index.core import Settings


class GroqLLM(CustomLLM):
    context_window: int = 32768
    num_output: int = 4096
    model_name: str = "mixtral-8x7b-32768"
    client: Groq = Field(
        default_factory=lambda: Groq(api_key=os.getenv("GROQ_API_KEY"))
    )

    @property
    def metadata(self) -> LLMMetadata:
        return LLMMetadata(
            context_window=self.context_window,
            num_output=self.num_output,
            model_name=self.model_name,
        )

    @llm_completion_callback()
    def complete(self, prompt: str, **kwargs: Any) -> CompletionResponse:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_name,
        )
        return CompletionResponse(text=response.choices[0].message.content)

    @llm_completion_callback()
    def stream_complete(
        self, prompt: str, **kwargs: Any
    ) -> Iterator[CompletionResponse]:
        full_response = self.complete(prompt, **kwargs)
        for char in full_response.text:
            yield CompletionResponse(text=char, delta=char)

groq_llm = GroqLLM()
Settings.llm = groq_llm
Settings.embed_model = "local:BAAI/bge-base-en-v1.5" 
