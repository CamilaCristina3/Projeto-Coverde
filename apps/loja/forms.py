from django import forms
from loja.models import Produto, Contacto  # Adicionado Contacto ao lado de Produto
from decimal import Decimal

class ProdutoForm(forms.ModelForm):
    """
    Formulário para criar ou editar produtos.
    """

    preco = forms.CharField(label="Preço (€)", required=True)

    class Meta:
        model = Produto  # Modelo vinculado ao formulário
        fields = ["nome", "preco", "categoria", "descricao"]  # Campos do formulário

    def clean_preco(self):
        """
        Valida o campo preço, convertendo para decimal e aplicando regras de negócio.
        """
        preco = self.cleaned_data["preco"].replace(",", ".")  # Converte vírgulas para pontos
        try:
            preco = Decimal(preco)
        except ValueError:
            raise forms.ValidationError("Por favor, insira um valor numérico válido.")

        if preco > Decimal("99999.99"):  # Restrição de preço máximo
            raise forms.ValidationError("O preço não pode ser maior que 99999,99.")

        return preco


class ContactoForm(forms.ModelForm):
    """
    Formulário para envio de mensagens de contato.
    """
    class Meta:
        model = Contacto  # Modelo vinculado ao formulário
        fields = ["nome", "email", "mensagem"]  # Campos do formulário

    def clean_email(self):
        """
        Valida o campo email para garantir que o formato é correto.
        """
        email = self.cleaned_data.get("email")
        if not email or "@" not in email:
            raise forms.ValidationError("Por favor, insira um endereço de email válido.")
        return email
