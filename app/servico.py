from __future__ import annotations

from app.excecoes import LivroEmprestado, LivroIndisponivel, LivroNaoEmprestado
from app.repositorio import RepositorioEmMemoria
from app.schemas import Livro, LivroAtualizar, LivroCriar


class ServicoBiblioteca:
    """Regras de negócio, independentes de HTTP."""

    def __init__(self, repositorio: RepositorioEmMemoria) -> None:
        self._repo = repositorio

    def cadastrar(self, dados: LivroCriar) -> Livro:
        return self._repo.criar(dados)

    def obter(self, id_: int) -> Livro:
        return self._repo.obter(id_)

    def listar(self, autor: str | None = None, disponivel: bool | None = None) -> list[Livro]:
        return self._repo.listar(autor, disponivel)

    def atualizar(self, id_: int, dados: LivroAtualizar) -> Livro:
        livro = self._repo.obter(id_)
        atualizado = livro.model_copy(update=dados.model_dump(exclude_unset=True, exclude_none=True))
        return self._repo.salvar(atualizado)

    def remover(self, id_: int) -> None:
        livro = self._repo.obter(id_)
        if not livro.disponivel:
            raise LivroEmprestado(id_)
        self._repo.remover(id_)

    def emprestar(self, id_: int, leitor: str) -> Livro:
        livro = self._repo.obter(id_)
        if not livro.disponivel:
            raise LivroIndisponivel(id_)
        return self._repo.salvar(livro.model_copy(update={"leitor_atual": leitor.strip()}))

    def devolver(self, id_: int) -> Livro:
        livro = self._repo.obter(id_)
        if livro.disponivel:
            raise LivroNaoEmprestado(id_)
        return self._repo.salvar(livro.model_copy(update={"leitor_atual": None}))
