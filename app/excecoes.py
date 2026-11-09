class ErroDeDominio(Exception):
    """Base das regras de negócio. ``status`` é o código HTTP correspondente."""

    status = 400

    def __init__(self, mensagem: str) -> None:
        super().__init__(mensagem)
        self.mensagem = mensagem


class LivroNaoEncontrado(ErroDeDominio):
    status = 404

    def __init__(self, id_: int) -> None:
        super().__init__(f"livro {id_} não encontrado")


class IsbnDuplicado(ErroDeDominio):
    status = 409

    def __init__(self, isbn: str) -> None:
        super().__init__(f"já existe um livro com o ISBN {isbn}")


class LivroIndisponivel(ErroDeDominio):
    status = 409

    def __init__(self, id_: int) -> None:
        super().__init__(f"o livro {id_} já está emprestado")


class LivroNaoEmprestado(ErroDeDominio):
    status = 409

    def __init__(self, id_: int) -> None:
        super().__init__(f"o livro {id_} não está emprestado")


class LivroEmprestado(ErroDeDominio):
    status = 409

    def __init__(self, id_: int) -> None:
        super().__init__(f"o livro {id_} está emprestado e não pode ser removido")
