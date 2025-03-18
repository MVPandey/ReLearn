from fastapi import APIRouter
from pydantic import BaseModel

from app.schema.langgraph.example_state import ExampleState
from app.services.agent_service import AgentService

router = APIRouter(prefix="/agents", tags=["agents"])


class ExampleAgentRequest(BaseModel):
    """
    Request for the example agent.
    """

    area_of_interest: str


@router.post("/example")
async def example_agent(request: ExampleAgentRequest) -> ExampleState:

    initial_state = ExampleState(area_of_interest=request.area_of_interest)
    result = await AgentService.invoke(initial_state)
    return result
