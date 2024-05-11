from fastapi import FastAPI, Query, APIRouter, Request
from fastapi.responses import JSONResponse

from schemas import RatingList, RatingCreate, RatingUpdate
from services import RatingService
from constants import DatabaseError, ExternalError, InternalError, InvalidDataError, DatabaseNotFoundDataError

app = FastAPI()
router = APIRouter(
    prefix="/api"
)

service_errors = (DatabaseError, ExternalError, InternalError)
rating_service = RatingService()


@app.middleware("http")
async def normalize_error(request: Request, call_next):
    response = await call_next(request)
    if response.status_code == 422:     # If the framework rejects the request due to invalid data types or ranges
        response = JSONResponse(
            status_code=400,
            content={"error_code": InvalidDataError().value}
        )
    return response


@router.get("/rating/{parent_id}/replies", response_model=RatingList, response_description="Successful operation")
async def get_ratings(parent_id: str, start: int = Query(0), count: int = Query(10)) -> RatingList | JSONResponse:
    try:
        return await rating_service.get_ratings(parent_id, start, count)
    except service_errors as e:
        return JSONResponse(
            status_code=500,
            content={"error_code": e.value}
        )


@router.put("/rating/{parent_id}/replies", response_description="Successful operation")
async def create_rating(parent_id: str, rating_data: RatingCreate) -> JSONResponse:
    try:
        await rating_service.create_rating(parent_id, rating_data)
    except service_errors as e:
        return JSONResponse(
            status_code=500,
            content={"error_code": e.value}
        )


@router.patch("/rating/{rating_id}", response_description="Successful operation")
async def update_rating(rating_id: str, rating_data: RatingUpdate) -> JSONResponse:
    try:
        await rating_service.update_rating(rating_id, rating_data)
    except service_errors as e:
        return JSONResponse(
            status_code=500,
            content={"error_code": e.value}
        )
    except DatabaseNotFoundDataError as e:
        return JSONResponse(
            status_code=400,
            content={"error_code": e.value}
        )


@router.delete("/rating/{rating_id}", response_description="Successful operation")
async def delete_rating(rating_id: str) -> JSONResponse:
    try:
        await rating_service.delete_rating(rating_id)
    except service_errors as e:
        return JSONResponse(
            status_code=500,
            content={"error_code": e.value}
        )
    except DatabaseNotFoundDataError as e:
        return JSONResponse(
            status_code=400,
            content={"error_code": e.value}
        )


app.include_router(router)
