from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_sessions():
    return "sessions app created!"
