from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, 
    BaseUserManager, 
    PermissionsMixin,
    Group,
    Permission
)
from django.utils.text import slugify
from django.utils import timezone
from decimal import Decimal
from django.core.exceptions import ValidationError
from django.conf import settings

# === GERENCIADOR DE USUÁRIOS PERSONALIZADOS ===
class UserManager(BaseUserManager):
    def create_user(self, email, primeiro_nome, ultimo_nome, telemovel, password=None):
        if not email:
            raise ValueError("O email é obrigatório!")
        user = self.model(
            email=self.normalize_email(email),
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            telemovel=telemovel,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, primeiro_nome, ultimo_nome, telemovel, password=None):
        user = self.create_user(
            email=email,
            primeiro_nome=primeiro_nome,
            ultimo_nome=ultimo_nome,
            telemovel=telemovel,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# === FUNÇÕES DE UPLOAD ===
def user_directory_path(instance, filename):
    return f'uploads/profiles/{instance.id}/{filename}'

def product_image_upload_path(instance, filename):
    return f'uploads/products/{instance.produto.id}/{filename}'

# === MODELO PERSONALIZADO DE USUÁRIO ===
class User(AbstractBaseUser, PermissionsMixin):
    primeiro_nome = models.CharField(max_length=50, verbose_name="Primeiro Nome")
    ultimo_nome = models.CharField(max_length=50, verbose_name="Último Nome")
    telemovel = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telemóvel")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    profile_picture = models.ImageField(
        upload_to=user_directory_path, 
        blank=True, 
        null=True,
        verbose_name="Foto de Perfil"
    )
    localidade = models.CharField(max_length=255, blank=True, null=True, verbose_name="Localidade")
    cidade = models.CharField(max_length=255, blank=True, null=True, verbose_name="Cidade")
    cp = models.CharField(max_length=20, blank=True, null=True, verbose_name="Código Postal")
    biografia = models.TextField(blank=True, null=True, verbose_name="Biografia")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_staff = models.BooleanField(default=False, verbose_name="Equipe")
    is_superuser = models.BooleanField(default=False, verbose_name="Superusuário")
    date_joined = models.DateTimeField(default=timezone.now, verbose_name="Data de Registro")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["primeiro_nome", "ultimo_nome", "telemovel"]

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'loja_user'
        app_label = 'loja'

    def __str__(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"

    def get_full_name(self):
        return f"{self.primeiro_nome} {self.ultimo_nome}"

    def get_short_name(self):
        return self.primeiro_nome

    # Definindo related_names únicos para evitar conflitos
    groups = models.ManyToManyField(
        Group,
        verbose_name='Grupos',
        blank=True,
        help_text='Os grupos aos quais este usuário pertence.',
        related_name="loja_user_groups",
        related_query_name="loja_user_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='Permissões do usuário',
        blank=True,
        help_text='Permissões específicas para este usuário.',
        related_name="loja_user_permissions",
        related_query_name="loja_user_permission",
    )

# === CATEGORIA ===
class Categoria(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Nome")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'loja_categoria'
        app_label = 'loja'
        ordering = ['nome']

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            counter = 1
            while Categoria.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

# === PRODUTO ===
class Produto(models.Model):
    GRUPO_CHOICES = [
        ('legumes', 'Legumes'),
        ('horticolas', 'Hortícolas'),
        ('frutas', 'Frutas'),
        ('sementes', 'Sementes'),
        ('graos', 'Grãos'),
        ('flores', 'Flores'),
        ('outros', 'Outros'),
    ]

    nome = models.CharField(max_length=255, verbose_name="Nome")
    descricao = models.TextField(blank=True, null=True, verbose_name="Descrição")
    preco = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Preço"
    )
    categoria = models.ForeignKey(
        Categoria, 
        on_delete=models.CASCADE,
        verbose_name="Categoria"
    )
    grupo = models.CharField(
        max_length=15, 
        choices=GRUPO_CHOICES, 
        default='outros',
        verbose_name="Grupo"
    )
    quantidade_disponivel = models.PositiveIntegerField(
        verbose_name="Quantidade Disponível"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        db_table = 'loja_produto'
        app_label = 'loja'
        ordering = ['-criado_em']

    def clean(self):
        if self.preco <= Decimal(0):
            raise ValidationError("O preço deve ser maior que zero.")
        if self.quantidade_disponivel < 0:
            raise ValidationError("A quantidade disponível não pode ser negativa.")

    def __str__(self):
        return f"{self.nome} ({self.categoria.nome})"

# === IMAGENS DO PRODUTO ===
class ProdutoImagem(models.Model):
    produto = models.ForeignKey(
        Produto, 
        related_name="imagens", 
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )
    imagem = models.ImageField(
        upload_to=product_image_upload_path,
        verbose_name="Imagem"
    )

    class Meta:
        verbose_name = 'Imagem do Produto'
        verbose_name_plural = 'Imagens dos Produtos'
        db_table = 'loja_produto_imagem'
        app_label = 'loja'

    def __str__(self):
        return f"Imagem do produto: {self.produto.nome}"

# === CARRINHO ===
class Carrinho(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )
    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        verbose_name="Produto"
    )
    quantidade = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade"
    )
    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name="Total"
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'
        db_table = 'loja_carrinho'
        app_label = 'loja'
        unique_together = ('user', 'produto')
        ordering = ['-criado_em']

    def save(self, *args, **kwargs):
        self.total = self.produto.preco * Decimal(self.quantidade)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Carrinho de {self.user.get_full_name()} - Produto: {self.produto.nome}"

# === MENSAGEM DE CONTATO ===
class MensagemContato(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    mensagem = models.TextField(verbose_name="Mensagem")
    enviado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Enviado em"
    )

    class Meta:
        verbose_name = 'Mensagem de Contato'
        verbose_name_plural = 'Mensagens de Contato'
        db_table = 'loja_mensagem_contato'
        app_label = 'loja'
        ordering = ['-enviado_em']

    def __str__(self):
        return f"Mensagem de {self.nome} ({self.email})"

# === FORMULÁRIO DE CONTATO ===
class Contacto(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField(verbose_name="E-mail")
    mensagem = models.TextField(verbose_name="Mensagem")
    data_envio = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Envio"
    )

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        db_table = 'loja_contacto'
        app_label = 'loja'
        ordering = ['-data_envio']

    def __str__(self):
        return f"Contato de {self.nome} ({self.email})"