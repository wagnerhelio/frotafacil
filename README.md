# FrotaFácil

Sistema moderno de gestão de frota desenvolvido em Django, com foco em padronização, responsividade, integração de dados e fluxo de requisições.

---

## 🖼️ Telas do Sistema

<table>
  <tr>
    <th>Login</th>
    <th>Home</th>
    <th>Home Veículos</th>
    <th>Home Requisições</th>
    <th>Home Agentes</th>
    <th>Home Admin</th>
  </tr>
  <tr>
    <td><a href="frotafacil/static/Docs/Login.png"><img src="frotafacil/static/Docs/Login.png" width="180"/></a></td>
    <td><a href="frotafacil/static/Docs/Home.png"><img src="frotafacil/static/Docs/Home.png" width="180"/></a></td>
    <td><a href="frotafacil/static/Docs/Home_Veiculos.png"><img src="frotafacil/static/Docs/Home_Veiculos.png" width="180"/></a></td>
    <td><a href="frotafacil/static/Docs/Home_Requisicoes.png"><img src="frotafacil/static/Docs/Home_Requisicoes.png" width="180"/></a></td>
    <td><a href="frotafacil/static/Docs/Home_Agentes.png"><img src="frotafacil/static/Docs/Home_Agentes.png" width="180"/></a></td>
    <td><a href="frotafacil/static/Docs/Home_Admin.png"><img src="frotafacil/static/Docs/Home_Admin.png" width="180"/></a></td>
  </tr>
</table>

## 🚀 Passo a Passo para Subir o Projeto

### 1. Crie e ative o ambiente virtual (recomendado: 'frotafacil-env')
```bash
# Windows
python -m venv frotafacil-env
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\frotafacil-env\Scripts\activate

# Linux/macOS
python3 -m venv frotafacil-env
source frotafacil-env/bin/activate
```

### 2. Clone o repositório pra dentro de frotafacil-env
```bash
cd frotafacil-env

git clone https://github.com/wagnerhelio/frotafacil.git
ou
git clone https://github.com/ViniciusBenevides/Projetos-JF.git

cd frotafacil
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt

Caso tenha atualizado o projeto atualize os requirements

pip freeze > requirements.txt
```

### 5. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Inicie o servidor Local
```bash
python manage.py runserver
```
### 8. Inicie o servidor Linux 

### Ajustando permissões do banco de dados SQLite

Após subir o projeto no servidor Linux, ajuste as permissões do arquivo do banco de dados para evitar erros de "readonly database" ao rodar com Apache:

```bash
# Dê a posse do arquivo do banco para o usuário do Apache
chown www-data:www-data /var/www/html/sistemas/frotafacil-env/frotafacil/db.sqlite3

# Dê permissão de leitura e escrita para o usuário e grupo
chmod 664 /var/www/html/sistemas/frotafacil-env/frotafacil/db.sqlite3

# Dê permissão de escrita no diretório onde está o banco
chown www-data:www-data /var/www/html/sistemas/frotafacil-env/frotafacil/
chmod 775 /var/www/html/sistemas/frotafacil-env/frotafacil/
```

Se o Apache estiver rodando como outro usuário, substitua `www-data` pelo usuário correto.

### Reiniciando o Apache e monitorando logs

Após ajustar as permissões, reinicie o serviço do Apache para garantir que as alterações tenham efeito:

```bash
service apache2 restart
```

Se quiser limpar o log de erros antes de testar novamente:

```bash
truncate -s 0 /var/log/apache2/error.log
```

Para monitorar o log de erros em tempo real:

```bash
tail -f /var/log/apache2/error.log
```

## ⚙️ URLs de Acesso

- **Admin Django Local:**
  - URL: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Admin Django Homolog Linux:**
  - URL: [http://172.22.3.95/frotafacil/admin](http://127.0.0.1:8000/admin/)

  > **Importante:** Após criar o superusuário, acesse a tela acima e insira os dados dos usuários de serviço LDAP e o Azure Tenant ID para autenticação corporativa.

---

## 🧰 Tecnologias Utilizadas

- Python 3.10+
- Django 5.2
- Bootstrap 5
- SQLite (desenvolvimento) / PostgreSQL (produção)
- Azure AD / LDAP para autenticação

## ✅ Requisitos

- Python 3.10+
- pip (gerenciador de pacotes Python)
- Git
- Navegador moderno (Chrome, Firefox, Edge)

---

## 🗂 Estrutura do Projeto

```
frotafacil/
├── controlefrota/           # Aplicação principal
│   ├── models/             # Modelos do banco de dados
│   ├── views/              # Views e lógica de negócio
│   ├── forms/              # Formulários
│   └── templates/          # Templates HTML
├── static/                 # Arquivos estáticos
│   ├── css/               # Estilos CSS
│   ├── js/                # Scripts JavaScript
│   └── img/               # Imagens
├── templates/             # Templates base
├── media/                 # Arquivos de mídia
└── manage.py             # Script de gerenciamento Django
```

## 📱 Funcionalidades Principais

### Autenticação
- Login local
- LDAP
- Azure AD
- Controle de permissões

### Gestão de Veículos
- Cadastro completo com informações detalhadas
- Importação em massa via Excel
- Filtros avançados de busca
- KPIs em tempo real

### Requisições
- Fluxo completo de requisição
- Aprovação automática configurável
- Validações de disponibilidade
- Controle de quilometragem

---

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📬 Contato

Wagner Hélio - wagner.helio@discente.ufg.br