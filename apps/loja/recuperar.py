from django.shortcuts import render
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView

class RecuperarSenhaView(PasswordResetView):
    """
    Permite que os usuários iniciem o processo de recuperação de senha.
    """
    template_name = 'auth/recuperar_senha.html'
    form_class = PasswordResetForm
    email_template_name = 'auth/emails/recuperar_senha_email.html'
    success_url = '/entrar/'  # Redireciona para a página de login após o envio
