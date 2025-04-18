from django.shortcuts import render

def upload_produto_view(request):
    if request.method == 'POST':
        # Lógica para upload de produto
        pass
    return render(request, 'loja/upload_produto.html')
