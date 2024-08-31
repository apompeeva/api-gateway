import httpx
from fastapi import APIRouter, HTTPException, status

from app.endpoints.auth_endpoints import AUTH_SERVICE_URL
from app.schemas.transaction_schemas import ReportData, Transaction

transaction_router = APIRouter()

TRANSACTION_SERVICE_URL = 'http://transaction-service-pompeeva-service:8002'

headers = {
    'Content-Type': 'application/json',
}


@transaction_router.post('/create_transaction', status_code=status.HTTP_200_OK)
async def create_transaction(transaction: Transaction):
    """Проксирует запрос создания транзакции c проверкой токена."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL + '/check_token' + f'?user_id={transaction.user_id}',
            headers=headers,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )
        else:
            response = await client.post(
                TRANSACTION_SERVICE_URL + '/create_transaction',
                data=transaction.model_dump_json(),
                headers=headers,
            )

            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
        return response.json()


@transaction_router.post('/get_report', status_code=status.HTTP_200_OK)
async def get_report(report_data: ReportData):
    """Проксирует запрос получения отчета о транзакциях за период."""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            AUTH_SERVICE_URL + '/check_token' + f'?user_id={report_data.user_id}',
            headers=headers,
        )
        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.text,
            )
        else:
            response = await client.post(
                TRANSACTION_SERVICE_URL + '/get_report',
                data=report_data.model_dump_json(),
                headers=headers,
            )

            if response.status_code != status.HTTP_200_OK:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.text,
                )
        return response.json()
