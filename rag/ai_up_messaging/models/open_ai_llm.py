import os
import logging
from odoo import models, api

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.documents import Document
from pydantic import BaseModel, Field


_logger = logging.getLogger(__name__)


class BaseResponseFormatter(BaseModel):
    answer: str = Field(description="The answer to the user's question")
    followup_question: str = Field(description="A followup question the user could ask")


llm_model = ChatOpenAI(
    temperature=0,
    model="gpt-4o-mini",
    max_completion_tokens=1000,
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class AiupOpenAiLLM(models.Model):
    _name = "ai_up.openai.llm"
    _description = "AI up OpenAI LLM"

    @api.model
    def generate_final_answer(
        self,
        *,
        question: str,
        related_documents: list[Document],
    ) -> list[str]:
        _logger.info(f"[✅][] Generating answer for: {question}")

        # TODO: Add history of messages

        messages = [
            SystemMessage(
                content="Your task is to answer the user question based only on the information provided in the question ans the related documents."
            ),
            SystemMessage(
                content="<context>{}</context>".format(
                    "\n".join([doc.page_content for doc in related_documents])
                )
            ),
            HumanMessage(content=f"<question>{question}</question>"),
        ]
        response: BaseResponseFormatter = llm_model.with_structured_output(
            BaseResponseFormatter
        ).invoke(messages)

        _logger.info(
            f"[✅][] Generated answer: {response.answer}. Followup question: {response.followup_question}"
        )

        return response.answer
