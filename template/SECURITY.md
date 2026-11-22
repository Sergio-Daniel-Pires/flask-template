# Segurança

Este projeto é um starter de demonstração para iteração rápida. Este documento
registra o que foi corrigido e o que foi **aceito conscientemente** (ACK).

## Baseline aplicado

- `FLASK_ENV` validado contra `development`, `test` e `production`; valores
  desconhecidos falham em vez de cair silenciosamente em development.
- Produção exige `FLASK_SECRET_KEY` com pelo menos 32 caracteres e rejeita
  placeholders como `change-me`.
- Corpo da requisição limitado a 1 MiB; echo limitado a 10.000 caracteres e
  notas a 500 caracteres.
- O container publica a porta apenas em `127.0.0.1`; TLS e rate limit ficam no
  nginx/proxy.
- Headers básicos: `X-Content-Type-Options`, `X-Frame-Options` e
  `Referrer-Policy`.
- SQLAlchemy/ORM, sem SQL concatenado. React escapa o conteúdo das notas.
- Docker roda como usuário não-root; a VPS gera `.env` com segredo aleatório e
  aplica `chmod 600`.

## Riscos aceitos (ACK)

| ID | Item | Decisão | Motivo | Mitigação atual | Revisar quando |
| --- | --- | --- | --- | --- | --- |
| ACK-001 | Rate limit | Fora do app; responsabilidade do nginx/proxy. | Evita dependência e complexidade no starter. | Porta bindada em `127.0.0.1`; proxy na frente. | Se o proxy sair do caminho ou houver exposição direta. |
| ACK-002 | Deploy SSH como `root` | Aceito; é configuração da máquina e não será alterada aqui. | O ambiente da VPS já é assim. | Chave dedicada, `VPS_SSH_KEY` em secret e fingerprint quando configurado. | Se a VPS permitir usuário de deploy com acesso ao Docker. |
| ACK-003 | API de notas pública | Aceito para demo. | O projeto é um starter sem identidade. | Não armazenar dados pessoais/sensíveis; uso local ou demo. | Antes de qualquer uso real ou dado de terceiros. |
| ACK-004 | TLS | Fora do app; terminação no nginx/proxy. | O pacote não deve embutir um proxy. | Container não é exposto diretamente. | Antes de acessar pela internet pública. |
| ACK-005 | Swagger público | Aceito para demo. | Ajuda a inspecionar a API durante a entrevista. | Nenhuma escrita privilegiada; endpoints são de exemplo. | Em produção real, proteger ou desativar `/api/docs`. |
| ACK-006 | CSP/HSTS | Delegado ao nginx/proxy. | CSP precisa conhecer o domínio e os assets do proxy. | Headers básicos no Flask. | Ao configurar o domínio e TLS. |
| ACK-007 | Actions por tag | Aceito no template. | Atualizações automáticas de segurança são desejáveis. | `permissions: contents: read`; secrets isolados. | Em repositório de alta assurance, pinar por SHA. |
| ACK-008 | Docker via `curl \| sh` | Aceito no bootstrap da VPS. | Setup rápido de uma máquina de demo. | Script roda só uma vez na configuração inicial. | Em ambiente hardened, usar pacote/checksum verificado. |
| ACK-009 | Docker usa `pip`, não `uv.lock` | Aceito para simplicidade. | O starter prioriza iteração rápida. | Dependências têm faixas no `pyproject.toml`. | Quando reprodutibilidade estrita for necessária. |
| ACK-010 | Notas sem paginação | Aceito para demo. | Volume pequeno, sem usuários reais. | Limite de 500 caracteres por nota. | Antes de crescer o volume de dados. |
| ACK-011 | Sem autenticação/identidade | Fora do escopo do starter. | Entrevista rápida, sem dados reais. | Não armazenar PII; API é de exemplo. | Antes de qualquer funcionalidade com dados de usuário. |
| ACK-012 | Fingerprint SSH opcional | Aceito para demo. | Nem toda VPS tem o secret configurado de início. | `VPS_FINGERPRINT` documentado; configure-o no deploy real. | Antes de qualquer deploy em produção. |

## Como registrar um novo ACK

Ao decidir não corrigir um achado, adicione uma linha à tabela acima com:

- ID sequencial;
- item e arquivo/rota afetados;
- motivo da decisão;
- mitigação atual;
- gatilho para revisitar.

Achados de segurança **não podem ser ignorados silenciosamente**. Se a decisão
for corrigir, registre o teste que cobre a correção. Se for aceitar, registre o
ACK. Nunca inclua segredos, tokens ou dados pessoais neste arquivo.

## Revisão

Última revisão: 2026-11-22. Revisar antes de armazenar dados pessoais, adicionar
autenticação, expor o serviço publicamente ou aumentar o volume de dados.
