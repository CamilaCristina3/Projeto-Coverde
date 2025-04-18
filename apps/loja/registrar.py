from django.shortcuts import render, redirect
from loja.forms import RegistoForm  # Certifique-se de que o formulário existe e está correto
from django.contrib import messages

def Signup(request):
    """
    Permite que novos usuários se registrem no sistema.
    """
    if request.method == 'POST':
        form = RegistoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registro realizado com sucesso! Faça login para continuar.")
            return redirect('entrar')  # Redireciona para a página de login
    else:
        form = RegistoForm()

    return render(request, 'auth/registrar.html', {'form': form})
