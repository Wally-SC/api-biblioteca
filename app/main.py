from __future__ import annotations

from fastapi import Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse

from app.excecoes import ErroDeDominio
from app.repositorio import RepositorioEmMemoria
from app.schemas import EmprestimoCriar, Livro, LivroAtualizar, LivroCriar
from app.servico import ServicoBiblioteca


def create_app(repositorio: RepositorioEmMemoria | None = None) -> FastAPI:
    """Fábrica da aplicação. Cada chamada tem seu próprio repositório (bom para testes)."""
    servico = ServicoBiblioteca(repositorio or RepositorioEmMemoria())
    app = FastAPI(title="API da Biblioteca", version="0.1.0")

    def obter_servico() -> ServicoBiblioteca:
        return servico

    @app.exception_handler(ErroDeDominio)
    async def tratar_erro_de_dominio(_: Request, exc: ErroDeDominio) -> JSONResponse:
        return JSONResponse(status_code=exc.status, content={"detalhe": exc.mensagem})

    @app.get("/saude")
    def saude() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/livros", response_model=Livro, status_code=201)
    def cadastrar(dados: LivroCriar, svc: ServicoBiblioteca = Depends(obter_servico)):
        return svc.cadastrar(dados)

    @app.get("/livros", response_model=list[Livro])
    def listar(autor: str | None = None, disponivel: bool | None = None, svc: ServicoBiblioteca = Depends(obter_servico)):
        return svc.listar(autor, disponivel)

    @app.get("/livros/{id_}", response_model=Livro)
    def obter(id_: int, svc: ServicoBiblioteca = Depends(obter_servico)):
        return svc.obter(id_)

    @app.patch("/livros/{id_}", response_model=Livro)
    def atualizar(id_: int, dados: LivroAtualizar, svc: ServicoBiblioteca = Depends(obter_servico)):
        return svc.atualizar(id_, dados)

    @app.delete("/livros/{id_}", status_code=204)
    def remover(id_: int, svc: ServicoBiblioteca = Depends(obter_servico)) -> Response:
        svc.remover(id_)
        return Response(status_code=204)

    @app.post("/livros/{id_}/emprestimo", response_model=Livro)
    def emprestar(id_: int, dados: EmprestimoCriar, svc: ServicoBiblioteca = Depends(obter_servico)):
        return svc.emprestar(id_, dados.leitor)

    @app.post("/livros/{id_}/devolucao", response_model=Livro)
    def devolver(id_: int, svc: ServicoBiblioteca = Depends(obter_servico)):
        return svc.devolver(id_)

    return app


app = create_app()
