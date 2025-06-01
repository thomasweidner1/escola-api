from datetime import datetime, date
import uvicorn
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing_extensions import Optional

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



class Curso(BaseModel):
    id: int = Field()
    nome: str = Field()
    sigla: Optional[str] = Field(default=None)



class CursoCadastro(BaseModel):
    nome: str = Field()
    sigla: Optional[str] = Field(default=None)



class CursoEditar(BaseModel):
    nome: str = Field()
    sigla: Optional[str] = Field(default=None)


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

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class AlunoCadastro(BaseModel):
    nome: str = Field()
    sobrenome: str = Field()
    cpf: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")
    class Config:
        allow_population_by_field_name = True


class AlunoEditar(BaseModel):
    nome: str = Field()
    sobrenome: str = Field()
    cpf: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")
    class Config:
        allow_population_by_field_name = True


alunos = [
    Aluno(id=1, nome="Thomas", sobrenome="Weidner", cpf="123.456.789-10", data_nascimento=date(2000, 6, 29)),
    Aluno(id=2, nome="João", sobrenome="da Silva", cpf="100.001.202-10", data_nascimento=date(2000, 6, 29))
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


########################professores############################################

class Professor(BaseModel):
    id: int = Field()
    nome: str = Field()
    cnpj: str = Field()
    nome_fantasia: str = Field(alias="nomeFantasia")
    formacao: str = Field()
    chave_pix: str = Field(alias="chavePix")
    signo: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

class ProfessorCadastro(BaseModel):
    nome: str = Field()
    cnpj: str = Field()
    nome_fantasia: str = Field(alias="nomeFantasia")
    formacao: str = Field()
    chave_pix: str = Field(alias="chavePix")
    signo: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")

    class Config:
        allow_population_by_field_name = True

class ProfessorEditar(BaseModel):
    nome: str = Field()
    cnpj: str = Field()
    nome_fantasia: str = Field(alias="nomeFantasia")
    formacao: str = Field()
    chave_pix: str = Field(alias="chavePix")
    signo: str = Field()
    data_nascimento: datetime = Field(alias="dataNascimento")

    class Config:
        allow_population_by_field_name = True

professores = [
    Professor(
        id=1,
        nome='Joaquim França',
        cnpj='00.557.588/0001-45',
        nome_fantasia='Joaquim Ensinos Licensiados',
        formacao='Engenharia de Software',
        chave_pix='joaquim.frança@gmail.com',
        signo='Câncer',
        data_nascimento=date(1997, 7, 4)
    ),
    Professor(
        id=2,
        nome='Pedro Lacerda',
        cnpj='81.972.224/0001-70',
        nome_fantasia='Ensino e Consultoria Lacerda',
        formacao='Ciência da Computação',
        chave_pix='81.972.224/0001-70',
        signo='Libra',
        data_nascimento=date(1988, 10, 5)
    )
]

@app.get("/api/professores")
def obter_professores():
    return professores

@app.get("/api/professores/{id}")
def obter_professores(id: int):
    professor_selecionado = [professor for professor in professores if professor.id == id]
    return professor_selecionado[0]

@app.post("/api/professores")
def cadastrar_professor(form: ProfessorCadastro):
    ultimo_id = max([professor.id for professor in professores], default=0)
    professor = Professor(
        id=ultimo_id + 1,
        nome=form.nome,
        cnpj=form.cnpj,
        nome_fantasia=form.nome_fantasia,
        formacao=form.formacao,
        chave_pix=form.chave_pix,
        signo=form.signo,
        data_nascimento=form.data_nascimento)
    professores.append(professor)
    return(professor)

@app.put("/api/professores/{id}")
def editar_professor(form: ProfessorCadastro, id: int):
    professor_selecionado = [professor for professor in professores if professor.id == id]
    if professor_selecionado[0]:
        professor_selecionado[0].nome = form.nome
        professor_selecionado[0].cnpj = form.cnpj
        professor_selecionado[0].formacao = form.formacao
        professor_selecionado[0].nome_fantasia = form.nome_fantasia
        professor_selecionado[0].chave_pix = form.chave_pix
        professor_selecionado[0].signo = form.signo
        professor_selecionado[0].data_nascimento = form.data_nascimento
        return professor_selecionado[0]
    raise HTTPException(status_code=404, detail=f"Professor não encontrado com id: {id}")

@app.delete("/api/professores/{id}")
def deletar_professor(id: int):
    professor_selecionado = [professor for professor in professores if professor.id == id]
    if professor_selecionado[0]:
        professores.remove(professor_selecionado[0])
        return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")



if __name__ == "__main__":
    uvicorn.run("main:app")
