from dataclasses import dataclass, field
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def index():
    return {"mensagem: Olá mundo"}

#localhost:8000/calculadora?numero1=20&numero2=40
@app.get("/calculadora")
def calculadora(numero1: int, numero2: int):
    soma = numero1 + numero2
    return {"soma": soma}


@app.get("/processar-cliente")
def processar_dados_cliente(nome:str, idade:int, sobrenome:str):
    nome_completo = nome + "" + sobrenome
    ano_nascimento = datetime.now().year - idade

    if ano_nascimento >= 1990 and ano_nascimento < 2000:
        decada = "decada de 90"
    elif ano_nascimento >= 1980 and ano_nascimento < 1990:
        decada = "decada de 80"
    elif ano_nascimento >= 1970 and ano_nascimento <1980:
        decada = "decada de 70"
    else:
        decada = "decada abaixo de 70 ou acima de 90"


    return {
        "nomeCompleto": nome_completo,
        "ano_nascimento": ano_nascimento,
        "decada": decada,
    }

@dataclass
class Curso:
    id: int = field()
    nome: str = field()
    sigla: str = field()

@dataclass
class CursoCadastro:
    nome: str = field()
    sigla: str = field()

@dataclass
class CursoEditar:
    nome: str = field()
    sigla: str = field()

cursos = [
    # instanciando um objeto da classe Curso
    Curso(id = 1, nome = "Python Web", sigla="PY1"),
    Curso(id = 2, nome="Git e Github", sigla="GT")
]
# /docs para abrir o swagger

@app.get("/api/cursos")
def listar_todos_cursos():
    return cursos

@app.get("/api/cursos/{id}")
def obter_por_id_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            return curso
    # Lançando uma exceção com o status code de 404 not found
    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")

@app.post("/api/cursos")
def cadastrar_curso(form: CursoCadastro):
    ultimo_id = max([curso.id for curso in cursos], default=0)

    # instanciar um objeto da classe Curso
    curso = Curso(id = ultimo_id + 1, nome=form.nome, sigla=form.sigla)

    cursos.append(curso)

    return curso

@app.delete("/api/cursos/{id}")
def apagar_curso(id: int):
    for curso in cursos:
        if curso.id == id:
            cursos.remove(curso)
            return

    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")

@app.put("/api/cursos/{id}")
def editar_curso(id: int, form: CursoEditar):
    for curso in cursos:
        if curso.id == id:
            curso.nome = form.nome
            curso.sigla = form.sigla
            return curso

    raise HTTPException(status_code=404, detail=f"Curso não encontrado com id: {id}")

if __name__ == "__main__":
    uvicorn.run("main:app")