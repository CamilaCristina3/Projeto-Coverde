from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.loja.models import User, Produto, Categoria , ProdutoImagem, MensagemContato


def handler404(request, exception):
    return render(request, 'loja/errors/404.html', status=404)

def handler500(request):
    return render(request, 'loja/errors/500.html', status=500)

# === Detalhes do Produto ===
def produto_detail(request, id):
    """
    Exibe os detalhes de um produto específico.
    """
    produto = get_object_or_404(Produto, id=id)
    imagens = ProdutoImagem.objects.filter(produto=produto)  # Obtém as imagens relacionadas ao produto
    return render(request, 'produto.html', {
        'produto': produto,
        'imagens': imagens
    })

# === Mensagem de Contato ===
@login_required
def enviar_mensagem_contato(request):
    """
    Permite aos usuários autenticados enviar mensagens de contato.
    """
    if request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        mensagem = request.POST.get('mensagem')

        # Cria uma nova mensagem de contato no banco de dados
        MensagemContato.objects.create(nome=nome, email=email, mensagem=mensagem)

        return redirect('homepage')  # Redireciona para a homepage após o envio da mensagem

    return render(request, 'contacto.html')

