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

## Skills de agente (OpenCode)

O projeto inclui `AGENTS.md` com o fluxo de trabalho (escopo → fatia
end-to-end → testes → review → demo) e a skill local
`.opencode/skills/owasp-review/SKILL.md`.

Para UI, instale as skills uma vez na raiz do projeto (se já instalou
globalmente com `--global`/`-g`, pule este passo):

```powershell
npx.cmd impeccable install
npx.cmd skills add https://github.com/Leonxlnx/taste-skill --list
npx.cmd skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend -a opencode
```

No Linux/macOS, troque `npx.cmd` por `npx`.

- **Taste (`design-taste-frontend`)**: só quando a direção visual ainda está em
  aberto. Propõe duas opções e espera a escolha.
- **Impeccable**: implementa a direção escolhida e revisa layout, tipografia,
  formulários, foco e estados.
- **`owasp-review`**: revisa o diff quando pedido ou antes da demo, se tocar em
  permissões, dados sensíveis ou gravações críticas.

Exemplos de chamada:

1. “Use `design-taste-frontend` para propor duas direções compactas para esta
   tela. Descreva o layout, a densidade e a ação principal. Espere minha escolha.”
2. “Use `impeccable` para implementar a direção escolhida. Conecte a ação
   principal à API e mostre claramente o sucesso ou o erro. Rode o teste
   relevante.”
3. “Use `owasp-review` no diff atual. Reporte achados concretos com arquivo e
   linha.”

Peça as skills pelo nome no OpenCode. Se alguma não estiver instalada, o agente
deve avisar e aplicar o mesmo checklist manualmente.

## Segurança

O baseline e os riscos aceitos conscientemente (**ACK**) ficam em
[`SECURITY.md`](SECURITY.md). Rate limit, TLS e headers de proxy são
responsabilidade do nginx; o container escuta apenas em `127.0.0.1`.

## Deploy na VPS

O workflow [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) já vem
com estes valores preenchidos:

| Item | Valor |
| --- | --- |
| Host | `[[ vps_host ]]` |
| Usuário SSH | `[[ vps_user ]]` |
| Diretório | `[[ vps_path ]]` |
| Porta upstream | `[[ app_port ]]` (bind em `127.0.0.1`) |

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
- O container fica em `127.0.0.1:[[ app_port ]]`; coloque nginx/Caddy com TLS
  na frente e não exponha essa porta direto no firewall. Rate limit e TLS são
  responsabilidade do proxy.
[[#if database]]
- Para outro banco, defina `DATABASE_URL` no `.env` da VPS.
[[/if]]

## Estrutura

```text
.
├── AGENTS.md               # instruções para agentes
├── SECURITY.md             # baseline + riscos aceitos (ACK)
├── .opencode/skills/       # skill local owasp-review
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
