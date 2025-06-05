import uvicorn

from src.escola_api.database.banco_dados import Base, engine
from src.escola_api.api.v1 import curso_controller, aluno_controller, professor_controller, formacao_controller
from src.escola_api.app import app

Base.metadata.create_all(bind=engine)

app.include_router(curso_controller.router)
app.include_router(aluno_controller.router)
app.include_router(professor_controller.router)
app.include_router(formacao_controller.router)


if __name__ == "__main__":
    uvicorn.run("main:app")
