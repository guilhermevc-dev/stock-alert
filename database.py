import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "estoque.db"


def conectar():
    conexao = sqlite3.connect(DB_PATH)
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL UNIQUE,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL DEFAULT 0
                CHECK (quantidade >= 0),
            estoque_minimo INTEGER NOT NULL DEFAULT 0
                CHECK (estoque_minimo >= 0)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto_id INTEGER NOT NULL,
            tipo TEXT NOT NULL
                CHECK (tipo IN ('entrada', 'saida')),
            quantidade INTEGER NOT NULL
                CHECK (quantidade > 0),
            data DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (produto_id) REFERENCES produtos(id)
        )
    """)

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    criar_tabelas()
    print("Banco de dados criado com sucesso!")
