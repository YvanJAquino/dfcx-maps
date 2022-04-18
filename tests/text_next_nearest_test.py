from rich import print
from httpx import Client

url = 'https://dfcx-va-qhlbuanwca-uk.a.run.app'
payload = {
  "detectIntentResponseId": "15c90aba-30c8-4da1-8f0d-df79d329bb41",
  "intentInfo": {
    "lastMatchedIntent": "projects/oktony-cx/locations/global/agents/ac6097e1-89fc-40fc-87c7-8d7bde8bdafc/intents/5fcb0afe-b1bf-481c-92a1-15da07fcf1cf",
    "parameters": {
      "phone-number": {
        "originalValue": "717-422-1563",
        "resolvedValue": "7174221563"
      }
    },
    "displayName": "Provide-phone-number",
    "confidence": 1
  },
  "pageInfo": {
    "currentPage": "projects/oktony-cx/locations/global/agents/ac6097e1-89fc-40fc-87c7-8d7bde8bdafc/flows/00000000-0000-0000-0000-000000000000/pages/1272e223-e1ae-480f-869b-5911e1b1ec34"
  },
  "sessionInfo": {
    "session": "projects/oktony-cx/locations/global/agents/ac6097e1-89fc-40fc-87c7-8d7bde8bdafc/environments/-/sessions/081G3Ku3cLZRhCuCUwafiExMQ",
    "parameters": {
      "phone-number": "7862511624",
      "zip-code": "20166"
    }
  },
  "fulfillmentInfo": {
    "tag": "text"
  },
  "messages": [
    {
      "text": {
        "text": [
          "Thank you, the facility address has been sent to 7174221563.\nWould you like to schedule an appointment? "
        ],
        "redactedText": [
          "Thank you, the facility address has been sent to 7174221563.\nWould you like to schedule an appointment? "
        ]
      },
      "responseType": "ENTRY_PROMPT",
      "source": "VIRTUAL_AGENT"
    }
  ],
  "payload": {
    "telephony": {
      "caller_id": "+17145854165"
    }
  },
  "transcript": "My phone number is 717-422-1563.",
  "languageCode": "en-us"
}

# timeout = httpx.Timeout(10)
with Client(base_url=url, timeout=10) as c:
    r = c.post('/text_next_nearest', json=payload)
    print(r)
    print(r.json())