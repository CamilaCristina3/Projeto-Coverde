from loja.models import Produto

def produto_detail(request, id):
    produto = Produto.objects.get(id=id)
    return render(request, 'loja/produto_detail.html', {'produto': produto})
