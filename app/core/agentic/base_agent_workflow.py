from abc import abstractmethod

from langgraph.graph import StateGraph


class BaseAgentWorkflow:

    @abstractmethod
    def build_edges(self, graph: StateGraph):
        """
        This must be implemented by the subclass. It builds the edges for the workflow.

        Add the edges to the graph.

        E.g.

        graph.add_edge("START", "agent_1_key")
        graph.add_edge("agent_1_key", "END")
        return graph
        """
        pass
