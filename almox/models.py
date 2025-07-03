from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    ST = [
        ('A','Ativo'),
        ('I', 'Inativo')
    ]
    
    nome = models.CharField(max_length = 100, unique = True)
    descricao = models.TextField()
    categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE)
    marca = models.ForeignKey("Marca", on_delete = models.CASCADE)
    quantidade_minima = models.IntegerField(default = 0)
    unidade = models.ForeignKey("Unidade", on_delete = models.CASCADE)
    status = models.CharField(max_length = 1, choices = ST)
    imagem = models.ImageField(upload_to="produtos/%Y/%m/%d/")
    observacao = models.TextField(blank = True)
    cod_bar = models.CharField(max_length = 14, unique = True, blank = True)
    
    def __str__(self):
        return self.nome 
    
class ItemProduto(models.Model):
    ST = [
        ('EST', 'Estoque'),
        ('PRO', 'Producao'),
        ('MAN', 'Manutencao'),
        ('VEN', 'Vendido'),
        ('BAI', 'Baixado')
    ]
    produto = models.ForeignKey(Produto, on_delete = models.CASCADE)
    data_aquisicao = models.DateField()
    data_entrada = models.DateTimeField()
    data_situacao = models.DateTimeField()
    data_garantia = models.DateField()
    numero_serie = models.CharField(max_length = 30)
    situacao = models.CharField(max_length = 3, choices = ST)
    localizacao = models.ForeignKey("Localizacao", on_delete = models.CASCADE)
    fornecedor = models.ForeignKey("Fornecedor", on_delete = models.CASCADE)
    custo = models.DecimalField(max_digits=9, decimal_places = 2)
    
    def __str__(self):
        return f'{self.produto.nome} - {self.numero_serie}'
      
class Categoria(models.Model):
    nome = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.nome
    
class Marca(models.Model):
    nome = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.nome
    
class Fornecedor(models.Model):
    nome = models.CharField(max_length = 30)
    
    def __str__(self):
        return self.nome
    
class Unidade(models.Model):
    nome = models.CharField(max_length = 20)
    sigla = models.CharField(max_length = 3)
    
    def __str__(self):
        return self.nome
    
class Localizacao(models.Model):
    responsavel = models.ForeignKey(User, on_delete = models.CASCADE)
    local = models.TextField()
    principal = models.BooleanField(default = False)
    producao = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.local} - {self.responsavel.username}'
        
class Movimentacao(models.Model):
    TIPO = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
        ('T', 'Transferência'),
        ('A', 'Altera Status')
    ]
    item_produto = models.ForeignKey(ItemProduto, on_delete = models.CASCADE)
    data = models.DateTimeField(auto_now_add = True)
    usuario = models.ForeignKey(User, on_delete = models.CASCADE)
    tipo_movimento = models.CharField(max_length = 1, choices = TIPO)
    responsavel = models.CharField(max_length=50, default = 'responsavel')
    local_origem = models.ForeignKey(Localizacao, on_delete = models.CASCADE, related_name = 'origem')
    local_destino = models.ForeignKey(Localizacao, on_delete = models.CASCADE, related_name='destino')
    
    
    def __str__(self):
        return f'{self.data} - {self.usuario.username} - {self.tipo_movimento} - {self.responsavel}'
    
class Pedido(models.Model):
    class Meta:
        permissions = [
            ('despachar', 'Pode despachar pedido'),
            ('entregar', 'Pode entregar pedido')
        ]
    STATUS = [
        ('ABE', 'Aberto'),
        ('AGU','Aguardando'),
        ('DEF', 'Deferido'),
        ('IND', 'Indeferido'),
        ('ENT', 'Entregue'),
    ]
    
    data_pedido = models.DateTimeField(auto_now_add = True)
    data_despacho = models.DateTimeField(blank = True, null=True)
    data_entrega = models.DateTimeField(blank = True, null = True)
    usuario_pedido = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'usuario_pedido')
    usuario_despacho = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, related_name = 'usuario_despacho', null = True)
    usuario_entrega = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, related_name = 'usuario_entrega', null = True)
    status = models.CharField(max_length = 3, choices = STATUS, default='ABE')
    recebido = models.BooleanField(default= False)
    
    def __str__(self):
        return f'{self.data_pedido.strftime('%d/%m/%Y')} - {self.usuario_pedido.username} - {self.status}'
    
class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete = models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete = models.CASCADE)
    entregue = models.BooleanField(default = False)