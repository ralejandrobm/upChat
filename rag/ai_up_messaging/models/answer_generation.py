import logging
from odoo import models, api

from langchain_core.documents import Document


_logger = logging.getLogger(__name__)


class AiupAnswerGeneration(models.Model):
    _name = "ai_up.answer.generation"
    _description = "AI up Answer Generation"

    @api.model
    def generate_answer(self, *, from_phone: str, message: str) -> list[str]:
        _logger.info(f"[✅][] Generating answer for: +{from_phone}: {message}")

        # TODO: Improve the process of generating the answer
        # 1. Generate a complete question to search
        # 2. Improve the search process
        # 3. Use RAG to generate the answer
        # 4. Format correctly the answer to be used in whatsapp

        related_documents: list[Document] = self.env[
            "ai_up.advertisement"
        ].similarity_search(
            query=message,
        )

        answer = self.env["ai_up.openai.llm"].generate_final_answer(
            question=message,
            related_documents=related_documents,
        )

        return [answer]
