from datetime import date

from pydantic import BaseModel, Field


class MatriculaBase(BaseModel):
    aluno_id: int = Field()
    curso_id: int = Field()

class MatriculaAluno(BaseModel):
    id: int = Field()
    nome: str = Field()
    sobrenome: str = Field()

class Matricula(MatriculaAluno):
    data_matricula: date = Field(alias='dataMatricula')
    aluno: MatriculaAluno = Field()
    id: int = Field()

    class Config:
        validate_by_name = True

class MatriculaCadastro(MatriculaBase):
    pass

class MatriculaEditar(BaseModel):
    curso_id: int = Field()