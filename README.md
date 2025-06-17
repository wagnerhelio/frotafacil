# Projeto JFGO

## ✅ Requisitos
- Python 3.10+
- Git

## 🚀 Instalação

## Instalações Recomendadas no Ambiente 
``` bash
ms-python.vscode-python-envs
```
https://visualstudio.microsoft.com/visual-cpp-build-tools/
Clique em “Download Build Tools”.

Na instalação, selecione “C++ build tools”.

Marque também a opção “Windows 10 SDK” ou “Windows 11 SDK”, conforme seu sistema.

## Comandos Recorrentes de Desenvolvimento 

```bash
git clone https://github.com/seu-usuario/JFGO.git
```
```bash
python -m venv venv
```
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
```bash
.\venv\Scripts\Activate
```
```bash
pip install -r requirements.txt
```
```bash
python manage.py migrate
```
```bash
python manage.py createsuperuser
```
```bash
@"
AD_USER=jfgo\exemplo_svc_control_frota
AD_PASSWORD=exemplo_jfgo@1234
"@ | Out-File -Encoding UTF8 .env
```
```bash
cat <<EOF > .env
AD_USER=jfgo\exemplo_svc_control_frota
AD_PASSWORD=exemplo_jfgo@1234
EOF
```
```bash
AD_USER=jfgo\exemplo_svc_control_frota
AD_PASSWORD=exemplo_jfgo@1234
```
```bash
python manage.py runserver
```
```bash
python manage.py runserver 0.0.0.0:8000
```
```bash
http://127.0.0.1:8000/admin
```
```bash
http://srvlabdbdsv-go.go.trf1.gov.br:8000/
```
