from rest_framework import viewsets, permissions, generics

from .serializers import *
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Vacations, LogList, MawsEditStatus, FormsMaws, EditEmails
from rest_framework.authtoken.models import Token


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # if using drf authtoken, create a new token
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        # return new token
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]


class ProfileCustomUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileCustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        profile = self.get_queryset().get(pk=self.request.user.pk)
        serializer = self.get_serializer(profile)
        return Response({'user': serializer.data})

    # def get_queryset(self):
    #     if self.request.user:
    #         user = get_user_model().objects.filter(pk=self.request.user.pk)
    #         if user is None:
    #             raise exceptions.AuthenticationFailed('Пользователь не найден')
    #         return user


class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class VacationsViewSet(viewsets.ModelViewSet):
    queryset = Vacations.objects.all().order_by('-doc_date')
    serializer_class = VacationsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Vacations.objects.all().order_by('-doc_date')
        id_user = self.request.query_params.get('id_user')
        if id_user:
            queryset = queryset.filter(id_user=id_user)

        return queryset

    def patch(self, request, *args, **kwargs):
        vacations = Vacations.objects.get()
        data = request.data

        vacations.vacation_status = data.get("vacation_status", vacations.vacation_status)
        vacations.description = data.get("description", vacations.description)
        vacations.decree = data.get("decree", vacations.decree)

        vacations.save()
        # serializer = VacationsSerializer(vacations)

        return Response(status=status.HTTP_200_OK)


class LogListViewSet(viewsets.ModelViewSet):
    queryset = LogList.objects.all().order_by('-doc_date')
    serializer_class = LogListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        loglist = LogList.objects.get()
        data = request.data

        loglist.doc_date = data.get("doc_date", loglist.doc_date)
        loglist.doc_status = data.get("doc_status", loglist.doc_status)
        loglist.description = data.get("description", loglist.description)
        loglist.decree = data.get("decree", loglist.decree)

        loglist.save()
        # serializer = LogListSerializer(loglist)

        return Response(status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = LogList.objects.all().order_by('-doc_date')
        id_user = self.request.query_params.get('id_user')
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(id_user=id_user, tag=tag)
        elif id_user:
            queryset = queryset.filter(id_user=id_user)

        return queryset


class MawsEditStatusViewSet(viewsets.ModelViewSet):
    queryset = MawsEditStatus.objects.all()
    serializer_class = MawsEditStatusSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = MawsEditStatus.objects.all()
        storage = self.request.query_params.get('storage')
        placement = self.request.query_params.get('placement')
        if placement:
            queryset = queryset.filter(placement=placement, storage=storage)
        return queryset


class FormsMawsViewSet(viewsets.ModelViewSet):
    queryset = FormsMaws.objects.all()
    serializer_class = FormsMawsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = FormsMaws.objects.all().order_by('-id')
        id_user = self.request.query_params.get('id_user')
        date = self.request.query_params.get('date')
        placement = self.request.query_params.get('placement')
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(id_user=id_user, date=date, placement=placement, name=name)
        elif id_user:
            queryset = queryset.filter(id_user=id_user, date=date, placement=placement)

        return queryset

    def patch(self, request, *args, **kwargs):
        formmaws = FormsMaws.objects.get()
        data = request.data

        formmaws.goods = data.get("goods", formmaws.goods)
        formmaws.responsibles = data.get("responsibles", formmaws.responsibles)
        formmaws.name = data.get("name", formmaws.name)

        formmaws.save()

        return Response(status=status.HTTP_200_OK)

    @action(detail=False)
    def delete_post(self, request, *arg, **kwarg):
        queryset = FormsMaws.objects.all()
        id = self.request.query_params.get('id')
        qs = queryset.filter(id=id)
        # delete the selected item
        qs.delete()
        # return deleted
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CheckUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        id_num = self.kwargs['id_num']
        return get_user_model().objects.filter(id_num=id_num)


class EditEmailsViewSet(viewsets.ModelViewSet):
    queryset = EditEmails.objects.all()
    serializer_class = EditEmailsSerializer
    permission_classes = [permissions.IsAuthenticated]


class EditPhoneViewSet(viewsets.ModelViewSet):
    queryset = EditPhone.objects.all()
    serializer_class = EditPhoneSerializer
    permission_classes = [permissions.IsAuthenticated]


class UpdateUserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *arg, **kwarg):
        id_num = self.kwargs['id_num']
        updateuser = get_user_model().objects.get(id_num=id_num)
        data = request.data
        if data:
            updateuser.phone = data.get("phone", updateuser.phone)
            updateuser.email_corp = data.get("email_corp", updateuser.email_corp)
            updateuser.first_name = data.get("first_name", updateuser.first_name)
            updateuser.last_name = data.get("last_name", updateuser.last_name)
            updateuser.third_name = data.get("third_name", updateuser.third_name)

        updateuser.save()
        return Response(status=status.HTTP_200_OK)
