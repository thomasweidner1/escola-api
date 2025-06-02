from datetime import date

from fastapi import HTTPException

from escola_api.app import router
from escola_api.schemas.professor_schema import Professor, ProfessorCadastro

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

@router.get("/api/professores")
def obter_professores():
    return professores

@router.get("/api/professores/{id}")
def obter_professores(id: int):
    professor_selecionado = [professor for professor in professores if professor.id == id]
    return professor_selecionado[0]

@router.post("/api/professores")
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

@router.put("/api/professores/{id}")
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

@router.delete("/api/professores/{id}")
def deletar_professor(id: int):
    professor_selecionado = [professor for professor in professores if professor.id == id]
    if professor_selecionado[0]:
        professores.remove(professor_selecionado[0])
        return
    raise HTTPException(status_code=404, detail=f"Professor não encontrado com id: {id}")