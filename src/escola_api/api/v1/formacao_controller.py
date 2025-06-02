from fastapi import HTTPException

from escola_api.app import router
from escola_api.schemas.formacao_schema import FormacaoCadastro, Formacao

formacoes = []

@router.get("/api/formacoes")
def obter_formacoes():
    return formacoes

@router.get("/api/formacoes/{id}")
def obter_formacoes(id: int):
    formacao_selecionado = [formacao for formacao in formacoes if formacao.id == id]
    return formacao_selecionado[0]

@router.post("/api/formacoes")
def cadastrar_formacao(form: FormacaoCadastro):
    ultimo_id = max([formacao.id for formacao in formacoes], default=0)
    formacao = Formacao(
        id=ultimo_id + 1,
        nome=form.nome,
        descricao=form.descricao,
        duracao=form.duracao)
    formacoes.append(formacao)
    return(formacao)

@router.put("/api/formacoes/{id}")
def editar_formacao(form: FormacaoCadastro, id: int):
    formacao_selecionado = [formacao for formacao in formacoes if formacao.id == id]
    if formacao_selecionado[0]:
        formacao_selecionado[0].nome = form.nome
        formacao_selecionado[0].descricao = form.descricao
        formacao_selecionado[0].duracao = form.duracao

        return formacao_selecionado[0]
    raise HTTPException(status_code=404, detail=f"Formação não encontrada com id: {id}")

@router.delete("/api/formacoes/{id}")
def deletar_formacao(id: int):
    formacao_selecionado = [formacao for formacao in formacoes if formacao.id == id]
    if formacao_selecionado[0]:
        formacoes.remove(formacao_selecionado[0])
        return
    raise HTTPException(status_code=404, detail=f"Formação não encontrada com id: {id}")
