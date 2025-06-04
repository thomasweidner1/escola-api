import uvicorn

from src.escola_api.database.banco_dados import Base, engine
from src.escola_api.api.v1 import curso_controller, aluno_controller, professor_controller, formacao_controller
from src.escola_api.app import app

app.include_router(curso_controller.router)
app.include_router(aluno_controller.router)
app.include_router(professor_controller.router)
app.include_router(formacao_controller.router)

Base.metadata.create_all(bind=engine)

# @router.get("/")
# def index():
#     return {"mensagem: Olá mundo"}
#
#
# # localhost:8000/calculadora?numero1=20&numero2=40
# @router.get("/calculadora")
# def calculadora(numero1: int, numero2: int):
#     soma = numero1 + numero2
#     return {"soma": soma}
#
#
# @router.get("/processar-cliente")
# def processar_dados_cliente(nome: str, idade: int, sobrenome: str):
#     nome_completo = nome + "" + sobrenome
#     ano_nascimento = datetime.now().year - idade
#
#     if ano_nascimento >= 1990 and ano_nascimento < 2000:
#         decada = "decada de 90"
#     elif ano_nascimento >= 1980 and ano_nascimento < 1990:
#         decada = "decada de 80"
#     elif ano_nascimento >= 1970 and ano_nascimento < 1980:
#         decada = "decada de 70"
#     else:
#         decada = "decada abaixo de 70 ou acima de 90"
#
#     return {
#         "nomeCompleto": nome_completo,
#         "ano_nascimento": ano_nascimento,
#         "decada": decada,
#     }

if __name__ == "__main__":
    uvicorn.run("main:app")
