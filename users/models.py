import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    COMPANY = 'COMP'
    PRIVATE_PERSON = 'PRIV'
    COMPANY_PRIVATE = [
        (COMPANY, 'Компания'),
        (PRIVATE_PERSON, 'Частное лицо'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(verbose_name='Организация', max_length=250, null=True, blank=True)
    third_name = models.CharField(verbose_name='Отчество', max_length=250, null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=250, null=True, blank=True)
    status = models.CharField(verbose_name='Юр/Физлицо', max_length=50, choices=COMPANY_PRIVATE,
                              default=COMPANY)
    id_num = models.CharField(verbose_name='ИИН', max_length=15, default='000000000000', null=True, blank=True)
    email_corp = models.EmailField(verbose_name='Корпоративная почта', default='', null=True, blank=True)
    one_off = models.CharField(verbose_name='Одноразовый пароль', max_length=250, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images', null=True, verbose_name='Аватарка')


class Vacations(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    doc_name = models.CharField(verbose_name='Название документа', max_length=250)

    id_user = models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор пользователя')
    id_num = models.CharField(verbose_name='ИИН', max_length=15, default='000000000000', null=True, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=250)
    last_name = models.CharField(verbose_name='Фамилия', max_length=250)

    start_vacation = models.DateField(verbose_name='Начало отпуска', null=True)
    end_vacation = models.DateField(verbose_name='Окончание отпуска', null=True)

    doc_date = models.DateTimeField(verbose_name='Дата создания', null=True, blank=True)

    vacation_status = models.CharField(verbose_name='Статус', max_length=250)
    vacation_type = models.CharField(verbose_name='Тип отпуска', max_length=250)
    line_manager = models.CharField(verbose_name='Line Manager', max_length=250, default='')

    description = models.CharField(verbose_name='Описание/Номер', max_length=250, default='', null=True)
    decree = models.CharField(verbose_name='Приказ', max_length=250, default='', null=True)

    class Meta:
        verbose_name = 'Заявки на отпуск'
        verbose_name_plural = 'Заявки на отпуск'


class LogList(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)

    id_user = models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор пользователя')
    id_num = models.CharField(verbose_name='ИИН', max_length=15, default='000000000000', null=True, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=250)
    last_name = models.CharField(verbose_name='Фамилия', max_length=250)

    doc_name = models.CharField(verbose_name='Название документа', max_length=250)
    doc_date = models.DateTimeField(verbose_name='Дата создания', null=True)
    doc_status = models.CharField(verbose_name='Статус', max_length=250)
    description = models.CharField(verbose_name='Описание/Номер', max_length=250, default='', null=True)
    decree = models.CharField(verbose_name='Приказ', max_length=250, default='', null=True)
    tag = models.CharField(verbose_name='tag', max_length=250, default='')

    class Meta:
        verbose_name = 'Список логов'
        verbose_name_plural = 'Список логов'


class MawsEditStatus(models.Model):
    id = models.IntegerField(primary_key=True, unique=True, editable=False)

    id_user = models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор пользователя')

    user = models.CharField(verbose_name='Пользователь', max_length=250)
    storage = models.CharField(verbose_name='Склад', max_length=250)
    placement = models.CharField(verbose_name='Помещение', max_length=250)

    class Meta:
        verbose_name = 'Статусы помещений'
        verbose_name_plural = 'Статусы помещений'


class FormsMaws(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    id_user = models.UUIDField(default=uuid.uuid4, verbose_name='Идентификатор пользователя')
    name = models.TextField(verbose_name='Название', default='')

    goods = models.TextField(verbose_name='goods JSON', default='')
    responsibles = models.TextField(verbose_name='responsibles JSON', default='')

    location = models.CharField(verbose_name='Локация', max_length=250, default='')
    storage = models.CharField(verbose_name='Склад', max_length=250, default='')
    placement = models.CharField(verbose_name='Помещение', max_length=250, default='')
    manager = models.CharField(verbose_name='Менеджер склада', max_length=250, default='')
    date = models.CharField(verbose_name='Дата', max_length=250, default='')

    class Meta:
        verbose_name = 'Черновики МАФС'
        verbose_name_plural = 'Черновики МАФС'


class EditEmails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    email = models.EmailField(verbose_name='Новая почта', default='')
    v_code = models.CharField(verbose_name='Код подтверждения', default='', max_length=6)

    class Meta:
        verbose_name = 'Email verification'
        verbose_name_plural = 'Email verification'


class EditPhone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    id_num = models.CharField(verbose_name='ИИН', max_length=15, default='')
    phone = models.CharField(verbose_name='Новый телефон', default='', max_length=12)
    v_code = models.CharField(verbose_name='Код подтверждения', default='', max_length=6)

    class Meta:
        verbose_name = 'Phone verification'
        verbose_name_plural = 'Phone verification'


class PaySlip(models.Model):
    # file_pdf = models.FileField(upload_to='payslips')

    class Meta:
        verbose_name = 'Payslips'
        verbose_name_plural = 'Payslips'