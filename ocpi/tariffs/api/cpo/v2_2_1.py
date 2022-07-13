from fastapi import APIRouter

router = APIRouter(
    prefix='/tariffs',
)


@router.get("/")
def get_tariffs():
    return "tariffs app created!"
