from dataclasses import dataclass, field
from datetime import datetime, date
import uvicorn
from dataclasses_json import dataclass_json, LetterCase
from fastapi import FastAPI, HTTPException
from rich_toolkit import form
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

origins = [
    "http://localhost:4200"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def index():
    return {"mensagem: Olá mundo"}


# localhost:8000/calculadora?numero1=20&numero2=40
@app.get("/calculadora")
def calculadora(numero1: int, numero2: int):
    soma = numero1 + numero2
    return {"soma": soma}


@app.get("/processar-cliente")
def processar_dados_cliente(nome: str, idade: int, sobrenome: str):
    nome_completo = nome + "" + sobrenome
    ano_nascimento = datetime.now().year - idade

    if ano_nascimento >= 1990 and ano_nascimento < 2000:
        decada = "decada de 90"
    elif ano_nascimento >= 1980 and ano_nascimento < 1990:
        decada = "decada de 80"
    elif ano_nascimento >= 1970 and ano_nascimento < 1980:
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
    Curso(id=1, nome="Python Web", sigla="PY1"),
    Curso(id=2, nome="Git e Github", sigla="GT")
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
    curso = Curso(id=ultimo_id + 1, nome=form.nome, sigla=form.sigla)

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


class Aluno(BaseModel):
    id: int = Field()
    nome: str = Field()
    sobrenome: str = Field()
    cpf: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")


class AlunoCadastro(BaseModel):
    nome: str = Field()
    sobrenome: str = Field()
    cpf: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")


class AlunoEditar(BaseModel):
    nome: str = Field()
    sobrenome: str = Field()
    cpf: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")


alunos = [
    Aluno(id=1, nome="Thomas", sobrenome="Weidner", cpf="123.456.789-10", dataNascimento=date(2000, 6, 29)),
    Aluno(id=2, nome="João", sobrenome="da Silva", cpf="100.001.202-10", dataNascimento=date(2000, 6, 29))
]


@app.get("/api/alunos")
def obter_todos_alunos():
    return alunos


@app.get("/api/alunos/{id}")
def obter_aluno(id: int):
    aluno_selecionado = [aluno for aluno in alunos if aluno.id == id]
    if not aluno_selecionado:
        raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")
    return aluno_selecionado[0]


#    for aluno in alunos:
#        if aluno.id == id:
#           return aluno

@app.post("/api/alunos")
def cadastrar_aluno(form: AlunoCadastro):
    ultimo_id = max([aluno.id for aluno in alunos], default=0)
    aluno = Aluno(id=ultimo_id + 1, nome=form.nome, sobrenome=form.sobrenome, cpf=form.cpf,
                  data_nascimento=form.data_nascimento)
    alunos.append(aluno)
    return aluno


@app.put("/api/alunos/{id}")
def editar_aluno(id: int, form: AlunoEditar):
    aluno_selecionado = [aluno for aluno in alunos if aluno.id == id]
    if aluno_selecionado[0]:
        aluno_selecionado[0].nome = form.nome
        aluno_selecionado[0].sobrenome = form.sobrenome
        aluno_selecionado[0].cpf = form.cpf
        aluno_selecionado[0].data_nascimento = form.data_nascimento
        return aluno_selecionado
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@app.delete("/api/alunos/{id}")
def apagar_aluno(id: int):
    aluno_selecionado = [aluno for aluno in alunos if aluno.id == id]
    if aluno_selecionado:
        alunos.remove(aluno_selecionado[0])
        return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


if __name__ == "__main__":
    uvicorn.run("main:app")
