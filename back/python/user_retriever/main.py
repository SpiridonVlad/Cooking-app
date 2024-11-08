from typing import Annotated
from fastapi import FastAPI, status, Header
from fastapi.responses import JSONResponse
from exception import UserRetrieverException
import services
import uvicorn
from constants import HOST, PORT, ErrorCodes
from schemas import UserData, UserCardData, UserCardsRequestData, UserFullData, UserCardDataList

app = FastAPI(title="User Retriever")


@app.get("/{user_id}", tags=["user_data"], response_model=UserData, response_description="Successful operation")
async def get_user_data(user_id: str, x_user_id: Annotated[str | None, Header()] = None) -> UserData | JSONResponse:
    try:
        return await services.get_user_data(user_id, x_user_id)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.get("/{user_id}/card", tags=["user_card_data"], response_model=UserCardData,
         response_description="Successful operation")
async def get_user_card(user_id: str, x_user_id: Annotated[str | None, Header()] = None) -> UserCardData | JSONResponse:
    try:
        return await services.get_user_card_data(user_id, x_user_id)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.post("/", tags=["user_cards_data"], response_model=UserCardDataList, response_description="Successful operation")
async def get_user_cards(user_ids: UserCardsRequestData,
                         x_user_id: Annotated[str | None, Header()] = None) -> UserCardDataList | JSONResponse:
    try:
        cards = await services.get_user_cards_data(user_ids.ids, x_user_id)
        return UserCardDataList(cards=cards)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


@app.get("/{user_id}/profile", tags=["user_full_data, auth"], response_model=UserFullData,
         response_description="Successful operation")
async def get_user_full_data(user_id: str,
                             x_user_id: Annotated[str | None, Header()] = None) -> UserFullData | JSONResponse:
    if not x_user_id:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"errorCode": ErrorCodes.UNAUTHORIZED_REQUEST.value})

    if x_user_id != user_id:
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN,
                            content={"errorCode": ErrorCodes.FORBIDDEN_REQUEST.value})

    try:
        return await services.get_user_full_data(user_id)
    except UserRetrieverException as e:
        return JSONResponse(status_code=e.status_code, content={"errorCode": e.error_code})
    except (Exception,):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content={"errorCode": ErrorCodes.SERVER_ERROR.value})


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
