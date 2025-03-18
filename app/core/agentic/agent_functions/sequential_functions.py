from app.schema.llm.message import Message
from app.schema.langgraph.example_state import ExampleState
from app.schema.langgraph.agents.agent_outputs import (
    SequentialAgentOneOutput,
    SequentialAgentTwoOutput,
)
from app.core.agentic.base_agent_function import BaseAgentFunction
from app.services.llm_service import LLMService


class SequentialAgentPrompts:

    SEQUENTIAL_FUNCTION_1_PROMPT = """Given an area of interest by a user, pick an interesting topic related to the area of interest.

    Area of interest: {area_of_interest}

    Return your response as a JSON object with the following fields:
    - topic: The topic that you chose

    DO NOT include any other text in your response. Respond only with the JSON object, without any markdown formatting.
"""

    SEQUENTIAL_FUNCTION_2_PROMPT = """Given two subtopics and an argument for each, choose the more interesting subtopic.

    Subtopic 1: {subtopic_1}
    Argument 1: {argument_1}

    Subtopic 2: {subtopic_2}
    Argument 2: {argument_2}

    Return your response as a JSON object with the following fields:
    - chosen_subtopic: The subtopic that you chose
    - justification: The justification for the chosen subtopic
    DO NOT include any other text in your response. Respond only with the JSON object, without any markdown formatting.
"""


class SequentialAgentFunctions(BaseAgentFunction):

    def add_mappings(self):
        return {
            self.sequential_function_1_key(): self.sequential_function_1,
            self.sequential_function_2_key(): self.sequential_function_2,
        }

    @staticmethod
    async def sequential_function_1(state: ExampleState):
        llm_service = LLMService()
        prompt = Message(
            role="user",
            content=SequentialAgentPrompts.SEQUENTIAL_FUNCTION_1_PROMPT.format(
                area_of_interest=state.area_of_interest
            ),
        )
        response_dict = await llm_service.query_llm(prompt, json_response=True)
        response = SequentialAgentOneOutput.model_validate(response_dict)
        return {"sequential_agent_one_output": response}

    @staticmethod
    async def sequential_function_2(state: ExampleState):
        llm_service = LLMService()
        prompt = Message(
            role="user",
            content=SequentialAgentPrompts.SEQUENTIAL_FUNCTION_2_PROMPT.format(
                subtopic_1=state.parallel_agent_one_output.subtopic,
                argument_1=state.parallel_agent_one_output.argument,
                subtopic_2=state.parallel_agent_two_output.subtopic,
                argument_2=state.parallel_agent_two_output.argument,
            ),
        )
        response_dict = await llm_service.query_llm(prompt, json_response=True)
        response = SequentialAgentTwoOutput.model_validate(response_dict)
        return {"sequential_agent_two_output": response}

    @staticmethod
    def sequential_function_1_key():
        return SequentialAgentFunctions.sequential_function_1.__name__

    @staticmethod
    def sequential_function_2_key():
        return SequentialAgentFunctions.sequential_function_2.__name__
