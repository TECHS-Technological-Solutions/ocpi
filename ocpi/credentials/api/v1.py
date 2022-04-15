from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_credentials():
    return "credentials app created!"
