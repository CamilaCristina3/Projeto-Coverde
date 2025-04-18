from django.urls import path
from django.contrib.auth.views import LogoutView
from apps.loja import (
    home,
    login,
    logout,
    registrar,
    produto,
    pedidos,
    contacto,
    sobre,
    upload_product
)

app_name = 'loja'

urlpatterns = [
    # Página inicial
    path('', home.index_view, name='home'),
    
    # Autenticação
    path('login/', login.login_view, name='login'),
    path('registrar/', registrar.registrar_view, name='registrar'),
    path('logout/', logout.logout_view, name='logout'),
    
    # Produtos
    path('produto/<int:id>/', produto.produto_detail, name='produto_detail'),
    path('produto/upload/', upload_product.upload_product_view, name='upload_product'),
    
    # Pedidos
    path('pedidos/', pedidos.pedidos_view, name='pedidos'),
    
    # Páginas informativas
    path('sobre/', sobre.sobre_view, name='sobre'),
    path('contacto/', contacto.contacto_view, name='contacto'),
]