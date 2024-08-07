import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from app.endpoints.auth_endpoints import AUTH_SERVICE_URL
from app.schemas.transaction_schemas import ReportData, Transaction

transaction_router = APIRouter()

TRANSACTION_SERVICE_URL = 'http://127.0.0.1:8002'

headers = {
    'Content-Type': 'application/json',
}


@transaction_router.post("/create_transaction", status_code=status.HTTP_200_OK)
async def create_transaction(transaction: Transaction):
    response = httpx.get(
        AUTH_SERVICE_URL + '/check_token' + f'?id={transaction.user_id}',
        headers=headers,
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)
    else:
        response = httpx.post(
            TRANSACTION_SERVICE_URL + '/create_transaction',
            data=transaction.model_dump_json(),
            headers=headers,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.text)
        return response.json()


@transaction_router.post("/get_report", status_code=status.HTTP_200_OK)
async def get_report(data: ReportData):
    response = httpx.get(
        AUTH_SERVICE_URL + '/check_token' + f'?id={data.user_id}',
        headers=headers,
    )
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code, detail=response.text)
    else:
        response = httpx.post(
            TRANSACTION_SERVICE_URL + '/get_report',
            data=data.model_dump_json(),
            headers=headers,
        )

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, detail=response.text)
        return response.json()
