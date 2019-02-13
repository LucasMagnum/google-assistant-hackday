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
            "fulfillmentMessages": [{
                "listSelect":  {
                    "title": "Top companies - EBTIDA",
                    "items": [{
                        "title": item["name"],
                        "description": item["ebitda"]
                    } for item in ebitda]
                }
            }]
        }

    if operator.lower() == "revenue":
        return {
            "fulfillmentMessages": [{
                "listSelect":  {
                    "title": "Top companies - Operating Revenue",
                    "items": [{
                        "title": item["name"],
                        "description": item["operating_revenue"]
                    } for item in operating_revenue]
                }
            }]
        }


    return {
        "fulfillmentText": "Unable to find the financial operator"
    }


handlers = {
    "top_companies": top_companies
}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT', 8000), debug=True)
