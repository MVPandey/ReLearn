from pydantic import BaseModel, Field


class AgentState(BaseModel):
    """
    State for the agent.
    """

    agent_1_output: str | None = Field(
        default=None, description="The output of agent 1"
    )
    agent_2_output: str | None = Field(
        default=None, description="The output of agent 2"
    )
    agent_3_output: str | None = Field(
        default=None, description="The output of agent 3"
    )
