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
                "items": [
                  {
                    "simpleResponse": {
                      "textToSpeech": "Simple Response"
                    }
                  },
                  {
                    "tableCard": {
                      "rows": [
                        {
                          "cells": [
                            {
                              "text": "row 1 item 1"
                            },
                            {
                              "text": "row 1 item 2"
                            },
                            {
                              "text": "row 1 item 3"
                            }
                          ],
                          "dividerAfter": True
                        },
                        {
                          "cells": [
                            {
                              "text": "row 2 item 1"
                            },
                            {
                              "text": "row 2 item 2"
                            },
                            {
                              "text": "row 2 item 3"
                            }
                          ],
                          "dividerAfter": True
                        }
                      ],
                      "columnProperties": [
                        {
                          "header": "header 1"
                        },
                        {
                          "header": "header 2"
                        },
                        {
                          "header": "header 3"
                        }
                      ]
                    }
                  }
                ]
              },
              "userStorage": "{\"data\":{}}"
            }
          }
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
