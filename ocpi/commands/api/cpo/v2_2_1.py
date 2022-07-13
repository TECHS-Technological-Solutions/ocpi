from fastapi import APIRouter

router = APIRouter(
    prefix='/commands',
)


@router.get("/")
def get_commands():
    return "commands app created!"
