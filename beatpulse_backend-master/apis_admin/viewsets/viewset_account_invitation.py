import uuid

from rest_framework.permissions import IsAuthenticated

from apis_admin.permissions.permissions import IsAdminOrReadOnly
from apis_admin.serializers.serializer_account_invitation import AccountInvitationSerializer
from apis_admin.viewsets.admin_dynamic_model_viewset import AdminDynamicModelViewset
from email_module.views import send_email_producer_invite
from models.models import AccountInvitation


class AccountInvitationViewSet(AdminDynamicModelViewset):
    queryset = AccountInvitation.objects.all()
    serializer_class = AccountInvitationSerializer
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'delete']

    def perform_create(self, serializer):
        invite: AccountInvitation = serializer.save(token=uuid.uuid4())
        send_email_producer_invite(email_sent_to=invite.email_sent_to, role=invite.role, token=invite.token)
