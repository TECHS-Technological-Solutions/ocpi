from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_commands():
    return "commands app created!"
