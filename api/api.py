import fastapi

router = fastapi.APIRouter()


@router.get('/ping')
async def ping() -> dict:
    return {'response': 'Pet Cam Server Running v. 0.0.1'}
