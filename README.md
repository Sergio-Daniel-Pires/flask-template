# Flask + React template

Template que gera um projeto completo com **Flask**, **React/Vite**,
**SQLite (opcional)**, testes e deploy automático para uma VPS via GitHub
Actions.

O repositório não é a aplicação em si: ele gera uma **pasta nova** já
configurada com nome, autor, porta e host da VPS. O gerador usa apenas a
biblioteca padrão do Python — não precisa instalar nada para criar o projeto.

> Não há MongoDB por padrão (nem nenhum banco). O padrão é **SQLite** via
> Flask-SQLAlchemy, e `--database none` gera o projeto sem banco.

## Requisitos

- Python 3.11+ (para gerar e rodar o backend)
- Node.js 20+ (para o frontend)
- [uv](https://docs.astral.sh/uv/) (recomendado) ou `pip`
- Docker + Docker Compose (apenas para produção/deploy)
- Git (opcional, para inicializar o projeto)

## Criar um projeto

```bash
python create_project.py \
  --name minha-api \
  --vps-host 203.0.113.10 \
  --port 8000
```

No Windows (PowerShell), em uma linha:

```powershell
python create_project.py --name minha-api --vps-host 203.0.113.10 --port 8000
```

Isso cria `../minha-api` (pasta irmã do template) com:

- `.env` local já preenchido com uma chave secreta aleatória
- repositório git inicializado em `main`
- host, usuário, caminho e porta da VPS aplicados no workflow de deploy
- frontend, backend, testes e CI prontos para rodar

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
| `--port` | `8000` | Porta upstream na VPS (bind em `127.0.0.1`) |
| `--repo-url` | inferido do `origin` | URL usada pelo setup da VPS |
| `--database` | `sqlite` | `sqlite` inclui o exemplo de CRUD; `none` remove |
| `--no-git-init` | desligado | Não roda `git init` |

## Rodar o projeto gerado

Backend:

```bash
cd ../minha-api
uv sync --extra dev
uv run flask --app project.app run --debug
```

Frontend (outro terminal):

```bash
cd frontend
npm install
npm run dev
```

- Frontend: <http://localhost:5173>
- API: <http://localhost:5000>
- Swagger: <http://localhost:5000/api/docs>
- Health: <http://localhost:5000/healthz>

Sem `uv`, use `python -m venv .venv`, ative o venv e rode
`pip install -e ".[dev]"`. O README gerado tem o passo a passo para Windows e
Linux.

## O que vem no projeto

- **Backend**: app factory, settings por ambiente, `/api` versionável, erros
  HTTP corretos, Swagger e `/healthz`.
- **Frontend**: React 19 + TypeScript + React Router, páginas de exemplo e
  proxy `/api` no Vite.
- **Banco**: SQLite em `instance/app.db` (Flask-SQLAlchemy) com CRUD de notas;
  `DATABASE_URL` troca para Postgres/MySQL.
- **Testes**: pytest para a API e Playwright (Chromium headless) para o fluxo
  real no navegador.
- **Docker**: imagem multi-stage (React build + Gunicorn), non-root, healthcheck
  e volume para o SQLite.
- **CI**: lint, typecheck, testes, Playwright e smoke test da imagem.
- **Deploy**: SSH + `docker compose up -d --build`, com health check.
- **Segurança**: `SECURITY.md` com baseline e ACKs explícitos; a skill OWASP
  exige ACK para achado aceito, em vez de ignorar.

### Playwright rápido

A suíte tem 3 testes e roda em Chromium headless:

```bash
cd frontend
npx playwright install --only-shell chromium   # primeira vez
npm run test:e2e        # build + Flask na porta 5050 (caminho de produção)
npm run test:e2e:dev    # reaproveita Flask + Vite já rodando (loop rápido)
```

O modo `test:e2e` valida o build real servido pelo Flask, incluindo deep link da
SPA. O modo `test:e2e:dev` é o mais rápido no dia a dia: se os dois servidores de
desenvolvimento já estiverem rodando, não há build nem espera de startup.

## Desenvolvimento do template

O conteúdo gerado fica em [`template/`](template/). Para testar uma alteração:

```bash
python create_project.py -n sample-app --vps-host 203.0.113.10 --no-git-init
cd ../sample-app
uv sync --extra dev
uv run ruff check .
uv run ruff format --check .
uv run pytest
cd frontend && npm ci && npm run typecheck && npm run test:e2e
```

O workflow [`template-ci.yml`](.github/workflows/template-ci.yml) gera o projeto
com e sem banco e roda backend, frontend e Playwright.

## Deploy

O workflow gerado (`.github/workflows/deploy.yml`) já contém host, usuário,
diretório e porta. Basta configurar no GitHub:

- `VPS_SSH_KEY` (secret obrigatório): chave privada SSH
- `VPS_FINGERPRINT` (secret opcional, recomendado): fingerprint do host

Na VPS, rode `bash deploy/setup-vps.sh` uma vez; depois cada push em `main`
atualiza o projeto. O `.env` da VPS é preservado entre deploys.

## Agentes e skills

- `AGENTS.md` na raiz: regras para trabalhar no próprio template (gerar as duas
  variantes, validar e atualizar o PR).
- `template/AGENTS.md`: instruções que nascem na raiz de cada projeto gerado —
  stack, comandos, loop de escopo/implementação/testes e definição de pronto.
- `.opencode/skills/owasp-review`: skill local de revisão de segurança do diff.
- Achados aceitos são registrados em `template/SECURITY.md` (ACK), não
  silenciados.
- UI: **Taste** só para explorar duas direções; **Impeccable** para implementar a
  direção escolhida. As instruções de instalação estão no README gerado.

## Estrutura

```text
.
├── AGENTS.md                # instruções para agentes neste repo
├── create_project.py        # gerador (sem dependências)
├── .opencode/skills/        # skill local de review OWASP
├── template/                # arquivos copiados para o projeto novo
│   ├── AGENTS.md            # instruções do projeto gerado
│   ├── SECURITY.md          # baseline + riscos aceitos (ACK)
│   ├── project/             # backend Flask (factory + services)
│   ├── frontend/            # React + Vite + Playwright
│   ├── tests/
│   ├── deploy/              # setup inicial da VPS
│   └── .github/workflows/   # CI e deploy do projeto gerado
└── .github/workflows/       # CI do próprio template
```
