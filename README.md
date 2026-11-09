# api-biblioteca

API REST de uma biblioteca (cadastro de livros e empréstimos) feita com **FastAPI**.

## Rodando

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
# documentação interativa: http://127.0.0.1:8000/docs
```

Com Docker:

```bash
docker build -t api-biblioteca .
docker run --rm -p 8000:8000 api-biblioteca
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/livros` | cadastra livro (ISBN de 10 ou 13 dígitos, único) |
| GET | `/livros?autor=&disponivel=` | lista com filtros |
| GET | `/livros/{id}` | detalhe |
| PATCH | `/livros/{id}` | atualização parcial |
| DELETE | `/livros/{id}` | remove (409 se estiver emprestado) |
| POST | `/livros/{id}/emprestimo` | empresta `{"leitor": "Ana"}` (409 se já emprestado) |
| POST | `/livros/{id}/devolucao` | devolve (409 se não estava emprestado) |
| GET | `/saude` | health check |

## Estrutura

```
app/
  main.py         # rotas e fábrica create_app()
  schemas.py      # modelos Pydantic e validações
  servico.py      # regras de negócio, sem dependência de HTTP
  repositorio.py  # armazenamento (em memória)
  excecoes.py     # erros de domínio com código HTTP associado
tests/test_api.py
```

As regras de negócio ficam no serviço e as rotas só traduzem HTTP, então trocar
o repositório em memória por um banco real não mexe nas rotas.
Os dados são perdidos ao reiniciar (por escolha: é o próximo passo natural do projeto).

## Testes

```bash
pytest
```
