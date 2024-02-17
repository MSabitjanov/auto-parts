from django.conf import settings
from django.http import HttpResponseRedirect

from allauth.account import app_settings as allauth_account_settings
from allauth.account.utils import complete_signup
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.models import TokenModel
from dj_rest_auth.utils import jwt_encode
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters('password1', 'password2'),
)

def email_confirm_redirect(request, key):
    return HttpResponseRedirect(
        f"{settings.EMAIL_CONFIRM_REDIRECT_BASE_URL}{key}/"
    )


def password_reset_confirm_redirect(request, uidb64, token):
    return HttpResponseRedirect(
        f"{settings.PASSWORD_RESET_CONFIRM_REDIRECT_BASE_URL}{uidb64}/{token}/"
    )
    
    
class CustomRegisterView(CreateAPIView):
    serializer_class = api_settings.REGISTER_SERIALIZER
    permission_classes = api_settings.REGISTER_PERMISSION_CLASSES
    token_model = TokenModel
    throttle_scope = 'dj_rest_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_response_data(self, user):
        if allauth_account_settings.EMAIL_VERIFICATION == \
                allauth_account_settings.EmailVerificationMethod.MANDATORY:
            return {'detail': _('Verification e-mail sent.')}

        if api_settings.USE_JWT:
            data = {
                'user': user,
                'access': self.access_token,
                'refresh': self.refresh_token,
            }
            return api_settings.JWT_SERIALIZER(data, context=self.get_serializer_context()).data
        elif api_settings.SESSION_LOGIN:
            return None
        else:
            return api_settings.TOKEN_SERIALIZER(user.auth_token, context=self.get_serializer_context()).data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        
        phone_number = self.request.data.get('phone_number')
        if phone_number:
            user.phone_number = phone_number
            user.save()

        if allauth_account_settings.EMAIL_VERIFICATION != \
                allauth_account_settings.EmailVerificationMethod.MANDATORY:
            if api_settings.USE_JWT:
                self.access_token, self.refresh_token = jwt_encode(user)
            elif not api_settings.SESSION_LOGIN:
                # Session authentication isn't active either, so this has to be
                #  token authentication
                api_settings.TOKEN_CREATOR(self.token_model, user, serializer)

        complete_signup(
            self.request._request, user,
            allauth_account_settings.EMAIL_VERIFICATION,
            None,
        )
        return user
