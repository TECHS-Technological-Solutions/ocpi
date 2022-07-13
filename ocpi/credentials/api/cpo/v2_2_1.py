from fastapi import APIRouter

router = APIRouter(
    prefix='/credentials',
)


@router.get("/")
def get_credentials():
    return "credentials app created!"
