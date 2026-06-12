# Deploy gratuito no PythonAnywhere

Este projeto roda bem no plano gratuito do PythonAnywhere usando Flask + SQLite.

## 1. Criar conta

Acesse `https://www.pythonanywhere.com/` e crie uma conta gratuita.

Seu site ficara em:

```text
https://thifroz.pythonanywhere.com
```

## 2. Baixar o projeto pelo GitHub

No console Bash do PythonAnywhere:

```bash
git clone https://github.com/ThiagoFroz/controle-estoque-natura-avon.git controle-estoque-natura-avon
```

## 3. Criar ambiente virtual

Ainda no console Bash do PythonAnywhere:

```bash
cd ~/controle-estoque-natura-avon
mkvirtualenv --python=/usr/bin/python3.13 estoque-env
pip install -r requirements.txt
```

## 4. Criar Web App

No painel **Web**:

1. Clique em **Add a new web app**.
2. Escolha **Manual configuration**.
3. Escolha Python 3.13.
4. Em **Virtualenv**, informe:

```text
/home/thifroz/.virtualenvs/estoque-env
```

## 5. Configurar WSGI

No arquivo WSGI do PythonAnywhere, substitua o conteudo pelo modelo abaixo:

```python
import os
import sys

path = "/home/thifroz/controle-estoque-natura-avon"

if path not in sys.path:
    sys.path.insert(0, path)

os.environ["SECRET_KEY"] = "coloque-uma-chave-secreta-grande-aqui"

from app import app as application
```

## 6. Configurar arquivos estaticos

No painel **Web**, em **Static files**, adicione:

```text
URL: /static/
Directory: /home/thifroz/controle-estoque-natura-avon/static
```

## 7. Recarregar

Clique em **Reload** no painel **Web**.

Logins iniciais:

```text
usuario: anafroz
senha: 181085

usuario: sandrafroz
senha: 181085

usuario: thifroz
senha: 181085
```

Antes de usar em producao, e recomendavel implementar uma tela para trocar senhas.
