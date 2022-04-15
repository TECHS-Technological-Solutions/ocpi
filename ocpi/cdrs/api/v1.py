from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_cdrs():
    return "cdrs app created!"
