from django.shortcuts import render, redirect
from loja.forms import ContactoForm  # Certifique-se de que o formulário está configurado corretamente
from django.contrib import messages

def ContactoView(request):
    """
    Permite ao usuário enviar mensagens de contato por meio de um formulário.
    """
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()  # Salva os dados do formulário no banco de dados
            # Mensagem de sucesso para o usuário
            messages.success(request, "Mensagem enviada com sucesso! Entraremos em contato em breve.")
            return redirect('homepage')  # Redireciona o usuário para a página inicial
    else:
        form = ContactoForm()  # Cria um formulário vazio para exibição inicial

    # Renderiza o template com o formulário
    return render(request, 'contacto/contacto.html', {'form': form})

