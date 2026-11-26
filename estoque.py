
from database import conectar
from contextlib import closing


def cadastrar_produto(codigo, nome, categoria, quantidade, estoque_minimo):
    with closing(conectar()) as conexao:
        with conexao:
            conexao.execute("""
                INSERT INTO produtos (
                    codigo, nome, categoria,
                    quantidade, estoque_minimo
                )
                VALUES (?, ?, ?, ?, ?)
            """, (codigo, nome, categoria, quantidade, estoque_minimo))


def listar_produtos():
    with closing(conectar()) as conexao:
        cursor = conexao.execute("""
            SELECT * FROM produtos
            ORDER BY nome
        """)

        return cursor.fetchall()


def atualizar_produto(id_produto, codigo, nome, categoria, estoque_minimo):
    with closing(conectar()) as conexao:
        with conexao:
            conexao.execute("""
                UPDATE produtos
                SET codigo = ?,
                    nome = ?,
                    categoria = ?,
                    estoque_minimo = ?
                WHERE id = ?
            """, (codigo, nome, categoria, estoque_minimo, id_produto))


def excluir_produto(id_produto):
    with closing(conectar()) as conexao:
        with conexao:
            conexao.execute("""
                DELETE FROM produtos
                WHERE id = ?
            """, (id_produto,))