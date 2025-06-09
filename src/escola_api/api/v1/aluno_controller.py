from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from src.escola_api.app import router
from src.escola_api.database.modelos import AlunoEntidade
from src.escola_api.dependencias import get_db
from src.escola_api.schemas.aluno_schema import AlunoEditar, AlunoCadastro, Aluno


@router.get("/api/alunos", tags=["alunos"])
def obter_todos_alunos(db: Session = Depends(get_db)):
    alunos = db.query(AlunoEntidade).all()
    alunos_response = [Aluno(
        id=aluno.id,
        nome=aluno.nome,
        sobrenome=aluno.sobrenome,
        cpf=aluno.cpf,
        data_nascimento=aluno.data_nascimento,
    ) for aluno in alunos]
    return alunos_response


@router.get("/api/alunos/{id}", tags=["alunos"])
def obter_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoEntidade).filter(AlunoEntidade.id == id).first()
    if not aluno:
        return Aluno(
            id=aluno.id,
            nome=aluno.nome,
            sobrenome=aluno.sobrenome,
            cpf=aluno.cpf,
            data_nascimento=aluno.data_nascimento
        )
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


#    for aluno in alunos:
#        if aluno.id == id:
#           return aluno

@router.post("/api/alunos", tags=["alunos"])
def cadastrar_aluno(form: AlunoCadastro, db: Session = Depends(get_db)):
    aluno = AlunoEntidade(
        nome=form.nome,
        sobrenome=form.sobrenome,
        cpf=form.cpf,
        data_nascimento=form.data_nascimento
    )

    db.add(aluno)
    db.commit()
    db.refresh(aluno)
    return aluno


@router.put("/api/alunos/{id}", tags=["alunos"])
def editar_aluno(id: int, form: AlunoEditar, db: Session = Depends(get_db)):
    aluno = db.query(AlunoEntidade).filter(AlunoEntidade.id == id).first()
    if aluno:
        aluno.nome = form.nome
        aluno.sobrenome = form.sobrenome
        aluno.cpf = form.cpf
        aluno.data_nascimento = form.data_nascimento
        db.commit()
        db.refresh(aluno)
        return aluno
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")


@router.delete("/api/alunos/{id}", tags=["alunos"])
def apagar_aluno(id: int, db: Session = Depends(get_db)):
    aluno = db.query(AlunoEntidade).filter(AlunoEntidade.id == id).first()
    if aluno:
        db.delete(aluno)
        db.commit()
        return
    raise HTTPException(status_code=404, detail=f"Aluno não encontrado com id: {id}")
