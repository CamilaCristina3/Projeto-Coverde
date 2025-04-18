from django.shortcuts import render
from loja.models import User, Produto, Categoria  # Importações corrigidas

def Index(request):
    """
    Renderiza a página inicial com todos os produtos e categorias disponíveis.
    """
    # Obtendo todos os produtos e categorias disponíveis
    produtos = Produto.objects.all()
    categorias = Categoria.objects.all()

    contexto = {
        'produtos': produtos,
        'categorias': categorias,
    }
    return render(request, 'home/index.html', contexto)


def loja(request):
    """
    Renderiza a página da loja com produtos filtrados por categoria, se selecionada.
    """
    # Obtendo todas as categorias
    categorias = Categoria.objects.all()
    categoria_id = request.GET.get('categoria')  # Obtendo o ID da categoria a partir da URL

    # Filtrando os produtos com base na categoria
    if categoria_id:
        produtos = Produto.objects.filter(categoria_id=categoria_id)
    else:
        produtos = Produto.objects.all()  # Caso nenhuma categoria seja selecionada, retorna todos os produtos

    contexto = {
        'produtos': produtos,
        'categorias': categorias,
    }

    # Informando sobre o e-mail do usuário no console
    print(f"Usuário logado: {request.session.get('email')}")
    
    return render(request, 'loja/loja.html', contexto)

