from datetime import date

from fastapi import HTTPException
from escola_api.app import router
from escola_api.schemas.aluno_schema import AlunoEditar, AlunoCadastro, Aluno

alunos = [
    Aluno(id=1, nome="Thomas", sobrenome="Weidner", cpf="123.456.789-10", data_nascimento=date(2000, 6, 29)),
    Aluno(id=2, nome="João", sobrenome="da Silva", cpf="100.001.202-10", data_nascimento=date(2000, 6, 29))
]


@router.get("/api/alunos")
def obter_todos_alunos():
    return alunos


@router.get("/api/alunos/{id}")
def obter_aluno(id: int):
    aluno_selecionado = [aluno for aluno in alunos if aluno.id == id]
    if not aluno_selecionado:
        raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")
    return aluno_selecionado[0]


#    for aluno in alunos:
#        if aluno.id == id:
#           return aluno

@router.post("/api/alunos")
def cadastrar_aluno(form: AlunoCadastro):
    ultimo_id = max([aluno.id for aluno in alunos], default=0)
    aluno = Aluno(id=ultimo_id + 1, nome=form.nome, sobrenome=form.sobrenome, cpf=form.cpf,
                  data_nascimento=form.data_nascimento)
    alunos.append(aluno)
    return aluno


@router.put("/api/alunos/{id}")
def editar_aluno(id: int, form: AlunoEditar):
    aluno_selecionado = [aluno for aluno in alunos if aluno.id == id]
    if aluno_selecionado[0]:
        aluno_selecionado[0].nome = form.nome
        aluno_selecionado[0].sobrenome = form.sobrenome
        aluno_selecionado[0].cpf = form.cpf
        aluno_selecionado[0].data_nascimento = form.data_nascimento
        return aluno_selecionado
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@router.delete("/api/alunos/{id}")
def apagar_aluno(id: int):
    aluno_selecionado = [aluno for aluno in alunos if aluno.id == id]
    if aluno_selecionado:
        alunos.remove(aluno_selecionado[0])
        return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")