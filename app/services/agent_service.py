from abc import abstractmethod

from langgraph.graph import StateGraph

from app.schema.langgraph.example_state import ExampleState
from app.core.agentic.agent_workflows.example_worflow import ExampleWorkflow
from app.core.agentic.base_agent_function import BaseAgentFunction
from app.core.logger import logger


def build_agent_mappings():
    """
    Builds a dictionary of agent functions using all of the mappings in the subclasses of AgentFunction.
    """
    agent_map: dict = {}

    agent_functions = BaseAgentFunction.__subclasses__()

    for agent_function in agent_functions:
        agent_map.update(agent_function().add_mappings())

    logger.info(f"Agent map: {agent_map}")
    return agent_map


class AgentService:

    @staticmethod
    def graph():
        """
        Builds the graph for the agent.
        """
        graph = StateGraph(state_schema=ExampleState)
        for agent_function_key, agent_function in build_agent_mappings().items():
            graph.add_node(agent_function_key, agent_function)

        graph = ExampleWorkflow.build_edges(graph)
        return graph.compile()

    @staticmethod
    async def invoke(state: ExampleState):
        """
        Invokes the agent.
        """
        return await AgentService.graph().ainvoke(state)
