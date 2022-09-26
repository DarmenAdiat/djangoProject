import uuid

from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from .models import Vacations, LogList, MawsEditStatus, FormsMaws, EditEmails, EditPhone
import random
from django.core.mail import send_mail
from lk.settings import DEFAULT_FROM_EMAIL
from django.contrib.auth import password_validation
from django.utils.translation import gettext_lazy as _


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                _('Your old password was entered incorrectly. Please enter it again.')
            )
        return value

    def validate(self, data):
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({'new_password2': _("The two password fields didn't match.")})
        password_validation.validate_password(data['new_password1'], self.context['request'].user)
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password1']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class CheckUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'id_num', 'is_active', 'one_off', 'phone']


class CustomUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(default=uuid.uuid4())
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'third_name', 'email', 'email_corp', 'phone',
                  'full_name', 'id_num', 'status', 'is_staff', 'is_active', 'one_off', 'profile_image']

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.is_active = False
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user


class ProfileCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'full_name', 'first_name', 'last_name', 'third_name', 'full_name', 'phone', 'email',
                  'email_corp', 'id_num', 'status', 'profile_image']


class VacationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vacations
        fields = ['id', 'id_user', 'id_num', 'first_name', 'last_name', 'doc_name', 'start_vacation',
                  'end_vacation', 'vacation_status', 'doc_date', 'vacation_type', 'line_manager', 'description',
                  'decree', ]


class LogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogList
        fields = ['id', 'id_user', 'id_num', 'first_name', 'last_name', 'doc_name', 'doc_status',
                  'doc_date', 'description', 'decree', 'tag', ]


class MawsEditStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MawsEditStatus
        fields = ['id', 'id_user', 'user', 'storage', 'placement']


class FormsMawsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsMaws
        fields = ['id', 'id_user', 'name', 'goods', 'responsibles', 'location', 'storage', 'placement', 'manager',
                  'date']


class EditEmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditEmails
        fields = ['id', 'email', 'v_code']

    def create(self, validated_data):
        editemails = super().create(validated_data)

        lower = 10 ** 5
        upper = 10 ** 6 - 1
        v_code = random.randint(lower, upper)
        v_code = str(v_code)

        subject = 'Подтверждение почты'
        message = """Вы запросили изменение личной почты на портале http://www.intra.isker.kz 
Ваш код для подтверждения почты: """ + v_code + """
                     
Вам необходимо указать данный код на портале.
"""
        from_email = [validated_data['email']]

        send_mail(f'{subject}', message, DEFAULT_FROM_EMAIL, from_email)

        editemails.id = validated_data['id']
        editemails.email = validated_data['email']
        editemails.v_code = v_code
        editemails.save()

        return Response(status=status.HTTP_200_OK)


class EditPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = EditPhone
        fields = ['id', 'id_num', 'phone', 'v_code']

    def create(self, validated_data):
        editphone = super().create(validated_data)

        lower = 10 ** 5
        upper = 10 ** 6 - 1
        v_code = random.randint(lower, upper)
        v_code = str(v_code)

        editphone.id = validated_data['id']
        editphone.phone = validated_data['phone']
        editphone.v_code = v_code
        editphone.save()

        return Response(status=status.HTTP_200_OK)
