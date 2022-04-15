from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_tokens():
    return "tokens app created!"
