from abc import abstractmethod

from langgraph.graph import StateGraph


class BaseAgentWorkflow:

    @abstractmethod
    def build_edges(self, graph: StateGraph):
        """
        This must be implemented by the subclass. It builds the edges for the workflow.

        Add the edges to the graph.
        """
        pass
