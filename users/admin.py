from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Vacations, LogList, MawsEditStatus, FormsMaws, EditEmails, EditPhone

admin.site.site_header = 'Панель администратора'


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'first_name', 'last_name', 'phone', 'email', 'email_corp']

    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительные данные',
         {'fields': ('third_name', 'phone', 'full_name', 'id_num', 'status', 'one_off', 'email_corp', 'profile_image')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительные данные', {'fields': ('first_name', 'last_name', 'third_name', 'email', 'phone', 'full_name',
                                              'id_num', 'status', 'one_off', 'email_corp', 'profile_image')}),
    )

    search_fields = ('first_name', 'last_name', 'email', 'phone', 'full_name', 'username', 'id_num',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')


class VacationsAdmin(admin.ModelAdmin):
    list_display = ['doc_name', 'first_name', 'last_name', 'start_vacation', 'end_vacation', 'doc_date',
                    'vacation_status', 'vacation_type',]
    ordering = ('-doc_date',)


class LogListAdmin(admin.ModelAdmin):
    list_display = ['doc_name', 'first_name', 'last_name', 'doc_date', 'doc_status', 'description', 'tag']
    ordering = ('-doc_date',)


class MawsEditStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_user', 'user', 'storage', 'placement']


class FormsMawsAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_user', 'name', 'goods', 'responsibles', 'location', 'storage', 'placement', 'manager',
                    'date']


class EditEmailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'v_code']


class EditPhoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'phone', 'v_code']


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vacations, VacationsAdmin)
admin.site.register(LogList, LogListAdmin)
admin.site.register(MawsEditStatus, MawsEditStatusAdmin)
admin.site.register(FormsMaws, FormsMawsAdmin)
admin.site.register(EditEmails, EditEmailsAdmin)
admin.site.register(EditPhone, EditPhoneAdmin)
