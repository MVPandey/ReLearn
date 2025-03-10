import json
from openai import AsyncOpenAI
from openai.types.chat.chat_completion import ChatCompletion

from app.config.config import app_settings
from app.schema.llm.message import Message
from app.core.exceptions import LLMException
from app.core.logger import logger


class LLMService:
    def __init__(
        self,
        base_url: str = app_settings.LLM_API_BASE_URL,
        api_key: str = app_settings.LLM_API_KEY,
        model_name: str = app_settings.LLM_MODEL_NAME,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.model_name = model_name

    def _client(self) -> AsyncOpenAI:
        return AsyncOpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    async def query_llm(
        self,
        messages: Message | list[Message],
        json_response: bool = False,
        **kwargs,
    ) -> Message:
        client = self._client()

        if isinstance(messages, Message):
            messages = [messages]

        try:
            logger.debug(f"Querying LLM with latest message: {messages[-1]}")
            completion: ChatCompletion = await client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                response_format={"type": "json_object"} if json_response else None,
                **kwargs,
            )
            logger.debug(f"LLM response: {completion}")
            logger.info(
                f"Query LLM completed with status {completion.choices[0].finish_reason}"
            )
            return (
                json.loads(completion.choices[0].message.content)
                if json_response
                else completion.choices[0].message
            )
        except json.JSONDecodeError as e:
            error_message = f"Failed to parse JSON response: {e}\n\nResponse: {completion.choices[0].message.content}"
            logger.error(error_message)
            raise LLMException(error_message) from e
        except Exception as e:
            error_message = f"Failed to query LLM: {e}"
            logger.error(error_message)
            raise LLMException(error_message) from e
