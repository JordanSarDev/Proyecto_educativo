from django.test import TestCase

# Create your tests here.

from Sirac_users import models

class DocumentoModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        models.Documento.objects.create(name_T_Document='Cedula', acronym_D='C.C.')

    def test_acronym_D_label(self):
        documento = models.Documento.objects.get(id=1)
        field_label = documento._meta.get_field('acronym_D').verbose_name
        self.assertEquals(field_label,'Siglas de Documento')

    def test_acronym_D_max_length(self):
        documento=models.Documento.objects.get(id=1)
        max_length = documento._meta.get_field('acronym_D').max_length
        self.assertEquals(max_length,10)
        
class UsuarioModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        models.Documento.objects.create(name_T_Document='Cedula', acronym_D='C.C.')
        models.Rol.objects.create(name_R='Aprendiz')
        models.Usuario.objects.create(N_Documento='1922321123',first_name='Nicolas',F_last_name='Cortes', Phone_number='3223242899', Inst_mail='persona121@misena.edu.co',
            Documento=models.Documento.objects.get(id=1), Rol=models.Rol.objects.get(id=1))

    def test_user_creation(self):
        users = models.Usuario.objects.all()
        self.assertEquals(users.count(), 1)

        user = models.Usuario.objects.get(id=1)
        self.assertEquals(user.Inst_mail, "persona121@misena.edu.co")
        self.assertEquals(user.first_name, "Nicolas")