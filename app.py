import logging
import os

from sanic import Sanic, response

from data import ebitda, operating_revenue, average_revenue

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

    text = "Here it is the top companies in regards to %s" % operator
    rows = []

    if operator.lower() == "earnings":
        columns = [
            {
              "header": "Company"
            },
            {
              "header": "EBITDA"
            },
        ]

        rows = [{
          "cells": [
            {
              "text": item["name"]
            },
            {
              "text": item["ebitda"]
            },
          ],
          "dividerAfter": True
        } for item in ebitda]

    elif operator.lower() == "revenue":
        columns = [
            {
              "header": "Company"
            },
            {
              "header": "Revenue"
            },
        ]

        rows = [{
          "cells": [
            {
              "text": item["name"]
            },
            {
              "text": item["operating_revenue"]
            },
          ],
          "dividerAfter": True
        } for item in operating_revenue]

    else:
        columns = [
            {
              "header": "Category"
            },
            {
              "header": "Average"
            },
        ]

        rows = [{
          "cells": [
            {
              "text": item["cat"]
            },
            {
              "text": item["avg_revenue_2017"]
            },
          ],
          "dividerAfter": True
        } for item in average_revenue]


    return {
      "payload": {
        "google": {
          "expectUserResponse": True,
          "richResponse": {
            "items": [
              {
                "simpleResponse": {
                  "textToSpeech": text
                }
              },
              {
                "tableCard": {
                  "rows": rows,
                  "columnProperties": [
                    {
                      "header": "Company"
                    },
                    {
                      "header": "EBITDA"
                    },
                  ]
                }
              }
            ]
          },
          "userStorage": "{\"data\":{}}"
        }
      }
    }


handlers = {
    "top_companies": top_companies
}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT', 8000), debug=True)
