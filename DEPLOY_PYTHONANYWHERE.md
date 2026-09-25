# Implantação no PythonAnywhere

Guia de referência para esta aplicação Flask. Ajuste caminhos, versão de Python e nome da conta ao ambiente disponível no painel do PythonAnywhere.

## Preparação

1. Clone o repositório e crie um ambiente virtual.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Defina no ambiente de execução:
   - `SECRET_KEY`: segredo aleatório e estável, diferente para cada instalação.
   - `ADMIN_USERNAME` e `ADMIN_PASSWORD`: dados **exclusivos** para criar o primeiro administrador em um banco novo. Eles não alteram contas existentes.
   - `ADMIN_NAME` (opcional): nome de exibição do administrador.
   - `DATABASE_URL` (opcional): URI de banco alternativa.
4. Configure o arquivo WSGI com o diretório do projeto no `sys.path` e importe `from app import app as application`. Forneça os segredos por configuração privada do ambiente, fora do repositório.
5. Configure o mapeamento de `/static/` para a pasta `static` e recarregue a aplicação pelo painel Web.

Exemplo de trecho WSGI, usando variáveis já definidas fora do arquivo:

```python
import sys

project = "/home/SEU_USUARIO/controle-estoque-natura-avon"
if project not in sys.path:
    sys.path.insert(0, project)

from app import app as application
```

A aplicação cria o banco SQLite em `instance/database.db` na primeira execução. Proteja esse arquivo e não o inclua em commits. Mantenha `FLASK_DEBUG` desligado na implantação e use HTTPS.

## Instalações antigas

Versões anteriores continham credenciais administrativas previsíveis e as redefiniam ao iniciar. O código atual parou de redefini-las, mas **não troca senhas já gravadas**. Altere imediatamente as senhas no banco de cada instalação antiga. Uma forma de atualizar uma conta pelo console privado da instalação:

```python
from getpass import getpass
from app import app
from models import Usuario, db

with app.app_context():
    login = input("Usuário existente: ")
    usuario = Usuario.query.filter_by(usuario=login).first()
    if usuario is None:
        raise SystemExit("Usuário não encontrado")
    usuario.set_senha(getpass("Nova senha exclusiva: "))
    db.session.commit()
```

Execute o trecho em um console Python dentro do diretório e do ambiente virtual do projeto. Faça isso para cada conta afetada. Remover a senha do arquivo atual não remove commits antigos do histórico público. Evite reutilizar essas credenciais em outros serviços.
