
import sqlite3
import streamlit as st

from database import criar_tabelas
from estoque import (
    cadastrar_produto,
    listar_produtos,
    atualizar_produto,
    excluir_produto
)

st.set_page_config(
    page_title="StockAlert",
    page_icon="📦",
    layout="wide"
)

criar_tabelas()


@st.dialog("Cadastrar produto")
def janela_cadastro():
    with st.form("cadastro"):
        codigo = st.text_input("Código")
        nome = st.text_input("Nome")
        categoria = st.text_input("Categoria")

        quantidade = st.number_input(
            "Quantidade em estoque",
            min_value=0,
            step=1
        )

        estoque_minimo = st.number_input(
            "Estoque mínimo",
            min_value=0,
            step=1
        )

        if st.form_submit_button("Cadastrar"):
            if not all([codigo.strip(), nome.strip(), categoria.strip()]):
                st.warning("Preencha todos os campos obrigatórios.")

            else:
                try:
                    cadastrar_produto(
                        codigo.strip(),
                        nome.strip(),
                        categoria.strip(),
                        quantidade,
                        estoque_minimo
                    )

                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Código já cadastrado.")


@st.dialog("Editar produto")
def janela_edicao(produto):
    with st.form("edicao"):
        codigo = st.text_input("Código", value=produto[1])
        nome = st.text_input("Nome", value=produto[2])
        categoria = st.text_input("Categoria", value=produto[3])

        estoque_minimo = st.number_input(
            "Estoque mínimo",
            min_value=0,
            value=produto[5],
            step=1
        )

        if st.form_submit_button("Salvar alterações"):
            if not all([codigo.strip(), nome.strip(), categoria.strip()]):
                st.warning("Preencha todos os campos obrigatórios.")

            else:
                try:
                    atualizar_produto(
                        produto[0],
                        codigo.strip(),
                        nome.strip(),
                        categoria.strip(),
                        estoque_minimo
                    )

                    st.rerun()

                except sqlite3.IntegrityError:
                    st.error("Código já cadastrado.")


@st.dialog("Excluir produto")
def janela_exclusao(produto):
    st.warning(
        f"Deseja realmente excluir o produto {produto[2]}?"
    )

    col1, col2 = st.columns(2)

    if col1.button("Confirmar exclusão", type="primary"):
        try:
            excluir_produto(produto[0])
            st.rerun()

        except sqlite3.IntegrityError:
            st.error("Este produto possui movimentações registradas.")

    if col2.button("Cancelar"):
        st.rerun()


st.title("StockAlert")
st.caption("Sistema de monitoramento de estoque")

st.divider()

col1, col2 = st.columns([4, 1])

with col1:
    st.subheader("Produtos cadastrados")

with col2:
    if st.button("＋ Novo produto", type="primary"):
        janela_cadastro()

pesquisa = st.text_input(
    "Pesquisar produto",
    placeholder="Digite o código, nome ou categoria..."
).strip().lower()

produtos = listar_produtos()

produtos_filtrados = [
    produto for produto in produtos
    if pesquisa in produto[1].lower()
    or pesquisa in produto[2].lower()
    or pesquisa in produto[3].lower()
]

larguras = [1, 3, 2, 1, 1, 1, 1]

colunas = st.columns(larguras)

titulos = [
    "Código",
    "Produto",
    "Categoria",
    "Estoque",
    "Mínimo",
    "Editar",
    "Excluir"
]

for coluna, titulo in zip(colunas, titulos):
    coluna.markdown(f"**{titulo}**")

st.divider()

for produto in produtos_filtrados:
    colunas = st.columns(larguras)

    colunas[0].write(produto[1])
    colunas[1].write(produto[2])
    colunas[2].write(produto[3])
    colunas[3].write(produto[4])
    colunas[4].write(produto[5])

    if colunas[5].button(
        "✏️",
        key=f"editar_{produto[0]}"
    ):
        janela_edicao(produto)

    if colunas[6].button(
        "🗑️",
        key=f"excluir_{produto[0]}"
    ):
        janela_exclusao(produto)

if not produtos_filtrados:
    st.info("Nenhum produto encontrado.")

st.divider()

st.caption(f"Total de produtos exibidos: {len(produtos_filtrados)}")
