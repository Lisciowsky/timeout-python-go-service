# Python Standard
import time
import json
from typing import Union

# Third Party
import uvicorn
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Local
import models
from exponea import entrypoint

description = """
### Exponea Software Engineer assignment Fast Api Server 🚀
"""


app = FastAPI(
    title="Dummy exponea request Server",
    description=description,
    version="0.0.1",
    contact={
        "name": "Any queries? Feel free to contact the developer!",
        "dev": "Jakub",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.post(
    "/api/smart",
    tags=["Get Exponea response/s"],
    response_model=models.ExponeaSuccessReponse,
)
async def exponea(request: Request):
    """
    performs up to 3 HTTP requests to the Exponea Testing HTTP Server
    and returns the first successful response.
    ● Instead of firing all 3 requests at once, the endpoint fires only a single request at the
    beginning.
    ○ If there is a successful response within 300 milliseconds, the endpoint returns
    this response and doesn’t fire other requests.
    ○ If there is no successful response within 300 milliseconds, it fires another 2
    requests. Then it returns the first successful response from any of the 3
    requests (including the first one).
    """
    body = await request.body()
    timeout = json.loads(body)["timeout"]
    result = await entrypoint(timeout=timeout)
    # quick fix :)
    if isinstance(result, models.ExponeaErrorResponse):
        return Response(
            content=json.dumps({"error": {"message": result.message}}),
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    return result


@app.get("/", tags=["Documentation"])
def documentation(request: Request):
    return {
        "documentation": str(request.url) + "docs",
    }


# for testing
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
    )
