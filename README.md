# FrotaFácil

Sistema moderno de gestão de frota desenvolvido em Django, com foco em padronização, responsividade, integração de dados e fluxo de requisições.

## 📌 Funcionalidades

- **Gestão de Veículos**
  - Cadastro completo de veículos com informações detalhadas
  - Importação em massa via planilha Excel
  - Listagem com filtros avançados
  - KPIs em tempo real

- **Requisições de Viatura/Motorista**
  - Fluxo completo de requisição, aprovação e finalização
  - Aprovação automática configurável
  - Validações de disponibilidade e conflitos
  - Controle de quilometragem com alertas de divergência

- **Autenticação e Segurança**
  - Suporte a login local
  - Integração com LDAP
  - Autenticação via Azure AD
  - Controle de permissões por nível de acesso

- **Interface Moderna**
  - Design responsivo
  - Menu lateral retrátil
  - KPIs visuais
  - Mensagens de feedback coloridas

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

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/frotafacil.git
cd frotafacil
```

2. Crie e ative o ambiente virtual:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## ⚙️ Configuração

### Variáveis de Ambiente (.env)

```env
# Configurações do Django
SECRET_KEY=sua-chave-secreta
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações do Azure AD
AZURE_TENANT_ID=seu-tenant-id
AZURE_CLIENT_ID=seu-client-id
AZURE_CLIENT_SECRET=seu-client-secret
AZURE_RESOURCE=seu-resource
AZURE_RELYING_PARTY_ID=seu-relying-party-id
AZURE_AUDIENCE=seu-audience

# Configurações do LDAP
LDAP_SERVER=seu-servidor-ldap
LDAP_PORT=389
LDAP_BASE_DN=dc=exemplo,dc=com,dc=br
```

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

### Autenticação
- Login local
- LDAP
- Azure AD
- Controle de permissões

## 🤝 Contribuindo

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 📬 Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/frotafacil](https://github.com/seu-usuario/frotafacil)

## 🙏 Agradecimentos

- [Django](https://www.djangoproject.com/)
- [Bootstrap](https://getbootstrap.com/)
- [Azure AD](https://azure.microsoft.com/)
- [LDAP](https://www.openldap.org/)
