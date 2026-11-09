from __future__ import annotations

from app.excecoes import IsbnDuplicado, LivroNaoEncontrado
from app.schemas import Livro, LivroCriar


class RepositorioEmMemoria:
    """Armazenamento simples em memória. Troque por um banco mantendo a mesma interface."""

    def __init__(self) -> None:
        self._livros: dict[int, Livro] = {}
        self._proximo_id = 1

    def criar(self, dados: LivroCriar) -> Livro:
        if any(l.isbn == dados.isbn for l in self._livros.values()):
            raise IsbnDuplicado(dados.isbn)
        livro = Livro(id=self._proximo_id, **dados.model_dump())
        self._livros[livro.id] = livro
        self._proximo_id += 1
        return livro

    def obter(self, id_: int) -> Livro:
        try:
            return self._livros[id_]
        except KeyError:
            raise LivroNaoEncontrado(id_) from None

    def listar(self, autor: str | None = None, disponivel: bool | None = None) -> list[Livro]:
        livros = list(self._livros.values())
        if autor:
            livros = [l for l in livros if autor.lower() in l.autor.lower()]
        if disponivel is not None:
            livros = [l for l in livros if l.disponivel == disponivel]
        return livros

    def salvar(self, livro: Livro) -> Livro:
        self.obter(livro.id)
        self._livros[livro.id] = livro
        return livro

    def remover(self, id_: int) -> None:
        self.obter(id_)
        del self._livros[id_]
