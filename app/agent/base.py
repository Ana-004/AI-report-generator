from abc import ABC, abstractmethod
from app.llm.factory import LLMFactory
from app.state import PipelineState

class BaseAgent(ABC):
    """
    Every agent implements run(state) -> state 
    Reads or writes the shared PipelineState. 
    Keeping the interface this narrow is what 
    lets the Orchestrator chain agents together,
    reorder them, or swap one out, without touching
    the others.
    """

    name: str = "base_agent"

    def __init__(self, model: str | None = None):

        self.model = model

        self.llm = LLMFactory(
            model=model
        ).create()

    @abstractmethod
    def run(self, state: PipelineState) -> PipelineState:
        pass
