import exceptions
import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from fastapi import FastAPI, Response, status

app = FastAPI()


@app.get("/tag")
async def get_tags(response: Response, starting_with: str = ''):
    try:
        return await services.get_tags_by_starting_string(starting_with)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/tag/{name}/inc")
async def inc_tag(name: str, response: Response):
    try:
        await services.inc_tag(name)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/tags/inc")
async def inc_tags(names: list[str], response: Response):
    try:
        await services.inc_tags(names)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/tag/{name}/dec")
async def dec_tag(name: str, response: Response):
    try:
        await services.dec_tag(name)
    except exceptions.TagException as e:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"errorCode": e.error_code}
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


@app.post("/tags/dec")
async def dec_tags(names: list[str], response: Response):
    try:
        await services.dec_tags(names)
    except (Exception,) as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"errorCode": ErrorCodes.SERVER_ERROR.value}


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
