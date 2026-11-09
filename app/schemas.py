from __future__ import annotations

from pydantic import BaseModel, Field, computed_field

ISBN_REGEX = r"^\d{10}(\d{3})?$"


class LivroCriar(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    autor: str = Field(min_length=1, max_length=120)
    isbn: str = Field(pattern=ISBN_REGEX, description="10 ou 13 dígitos, sem hífen")
    ano: int = Field(ge=0, le=2100)


class LivroAtualizar(BaseModel):
    """Atualização parcial: só os campos enviados mudam."""

    titulo: str | None = Field(default=None, min_length=1, max_length=200)
    autor: str | None = Field(default=None, min_length=1, max_length=120)
    ano: int | None = Field(default=None, ge=0, le=2100)


class Livro(LivroCriar):
    id: int
    leitor_atual: str | None = None

    @computed_field  # aparece na resposta JSON sem ser armazenado
    @property
    def disponivel(self) -> bool:
        return self.leitor_atual is None


class EmprestimoCriar(BaseModel):
    leitor: str = Field(min_length=1, max_length=120)
