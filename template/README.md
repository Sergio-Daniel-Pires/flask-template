# [[ project_name ]]

Backend Flask + frontend React/Vite, gerado a partir de um template enxuto.

- API documentada em `/api/docs` (Swagger)
- Frontend React 19 + TypeScript, servido pelo Flask em produção
[[#if database]]
- SQLite via Flask-SQLAlchemy (exemplo de CRUD de notas)
[[/if]]
- pytest para a API e Playwright para o fluxo real no navegador
- Docker Compose para a VPS e deploy automático via GitHub Actions

## Requisitos

- Python 3.11+ ([uv](https://docs.astral.sh/uv/) é recomendado)
- Node.js 20+ (22 é o alvo)
- Docker + Docker Compose apenas para produção/deploy
- Git

## Rodando no Windows e no Linux

O projeto já vem com um `.env` local (chave secreta aleatória) e roda sem Docker.
Abra dois terminais.

### 1. Backend

```bash
uv sync --extra dev
uv run flask --app project.app run --debug
```

Sem `uv`:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
source .venv/bin/activate

pip install -e ".[dev]"
flask --app project.app run --debug
```

API em <http://localhost:5000>, documentação em
<http://localhost:5000/api/docs> e health check em
<http://localhost:5000/healthz>.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Abra <http://localhost:5173>. O Vite faz proxy de `/api` e `/healthz` para o
Flask na porta 5000.

### Produção local com Docker (opcional)

O projeto já vem com `.env` e uma chave secreta aleatória. Se estiver partindo de
um clone sem `.env`, crie a partir do exemplo e troque `FLASK_SECRET_KEY`:

```bash
cp .env.example .env   # Windows: Copy-Item .env.example .env
docker compose up -d --build
```

A aplicação fica em <http://localhost:[[ app_port ]]>.

## Banco de dados

[[#if database]]
SQLite é o padrão, em `instance/app.db`, via Flask-SQLAlchemy. O
`DATABASE_URL` permite trocar o banco sem mexer no código:

```bash
# SQLite relativo à pasta instance/ (padrão)
DATABASE_URL=sqlite:///app.db

# PostgreSQL (instale o driver, por exemplo: uv add psycopg[binary])
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/app
```

Rotas de exemplo:

- `GET /api/notes/` lista as notas
- `POST /api/notes/` cria uma nota com `{"text": "..."}`

O template usa `db.create_all()` na inicialização para manter o primeiro contato
simples. Quando o schema começar a evoluir, troque por migrações (Flask-Migrate
ou Alembic).

[[/if]]

[[#if database]]
Não use o banco de exemplo como modelo para dados sensíveis:
ele existe para demonstrar a integração ponta a ponta.
[[/if]]

## Testes

Backend:

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest --cov=project --cov-report=term-missing
```

Frontend:

```bash
cd frontend
npm run typecheck
npm run build
```

Playwright (Chromium headless):

```bash
cd frontend
npx playwright install --only-shell chromium   # primeira vez
npm run test:e2e
```

`npm run test:e2e` testa o caminho de produção: build do Vite servido pelo Flask
em uma porta isolada (5050), incluindo fallback de SPA.

Para o loop mais rápido, deixe `uv run flask ...` e `npm run dev` rodando e use:

```bash
npm run test:e2e:dev
```

Nesse modo os servidores de desenvolvimento são reaproveitados, sem rebuild.

## Deploy na VPS

O workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) já vem
com estes valores preenchidos:

| Item | Valor |
| --- | --- |
| Host | `[[ vps_host ]]` |
| Usuário SSH | `[[ vps_user ]]` |
| Diretório | `[[ vps_path ]]` |
| Porta pública | `[[ app_port ]]` |

1. Gere uma chave SSH para o deploy e autorize a pública na VPS:

   ```bash
   ssh-keygen -t ed25519 -C "github-actions-[[ project_name ]]" -f deploy_key
   ssh-copy-id -i deploy_key.pub [[ vps_user ]]@[[ vps_host ]]
   ```

2. No GitHub, em **Settings → Secrets and variables → Actions**, crie:

   - `VPS_SSH_KEY`: conteúdo da chave privada (`deploy_key`)
   - `VPS_FINGERPRINT` (opcional, recomendado): fingerprint do host. Na VPS:

     ```bash
     ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
     ```

3. Na VPS, rode o setup uma única vez:

   ```bash
   git clone [[ repo_url ]] [[ vps_path ]]
   cd [[ vps_path ]]
   bash deploy/setup-vps.sh
   ```

   O script instala Docker (quando necessário), cria o `.env` com uma chave
   secreta aleatória e sobe os containers.

4. A partir daí, cada push em `main` faz `git fetch/reset`, rebuild da imagem e
   health check. O workflow usa o environment `production`; você pode exigir
   aprovação manual nas configurações do repositório.

Observações:

- O `.env` da VPS não é versionado e sobrevive ao `git reset --hard`.
- Repositório privado: configure uma deploy key com acesso de leitura na VPS
  (ou clones via HTTPS com token) para o `git fetch` funcionar.
- Libere a porta `[[ app_port ]]` no firewall/security group da VPS.
[[#if database]]
- Para outro banco, defina `DATABASE_URL` no `.env` da VPS.
[[/if]]

## Estrutura

```text
.
├── project/
│   ├── app.py              # factory + serving do build do frontend
│   ├── config.py           # settings por ambiente
│   ├── wsgi.py             # entrypoint do Gunicorn
│   └── services/           # home, echo
[[#if database]]
│       └── notes/          # exemplo SQLite
[[/if]]
├── frontend/
│   ├── src/                # páginas e componentes React
│   └── e2e/                # testes Playwright
├── tests/                  # testes pytest da API
├── deploy/setup-vps.sh
├── .github/workflows/      # CI e deploy
├── Dockerfile
└── docker-compose.yml
```

## Variáveis de ambiente

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `FLASK_ENV` | `development` | `production` exige `FLASK_SECRET_KEY` |
| `FLASK_SECRET_KEY` | — | obrigatória em produção |
[[#if database]]
| `DATABASE_URL` | `sqlite:///.../instance/app.db` | conexão SQLAlchemy |
[[/if]]
| `FRONTEND_DIST` | `frontend/dist` | pasta do build servido pelo Flask |
| `GUNICORN_BIND` | `0.0.0.0:8000` | bind do Gunicorn |
| `GUNICORN_WORKERS` | `2` | workers |
| `GUNICORN_TIMEOUT` | `60` | timeout em segundos |

O frontend aceita `VITE_API_URL` se você quiser apontar para outra API; o padrão
é `/api`.

---

Gerado por `flask-template` — [[ year ]].
