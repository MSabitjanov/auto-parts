from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework.permissions import BasePermission, SAFE_METHODS

from apps.communication.models import Chat


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and obj.user == request.user


class IsSellerOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and hasattr(request.user, "seller"):
            return True

        self.message = "You must have seller account to perform this action."
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.seller.user == request.user


class IsAutoPartOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        self.message = "What are you doing my friend? You do not have permission to perform this action."
        return obj.auto_part.seller.user == request.user


class IsMasterOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated and hasattr(request.user, "master"):
            return True

        self.message = "You must have master account to perform this action."
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.master.user == request.user


class IsChatParticipant(BasePermission):
    def has_permission(self, request, view):
        chat_id = view.kwargs.get("chat_id")
        if chat_id:
            return (
                request.user
                in get_object_or_404(Chat.objects.all(), id=chat_id).participants.all()
            )

        return False
