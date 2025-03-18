from app.schema.llm.message import Message
from app.schema.langgraph.example_state import ExampleState
from app.schema.langgraph.agents.agent_outputs import ParallelAgentOutput
from app.core.agentic.base_agent_function import BaseAgentFunction
from app.services.llm_service import LLMService


class ParallelAgentPrompts:

    PARALLEL_FUNCTIONS_PROMPT = """Given the following topic, choose ONE interesting subtopic and provide an argument as to why that subtopic is interesting.

    Topic: {topic}


    Return your response as a JSON object with the following fields:
    - subtopic: The subtopic that you chose
    - argument: The argument as to why that subtopic is interesting

    DO NOT include any other text in your response. Respond only with the JSON object, without any markdown formatting.
    """


class ParallelAgentFunctions(BaseAgentFunction):

    def add_mappings(self):
        return {
            self.parallel_function_1_key(): self.parallel_function_1,
            self.parallel_function_2_key(): self.parallel_function_2,
        }

    @staticmethod
    async def parallel_function_1(state: ExampleState):
        llm_service = LLMService()
        prompt = Message(
            role="user",
            content=ParallelAgentPrompts.PARALLEL_FUNCTIONS_PROMPT.format(
                topic=state.sequential_agent_one_output.topic
            ),
        )
        response_dict = await llm_service.query_llm(prompt, json_response=True)
        response = ParallelAgentOutput.model_validate(response_dict)
        return {"parallel_agent_one_output": response}

    @staticmethod
    async def parallel_function_2(state: ExampleState):
        llm_service = LLMService()
        prompt = Message(
            role="user",
            content=ParallelAgentPrompts.PARALLEL_FUNCTIONS_PROMPT.format(
                topic=state.sequential_agent_one_output.topic
            ),
        )
        response_dict = await llm_service.query_llm(prompt, json_response=True)
        response = ParallelAgentOutput.model_validate(response_dict)
        return {"parallel_agent_two_output": response}

    @staticmethod
    def parallel_function_1_key():
        return ParallelAgentFunctions.parallel_function_1.__name__

    @staticmethod
    def parallel_function_2_key():
        return ParallelAgentFunctions.parallel_function_2.__name__
