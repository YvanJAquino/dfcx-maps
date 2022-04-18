from json import dumps
from typing import Any, List, Dict, Optional, Union
from pydantic import BaseModel


class SessionInfo(BaseModel):
    session: str
    parameters: Dict[str, Any]


class WebhookRequest(BaseModel):
    detectIntentResponseId: str
    languageCode: str
    text: Optional[Union[str, List[str]]]
    fuilfillmentInfo: Optional[Dict[str, Any]]
    intentInfo: Optional[Dict[str, Any]]
    pageInfo: Optional[Dict[str, Any]]
    sessionInfo: SessionInfo
    messages: Optional[List[Dict[str, Any]]]
    payload: Optional[Dict[str, Any]]
    sentimentAnalysisResult: Optional[Dict[str, Any]]
    query: Optional[Dict[str, Any]]


# if __name__ == '__main__':
#     from rich import print
#     sample = {
#     "detectIntentResponseId": "10c3698f-7f4c-437f-849a-531de54ca796",
#     "pageInfo": {
#         "currentPage": "projects/holy-diver-297719/locations/us-central1/agents/7623161c-adfd-4acc-9de7-66946d751595/flows/00000000-0000-0000-0000-000000000000/pages/928b3fb4-d1c0-4fd1-a254-46fa460373ec",
#         "formInfo": {
#         "parameterInfo": [
#             {
#             "displayName": "count-sweets",
#             "required": True,
#             "state": "FILLED",
#             "value": 1,
#             "justCollected": True
#             }
#         ]
#         }
#     },
#     "sessionInfo": {
#         "session": "projects/holy-diver-297719/locations/us-central1/agents/7623161c-adfd-4acc-9de7-66946d751595/sessions/da0a27-077-9f8-cf7-56abf3b65",
#         "parameters": {
#         "count-sweets": 1,
#         "entity-sweets": "cupcake"
#         }
#     },
#     "fulfillmentInfo": {
#         "tag": "webhook-check-inventory-sweets"
#     },
#     "messages": [
#         {
#         "text": {
#             "text": [
#             "You want 1 of $session.params.entity-sweets.original - no problem, let's check if we've got that in stock.   "
#             ],
#             "redactedText": [
#             "You want 1 of $session.params.entity-sweets.original - no problem, let's check if we've got that in stock.   "
#             ]
#         },
#         "responseType": "HANDLER_PROMPT",
#         "source": "VIRTUAL_AGENT"
#         }
#     ],
#     "text": "1",
#     "languageCode": "en"
#     }
#     model = WebhookRequest(**sample)
#     print(model)
#     print('\t\t\---\n\n\t\t---', )
#     print(model.dict())
#     print(model.sessionInfo.dict()['parameters']['entity-sweets'])
