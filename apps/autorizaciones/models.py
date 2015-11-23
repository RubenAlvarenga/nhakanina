from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from apps.thumbs import ImageWithThumbsField
from django.contrib.auth.models import Permission

num2words1 = {1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 10: 'Ten', 11: 'Eleven', 12: 'Twelve', 13: 'Thirteen', 14: 'Fourteen', 15: 'Fifteen', 16: 'Sixteen', 17: 'Seventeen', 18: 'Eighteen', 19: 'Nineteen'}
num2words2 = ['Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']
def number(Number):
    if (Number > 1) or (Number < 19):
        return (num2words1[Number])
    elif (Number > 20) or (Number < 99):
        return (num2words2[Number])



# class Impresoras(models.Model):
#     nombre = models.CharField(max_length=100, verbose_name='Nombre')
#     class Meta:
#         verbose_name = ('impresora')
#         verbose_name_plural = ('impresoras')
#         default_permissions = ('add', 'change', 'delete', 'view', 'list')
#     def __unicode__(self):
#         return '%s' % (self.nombre)


class Perfil(models.Model):
    user=models.OneToOneField(User)
    avatar=ImageWithThumbsField(upload_to='avatar_user/',  null=True, blank=True, verbose_name='avatar', sizes=((125,125),(30,30)))
    impresora = models.CharField(max_length=100, verbose_name='Impresora', null=True, blank=True)



    class Meta:
        verbose_name = ('perfil')
        verbose_name_plural = ('perfiles')
        default_permissions = ('add', 'change', 'delete', 'view', 'list')
    def __unicode__(self):
        return '%s' % (self.user.username)



from django.dispatch import receiver
@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)

post_save.connect(ensure_profile_exists, sender=User)





class MenuApp(models.Model):
    titulo = models.CharField(max_length=100, verbose_name='Titulo')
    app_name = models.CharField(max_length=100, verbose_name='App Name', unique=True,)
    icono = models.CharField(max_length=100)
    index = models.CharField(max_length=200, verbose_name='Index')
    class Meta:
        verbose_name = 'App'
        verbose_name_plural = 'Apps'
    def __unicode__(self):
        return '%s' % (self.titulo)

class Agrupador(models.Model):
    grupo = models.CharField(max_length=100, verbose_name='Grupo')
    icono = models.CharField(max_length=100)
    class Meta:
        verbose_name = 'Grupo Menu'
        verbose_name_plural = 'Grupos de Menus'
    def __unicode__(self):
        return '%s' % (self.grupo)


class Enlace(models.Model):
    app = models.ForeignKey(MenuApp, verbose_name='App', on_delete=models.PROTECT)
    grupo = models.ForeignKey(Agrupador, verbose_name='Grupo', on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100, verbose_name='Titulo')
    enlace = models.CharField(max_length=200, verbose_name='Enlace')
    permiso = models.ForeignKey(Permission, verbose_name='Permiso')
    class Meta:
        verbose_name = 'Enlace'
        verbose_name_plural = 'Enlaces'
        #unique_together = (('app', 'grupo', 'enlace' ),)
    def __unicode__(self):
        return '%s' % (self.nombre)
