# Controle de Estoque Natura & Avon

Sistema web em Flask para gerenciamento de estoque, vendas, combos, promocoes e ciclos de produtos Natura e Avon.

## Funcionalidades

- Area publica com pagina inicial, promocoes do ciclo, combos, destaques e catalogo filtravel.
- Login administrativo para `anafroz`, `sandrafroz` e `thifroz`.
- CRUD de produtos com imagem, destaque, estoque minimo e exclusao logica.
- Movimentacoes de estoque com historico e responsavel.
- Cadastro de vendas com baixa automatica de estoque.
- Cadastro de ciclos, combos e promocoes vinculadas a ciclos.
- Dashboard com indicadores e relatorios de estoque/vendas em CSV e pagina de impressao para PDF.

## Como executar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Depois acesse:

- Publico: `http://127.0.0.1:5000/`
- Admin: `http://127.0.0.1:5000/login`

O banco SQLite fica em `instance/database.db` e e criado automaticamente na primeira execucao.

Usuarios administrativos iniciais:

```text
anafroz / 181085
sandrafroz / 181085
thifroz / 181085
```

## Deploy gratuito

Para publicar sem custo, use o guia [DEPLOY_PYTHONANYWHERE.md](DEPLOY_PYTHONANYWHERE.md).
