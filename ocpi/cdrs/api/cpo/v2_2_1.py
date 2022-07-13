from fastapi import APIRouter

router = APIRouter(
    prefix='/cdrs',
)


@router.get("/")
def get_cdrs():
    return "cdrs app created!"
