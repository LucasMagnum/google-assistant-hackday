import logging
import os

from sanic import Sanic, response

from data import ebitda, operating_revenue

app = Sanic()

logger = logging.getLogger(__name__)


@app.route("/", methods=["POST", "GET"])
async def handler(request):
    print("Request received", request.json)

    action_type = request.json["queryResult"]["parameters"]["action_type"]

    handler = handlers.get(action_type)

    if handler:
        return response.json(handler(request.json["queryResult"]["parameters"]))

    return response.json({
        "fulfillmentText": "Sorry we are unable to process with your request"
    })


def top_companies(parameters):
    operator = parameters["operator"]

    if operator.lower() == "earnings":
        return {
          "payload": {
            "google": {
              "expectUserResponse": True,
              "richResponse": {
                "items": []
              },
              "userStorage": "{\"data\":{}}",
              "systemIntent": {
                "intent": "actions.intent.OPTION",
                "data": {
                  "@type": "type.googleapis.com/google.actions.v2.OptionValueSpec",
                  "listSelect": {
                    "title": "List Title",
                    "items": [
                      {
                        "optionInfo": {
                          "key": "SELECTION_KEY_ONE",
                          "synonyms": [
                            "synonym 1",
                            "synonym 2",
                            "synonym 3"
                          ]
                        },
                        "description": "This is a description of a list item.",
                        "image": {
                          "url": "IMG_URL_AOG.com",
                          "accessibilityText": "Image alternate text"
                        },
                        "title": "Title of First List Item"
                      },
                      {
                        "optionInfo": {
                          "key": "SELECTION_KEY_GOOGLE_HOME",
                          "synonyms": [
                            "Google Home Assistant",
                            "Assistant on the Google Home"
                          ]
                        },
                        "description": "Google Home is a voice-activated speaker powered by the Google Assistant.",
                        "image": {
                          "url": "IMG_URL_GOOGLE_HOME.com",
                          "accessibilityText": "Google Home"
                        },
                        "title": "Google Home"
                      },
                      {
                        "optionInfo": {
                          "key": "SELECTION_KEY_GOOGLE_PIXEL",
                          "synonyms": [
                            "Google Pixel XL",
                            "Pixel",
                            "Pixel XL"
                          ]
                        },
                        "description": "Pixel. Phone by Google.",
                        "image": {
                          "url": "IMG_URL_GOOGLE_PIXEL.com",
                          "accessibilityText": "Google Pixel"
                        },
                        "title": "Google Pixel"
                      }
                    ]
                  }
                }
              }
            }
          },
          "outputContexts": [
            {
              "name": "/contexts/_actions_on_google",
              "lifespanCount": 99,
              "parameters": {
                "data": "{}"
              }
            }
          ]
        }

    if operator.lower() == "revenue":
        return {
            "fulfillmentText": "Top companies - revenue",
            "fulfillmentMessages": [{
                "listSelect":  {
                    "title": "Top companies - Operating Revenue",
                    "items": [{
                        "title": item["name"],
                        "description": item["operating_revenue"]
                    } for item in operating_revenue]
                }
            }],
            "source": "Motherbrain"
        }


    return {
        "fulfillmentText": "Unable to find the financial operator"
    }


handlers = {
    "top_companies": top_companies
}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT', 8000), debug=True)
