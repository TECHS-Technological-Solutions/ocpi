from fastapi import APIRouter

router = APIRouter(
    prefix='/sessions',
)


@router.get("/")
def get_sessions():
    return "sessions app created!"
