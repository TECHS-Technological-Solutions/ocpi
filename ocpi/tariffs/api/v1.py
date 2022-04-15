from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_tariffs():
    return "tariffs app created!"
