from fastapi import APIRouter

router = APIRouter(
    prefix='/tokens',
)


@router.get("/")
def get_tokens():
    return "tokens app created!"
