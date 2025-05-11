# 💼 Sistema de Gestão de Colaboradores e Reembolsos

Este projeto é uma API desenvolvida em **Flask** para gerenciamento de colaboradores e controle de solicitações de reembolso. Ele permite o cadastro, autenticação e atualização de colaboradores, além da criação, listagem e visualização de reembolsos.

## 🚀 Tecnologias Utilizadas

- Python 3.x
- Flask
- SQLAlchemy
- Flask-Session
- Bcrypt
- Flasgger (Swagger UI para documentação da API)
- Banco de dados (ex: MySQL, PostgreSQL ou SQLite)




## 🔐 Funcionalidades

### 👤 Colaboradores

- `GET /colaborador/todos-colaboradores`  
  Lista todos os colaboradores cadastrados.

- `POST /colaborador/cadastrar`  
  Cadastra um novo colaborador (**com hash de senha e validação de e-mail único**).

- `PUT /colaborador/atualizar/<id_colaborador>`  
  Atualiza os dados de um colaborador (mock).

- `POST /colaborador/login`  
  Realiza o login e inicia a sessão do colaborador.

- `GET /colaborador/perfil`  
  Retorna os dados do colaborador logado.

---

### 💸 Reembolsos

- `POST /colaborador/reembolsos`  
  Cria uma nova solicitação de reembolso.

- `GET /colaborador/reembolsos/<num_prestacao>`  
  Visualiza um reembolso pelo número da prestação.

- `GET /colaborador/reembolsos`  
  Lista todos os reembolsos.

- `GET /colaborador/reembolsos/<id>`  
  Busca um reembolso por ID.

---

## 📦 Instalação e Execução

1. Clone o repositório:
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio

2. Crie e ative um ambiente virtual:
  python -m venv venv
  source venv/bin/activate  # Linux/macOS
  venv\Scripts\activate     # Windows

3. Instale as dependências:
  pip install -r requirements.txt

4. Configure o banco de dados no arquivo app.py ou em um .env.

5. Execute o servidor:
  flask run
6. Acesse a documentação Swagger em:
   http://localhost:5000/apidocs/

✅ Próximas Melhorias
-Validação de e-mails e crachás duplicados

-Logout de sessões

-Filtros e paginação para reembolsos

-Upload de comprovantes de despesas
