from pydantic import BaseModel

from app.schema.langgraph.agents.agent_outputs import (
    SequentialAgentOneOutput,
    SequentialAgentTwoOutput,
    ParallelAgentOutput,
)


class ExampleState(BaseModel):
    """
    State for the example.
    """

    area_of_interest: str | None = None
    sequential_agent_one_output: SequentialAgentOneOutput | None = None
    parallel_agent_one_output: ParallelAgentOutput | None = None
    parallel_agent_two_output: ParallelAgentOutput | None = None
    sequential_agent_two_output: SequentialAgentTwoOutput | None = None
