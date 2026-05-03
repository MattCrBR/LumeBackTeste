from django.urls import path
from core.views import (
    csrf_token_view,
    api_me,
    api_login,
    api_signup,
    api_logout,
    api_catalogo,
    api_carrinho,
    api_adicionar_carrinho,
    api_atualizar_carrinho,
    api_remover_carrinho,
    api_limpar_carrinho,
    api_pedidos,
    api_checkout,
    api_checkout_status,
    stripe_webhook,
    health,
)

urlpatterns = [
    path("api/csrf/", csrf_token_view),

    path("api/me/", api_me),
    path("api/login/", api_login),
    path("api/signup/", api_signup),
    path("api/logout/", api_logout),

    path("api/catalogo/", api_catalogo),

    path("api/carrinho/", api_carrinho),
    path("api/carrinho/adicionar/", api_adicionar_carrinho),
    path("api/carrinho/atualizar/", api_atualizar_carrinho),
    path("api/carrinho/remover/", api_remover_carrinho),
    path("api/carrinho/limpar/", api_limpar_carrinho),

    path("api/pedidos/", api_pedidos),

    path("api/checkout/", api_checkout),
    path("api/checkout/status/", api_checkout_status),

    path("webhooks/stripe/", stripe_webhook),
    path("health/", health),
]
