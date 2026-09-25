# Controle de Estoque Natura & Avon

Aplicação web de estudo em **Flask e SQLite** para acompanhar produtos, estoque e vendas de Natura e Avon. Há uma área pública com catálogo, combos e promoções por ciclo, e uma área administrativa para produtos, movimentações, vendas e relatórios.

## Recursos implementados

- Cadastro de produtos com imagens, destaque e estoque mínimo.
- Registro de entradas e saídas e baixa de estoque nas vendas.
- Ciclos, combos e promoções.
- Relatórios de estoque e vendas em CSV e visualização para impressão.

## Executar localmente

```bash
git clone https://github.com/ThiagoFroz/controle-estoque-natura-avon.git
cd controle-estoque-natura-avon
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="$(python3 -c 'import secrets; print(secrets.token_hex(32))')"
export ADMIN_USERNAME="seu-admin"
export ADMIN_PASSWORD="uma-senha-longa-e-exclusiva"
python app.py
```

Acesse `http://127.0.0.1:5000/` para a área pública e `http://127.0.0.1:5000/login` para entrar. O banco local é criado em `instance/database.db`.

`ADMIN_USERNAME` e `ADMIN_PASSWORD` só criam um usuário se ele ainda não existir; iniciar o aplicativo novamente **não redefine senhas existentes**. Para outras contas, configure usuários diretamente por um fluxo administrativo apropriado. Não use credenciais de exemplo nem publique o banco de dados. Em produção, defina uma `SECRET_KEY` estável, exclusiva e secreta, mantenha `FLASK_DEBUG` desligado e use HTTPS. O [guia de implantação](DEPLOY_PYTHONANYWHERE.md) contém o roteiro para PythonAnywhere; confira as variáveis de ambiente antes de publicar.

> Credenciais anteriormente incluídas no histórico público devem ser consideradas comprometidas. Troque senhas em qualquer instalação existente; alterar o README ou o código atual não invalida o histórico.
