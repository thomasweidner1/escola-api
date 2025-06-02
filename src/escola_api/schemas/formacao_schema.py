from datetime import date

from pydantic import BaseModel, Field


class Formacao(BaseModel):
    id: int = Field()
    nome: str = Field()
    descricao: str = Field()
    duracao: date = Field()

    class Config:
        allow_population_by_field_name = True
        populate_by_name = True

class FormacaoCadastro(BaseModel):
    nome: str = Field()
    descricao: str = Field()
    duracao: date = Field()


class Config:
        allow_population_by_field_name = True

class FormacaoEditar(BaseModel):
    nome: str = Field()
    descricao: str = Field()
    duracao: date = Field()

    class Config:
        allow_population_by_field_name = True

