# Lume 3D — Deploy Unificado (Django + React no Render)

## Visão geral

Frontend React e backend Django hospedados no **mesmo serviço no Render**.
O Django serve a SPA React como arquivos estáticos e responde às rotas `/api/*`.

```
Render Web Service
├── /api/*           → Django (Python)
├── /admin/          → Django Admin
├── /webhooks/*      → Stripe webhook
└── /*               → React SPA (index.html servido pelo Django)
```

---

## Deploy no Render (primeira vez)

### 1. Faça fork / push do projeto

Certifique-se de que o repositório tem esta estrutura na raiz:

```
build.sh
render.yaml
requirements.txt
django_min/
frontend/
```

### 2. Crie o serviço no Render

**Opção A — via render.yaml (recomendado):**
- No dashboard do Render, clique em **New → Blueprint**
- Aponte para o repositório — o `render.yaml` cria o serviço e o banco automaticamente

**Opção B — manual:**
- **New → Web Service** → conecte o repositório
- Runtime: **Python**
- Build Command: `./build.sh`
- Start Command: `cd django_min && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### 3. Configure as variáveis de ambiente

| Variável | Valor |
|---|---|
| `DATABASE_URL` | String de conexão do PostgreSQL (gerado pelo Render) |
| `DJANGO_SECRET_KEY` | Chave secreta longa e aleatória |
| `DEBUG` | `False` |
| `SITE_URL` | `https://nome-do-seu-app.onrender.com` |
| `STRIPE_SECRET_KEY` | *(opcional)* Chave do Stripe |
| `STRIPE_WEBHOOK_SECRET` | *(opcional)* Secret do webhook do Stripe |

### 4. Deploy

Clique em **Deploy** — o Render vai:
1. Instalar dependências Python
2. Instalar Node e buildar o React (`npm ci && npm run build`)
3. Copiar o `dist/` para `django_min/spa/`
4. Rodar `migrate`, `collectstatic` e `seed_catalogo`
5. Iniciar o Gunicorn

---

## Desenvolvimento local

### Backend (Django)

```bash
cd django_min
cp ../.env.example ../.env   # preencha DATABASE_URL
pip install -r ../requirements.txt
python manage.py migrate
python manage.py seed_catalogo
python manage.py runserver
```

### Frontend (React)

```bash
cd frontend
npm install
# O proxy já está configurado no vite.config.ts para http://localhost:8000
npm run dev
```

O React vai rodar em `http://localhost:8080` e redirecionar `/api/*` para o Django em `8000`.

---

## Estrutura dos arquivos modificados

```
├── build.sh                         ← build unificado (Python + Node)
├── render.yaml                      ← configuração de deploy automático
├── .env.example                     ← variáveis necessárias
├── django_min/
│   ├── config/
│   │   ├── settings.py              ← whitenoise, SPA_DIR, CSRF ajustado
│   │   └── urls.py                  ← catch-all para o React
│   └── core/
│       ├── models.py                ← + campos slug, tag, specs
│       ├── views.py                 ← auth real + todos os endpoints API
│       ├── urls.py                  ← rotas /api/*
│       └── migrations/0004_...py   ← migration dos novos campos
│       └── management/commands/
│           └── seed_catalogo.py     ← produtos reais do frontend
└── frontend/
    ├── vite.config.ts               ← proxy /api → Django em dev
    ├── .env.example
    └── src/
        ├── lib/api.ts               ← camada centralizada de API
        ├── contexts/
        │   ├── AuthContext.tsx      ← auth real (sessão Django)
        │   └── CartContext.tsx      ← carrinho sincronizado com backend
        └── pages/
            ├── Index.tsx            ← catálogo da API + fallback local
            ├── LoginPage.tsx        ← login real
            ├── SignupPage.tsx       ← cadastro real
            └── ProfilePage.tsx     ← logout assíncrono
        └── components/account/
            └── Orders.tsx           ← pedidos reais do backend
```

---

## APIs disponíveis

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/csrf/` | Inicializa cookie CSRF |
| GET | `/api/me/` | Usuário autenticado atual |
| POST | `/api/login/` | Login com e-mail/senha |
| POST | `/api/signup/` | Criação de conta |
| POST | `/api/logout/` | Logout |
| GET | `/api/catalogo/` | Lista produtos ativos |
| GET | `/api/carrinho/` | Carrinho do usuário |
| POST | `/api/carrinho/adicionar/` | Adiciona item |
| POST | `/api/carrinho/atualizar/` | Atualiza quantidade |
| POST | `/api/carrinho/remover/` | Remove item |
| POST | `/api/carrinho/limpar/` | Limpa carrinho |
| GET | `/api/pedidos/` | Lista pedidos do usuário |
| POST | `/api/checkout/` | Inicia checkout Stripe |
| POST | `/webhooks/stripe/` | Webhook de pagamento |
| GET | `/health/` | Health check |
