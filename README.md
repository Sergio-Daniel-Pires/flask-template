# Flask + React template

Template de projeto com backend Flask, frontend React/Vite, testes, Docker e
deploy automático para uma VPS via GitHub Actions.

O repositório não é a aplicação em si: ele gera uma **nova pasta de projeto**
já configurada com nome, autor, porta e host da VPS.

## Requisitos

- Python 3.11+ (para gerar e rodar o backend)
- Node.js 20+ (para o frontend)
- [uv](https://docs.astral.sh/uv/) (recomendado) ou `pip`
- Docker + Docker Compose (opcional, apenas para produção/local em container)
- Git (opcional, para inicializar o projeto)

O gerador usa apenas a biblioteca padrão do Python.

## Criar um projeto

```bash
python create_project.py \
  --name minha-api \
  --vps-host 203.0.113.10 \
  --port 8000
```

No Windows (PowerShell), a mesma coisa em uma linha:

```powershell
python create_project.py --name minha-api --vps-host 203.0.113.10 --port 8000
```

Isso cria `../minha-api` (uma pasta irmã do template) com:

- `.env` local já preenchido com uma chave secreta aleatória
- repositório git inicializado em `main`
- host, usuário, caminho e porta da VPS já aplicados no workflow de deploy

### Opções

| Opção | Padrão | Descrição |
| --- | --- | --- |
| `-n, --name` | obrigatório | Nome em kebab-case (`minha-api`) |
| `--path` | `../<name>` | Pasta de destino |
| `-a, --author` | `git config user.name` | Autor no `pyproject.toml` |
| `-e, --email` | `git config user.email` | E-mail no `pyproject.toml` |
| `--vps-host` | obrigatório | Host/IP gravado no workflow de deploy |
| `--vps-user` | `root` | Usuário SSH do deploy |
| `--vps-path` | `/opt/<name>` | Pasta do projeto na VPS |
| `--port` | `8000` | Porta pública na VPS |
| `--repo-url` | inferido do `origin` | URL usada pelo script de setup da VPS |
| `--no-git-init` | desligado | Não roda `git init` |

## Desenvolvimento do template

O conteúdo gerado fica em [`template/`](template/). Para testar uma alteração:

```bash
python create_project.py -n sample-app --vps-host 203.0.113.10 --no-git-init
cd ../sample-app
uv sync --extra dev
uv run pytest
cd frontend && npm install && npm run build
```

O workflow [`template-ci.yml`](.github/workflows/template-ci.yml) faz exatamente
isso a cada push.

## Estrutura

```text
.
├── create_project.py        # gerador (sem dependências)
├── template/                # arquivos copiados para o projeto novo
│   ├── project/             # backend Flask (factory + services)
│   ├── frontend/            # React + Vite
│   ├── tests/
│   ├── deploy/              # setup inicial da VPS
│   └── .github/workflows/   # CI e deploy do projeto gerado
└── .github/workflows/       # CI do próprio template
```
