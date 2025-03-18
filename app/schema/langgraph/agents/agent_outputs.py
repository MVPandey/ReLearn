from pydantic import BaseModel


class AgentState(BaseModel):
    """
    State for the agent.
    """

    pass


class SequentialAgentOneOutput(AgentState):
    """
    The output of the first sequential agent.
    """

    topic: str | None = None


class SequentialAgentTwoOutput(AgentState):
    """
    The output of the second sequential agent.
    """

    chosen_subtopic: str | None = None
    justification: str | None = None


class ParallelAgentOutput(AgentState):
    """
    The output of the first parallel agent.
    """

    subtopic: str | None = None
    argument: str | None = None
