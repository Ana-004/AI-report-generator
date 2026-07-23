from abc import ABC, abstractmethod

import PipelineState

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

    @abstractmethod
    def run(self, state: PipelineState) -> PipelineState:
        pass
