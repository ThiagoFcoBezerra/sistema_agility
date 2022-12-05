from models import Autorizacao
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

content_type = ContentType.objects.get_for_model(Autorizacao)
permission = Permission.objects.create(
    codename='despachar',
    name='Permite despachar',
    content_type=content_type,
)