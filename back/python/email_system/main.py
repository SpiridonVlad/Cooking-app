import os
from dotenv import load_dotenv
from fastapi import FastAPI, status, Response
import uvicorn

from constants import ErrorCodesToHTTPCodesMapping
from schemas import AccountVerification, ChangeRequest
from services import handle_account_verification, handle_change_request

load_dotenv()

app = FastAPI()


@app.post("/verify-account")
async def verify_account(account_verification: AccountVerification, response: Response):
    try:
        handle_account_verification(account_verification)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            response.status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return {"errorCode": error_code}


@app.post("/request-change")
async def request_change(change_request: ChangeRequest, response: Response):
    try:
        handle_change_request(change_request)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        error_code = int(str(e))
        if error_code in ErrorCodesToHTTPCodesMapping:
            response.status_code = ErrorCodesToHTTPCodesMapping[error_code]
        return {"errorCode": error_code}


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST", "localhost"), port=int(os.getenv("PORT", 2060)))
