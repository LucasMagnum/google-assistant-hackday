import logging
import os

from sanic import Sanic, response

app = Sanic()

logger = logging.getLogger(__name__)


@app.route("/", methods=["POST", "GET"])
async def space(request):
    return response.json({
        "text": "The space has grown 10% last year"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv('PORT', 8000)
)
