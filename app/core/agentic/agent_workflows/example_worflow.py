from langgraph.graph import StateGraph, START, END

from app.schema.langgraph.example_state import ExampleState
from app.core.agentic.base_agent_workflow import BaseAgentWorkflow
from app.core.agentic.agent_functions.sequential_functions import (
    SequentialAgentFunctions as saf,
)
from app.core.agentic.agent_functions.parallel_functions import (
    ParallelAgentFunctions as paf,
)


class ExampleWorkflow(BaseAgentWorkflow):

    @staticmethod
    def run_parallel_functions(state: ExampleState):  # noqa: F821
        return [paf.parallel_function_1_key(), paf.parallel_function_2_key()]

    @staticmethod
    def build_edges(graph: StateGraph):
        graph.add_edge(START, saf.sequential_function_1_key())
        graph.add_conditional_edges(
            saf.sequential_function_1_key(), ExampleWorkflow.run_parallel_functions
        )
        graph.add_edge(paf.parallel_function_1_key(), saf.sequential_function_2_key())
        graph.add_edge(paf.parallel_function_2_key(), saf.sequential_function_2_key())
        graph.add_edge(saf.sequential_function_2_key(), END)
        return graph
