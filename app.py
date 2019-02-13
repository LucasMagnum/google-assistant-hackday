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
              "expectUserResponse": true,
              "expectedInputs": [
                {
                  "inputPrompt": {
                    "richInitialPrompt": {
                      "items": [
                        {
                          "basicCard": {
                            "title": "Title: this is a title",
                            "subtitle": "This is a subtitle",
                            "formattedText": "This is a basic card.  Text in a basic card can include \"quotes\" and\n        most other unicode characters including emoji 📱.  Basic cards also support\n        some markdown formatting like *emphasis* or _italics_, **strong** or\n        __bold__, and ***bold itallic*** or ___strong emphasis___ as well as other\n        things like line  \nbreaks",
                            "image": {
                              "url": "https://example.com/image.png",
                              "accessibilityText": "Image alternate text"
                            },
                            "buttons": [
                              {
                                "title": "This is a button",
                                "openUrlAction": {
                                  "url": "https://assistant.google.com/"
                                }
                              }
                            ],
                            "imageDisplayOptions": "CROPPED"
                          }
                        }
                      ]
                    }
                  },
                  "possibleIntents": [
                    {
                      "intent": "actions.intent.TEXT"
                    }
                  ]
                }
              ],
              "conversationToken": "{\"data\":{}}",
              "userStorage": "{\"data\":{}}"
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
