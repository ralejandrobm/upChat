from odoo import http
from odoo.http import Response

import json
import logging
from pydantic import BaseModel, ValidationError, Field

_logger = logging.getLogger(__name__)


class MessageRequestModel(BaseModel):
    # TODO: add validation for phone number
    from_phone: str = Field(..., min_length=7, max_length=15)
    # TODO: add validation to too many characters
    message: str = Field(..., min_length=1)


class AiupWhatsappAnswerConnectorController(http.Controller):
    @http.route(
        "/api/v1/whatsapp/answers",
        type="http",
        auth="public",
        methods=["POST"],
        csrf=False,
    )
    def get_answers(self, **kwargs):
        """
        Get AI generated answers
        """

        # TODO: add authentication
        # TODO: add error handling
        # TODO: add logging
        # TODO: add whatsapp message creation

        try:
            body = json.loads(http.request.httprequest.data)
            message_request = MessageRequestModel(**body)
        except ValidationError as e:
            _logger.error(f"[❌][AiupMessagingController] Error: {e.json()}")
            return Response(
                json.dumps({"status": 400, "error": json.loads(e.json())}),
                mimetype="application/json",
                status=400,
            )

        # TODO: improve permission handling. Should not use sudo!
        answer = (
            http.request.env["ai_up.answer.generation"]
            .sudo()
            .generate_answer(
                from_phone=message_request.from_phone, message=message_request.message
            )
        )

        return Response(
            json.dumps({"status": 200, "data": answer}),
            mimetype="application/json",
            status=200,
        )
