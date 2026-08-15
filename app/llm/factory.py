'''
LLM Factory : Every agent asks this factory for a client instead
of importing a provider SDK directly.

Built on litellm, which exposes one completion() call that works the
same way across every major provider.

This factory just resolves the right model string  and wraps the call
in a small, agent-friendly interface (generate(system, user) -> str)
so agents never touch the underlying SDK response shape.
'''

# To read environment variables
import os 

#LiteLLM provides one unified API for many model providers.
try:
    import litellm  # type: ignore[import-not-found]
except ImportError:
    litellm = None

#LLM provider
DEFAULT_MODELS = {
    "anthropic" : "claude-sonnet-5",
    "openai" : "gpt-40",
    "gemini" : "gemini/gemini-1.5.pro"
}

class LLMClient:
    '''
    thin wrapper around LiteLLM. Agents only ever call generate().
    '''

    def __init__(self, model: str):
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int=2000) -> str:
        #API request
        response = litellm.completion(
            model=self.model,
            max_tokens = max_tokens,
            messages = [
                {"role" : "system", "content" : system_prompt},
                {"role" : "user", "content" : user_prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]

class LLMFactory:

    def __init__(self, provider: str | None = None, model: str | None = None):
        self.provider = provider or os.getenv("LLM_PROVIDER", "anthropic")
        self.model = model or os.getenv("LLM_MODEL") or DEFAULT_MODELS.get(self.provider)
        if not self.model:
            raise ValueError(
                f"Unknown provider '{self.provider}' and no LLM_MODEL set. "
                f"Known providers: {list(DEFAULT_MODELS)}"
            )

    def create(self) -> LLMClient:
        return LLMClient(model=self.model)