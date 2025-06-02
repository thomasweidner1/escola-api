from datetime import datetime
from pydantic import BaseModel, Field

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