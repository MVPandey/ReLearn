from abc import abstractmethod

from langgraph.graph import StateGraph

from app.schema.langgraph.agent_state import AgentState


class AgentFunction:

    @abstractmethod
    def add_mappings(self):
        """
        This must be implemented by the subclass. It maps the function name to the function.

        E.g.

        def add_mappings(self):
            return {
                "function_name": self.function,
            }
        """
        pass


def build_agent_mappingss():
    """
    Builds a dictionary of agent functions using all of the mappings in the subclasses of AgentFunction.
    """
    agent_map: dict = {}

    agent_functions = AgentFunction.__subclasses__()

    for agent_function in agent_functions:
        agent_map.update(agent_function().add_mappings())

    return agent_map


class AgentService:
    def __init__(self, state: AgentState):
        self.agent_map = build_agent_mappingss()
        self.state = state

    @property
    def graph(self):
        """
        Builds the graph for the agent.
        """

        graph = StateGraph(self.state)
        for agent_key, agent_function in self.agent_map.items():
            graph.add_node(agent_key, agent_function)

        return graph
