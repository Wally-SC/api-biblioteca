import pytest
from fastapi.testclient import TestClient

from app.main import create_app

LIVRO = {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "isbn": "9788535910663", "ano": 1899}


@pytest.fixture
def client():
    return TestClient(create_app())  # app novo por teste: sem estado compartilhado


def cadastrar(client, **mudancas):
    resposta = client.post("/livros", json={**LIVRO, **mudancas})
    assert resposta.status_code == 201, resposta.text
    return resposta.json()


def test_saude(client):
    assert client.get("/saude").json() == {"status": "ok"}


def test_cadastrar_e_obter(client):
    criado = cadastrar(client)
    assert criado["id"] == 1
    assert criado["disponivel"] is True
    assert client.get("/livros/1").json()["titulo"] == "Dom Casmurro"


def test_livro_inexistente(client):
    resposta = client.get("/livros/99")
    assert resposta.status_code == 404
    assert "não encontrado" in resposta.json()["detalhe"]


def test_isbn_duplicado(client):
    cadastrar(client)
    resposta = client.post("/livros", json=LIVRO)
    assert resposta.status_code == 409


@pytest.mark.parametrize(
    "mudanca",
    [{"titulo": ""}, {"isbn": "123"}, {"isbn": "abcdefghij"}, {"ano": -1}, {"autor": ""}],
)
def test_validacao_de_entrada(client, mudanca):
    assert client.post("/livros", json={**LIVRO, **mudanca}).status_code == 422


def test_listar_com_filtros(client):
    cadastrar(client)
    cadastrar(client, titulo="Memórias Póstumas", isbn="9788535911664", autor="Machado de Assis")
    cadastrar(client, titulo="Vidas Secas", isbn="8501012345", autor="Graciliano Ramos")
    client.post("/livros/3/emprestimo", json={"leitor": "Ana"})

    assert len(client.get("/livros").json()) == 3
    assert len(client.get("/livros", params={"autor": "machado"}).json()) == 2
    disponiveis = client.get("/livros", params={"disponivel": True}).json()
    assert {l["id"] for l in disponiveis} == {1, 2}
    assert [l["id"] for l in client.get("/livros", params={"disponivel": False}).json()] == [3]


def test_atualizacao_parcial(client):
    cadastrar(client)
    resposta = client.patch("/livros/1", json={"ano": 1900})
    assert resposta.status_code == 200
    corpo = resposta.json()
    assert corpo["ano"] == 1900
    assert corpo["titulo"] == "Dom Casmurro"  # intacto


def test_ciclo_de_emprestimo(client):
    cadastrar(client)

    emprestado = client.post("/livros/1/emprestimo", json={"leitor": "Ana"}).json()
    assert emprestado["disponivel"] is False
    assert emprestado["leitor_atual"] == "Ana"

    assert client.post("/livros/1/emprestimo", json={"leitor": "Bia"}).status_code == 409

    devolvido = client.post("/livros/1/devolucao").json()
    assert devolvido["disponivel"] is True
    assert devolvido["leitor_atual"] is None

    assert client.post("/livros/1/devolucao").status_code == 409


def test_nao_remove_livro_emprestado(client):
    cadastrar(client)
    client.post("/livros/1/emprestimo", json={"leitor": "Ana"})
    assert client.delete("/livros/1").status_code == 409
    client.post("/livros/1/devolucao")
    assert client.delete("/livros/1").status_code == 204
    assert client.get("/livros/1").status_code == 404


def test_leitor_vazio_rejeitado(client):
    cadastrar(client)
    assert client.post("/livros/1/emprestimo", json={"leitor": ""}).status_code == 422
