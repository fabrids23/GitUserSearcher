from rest_framework_jwt import authentication

from GitUserSearcher.integrations.serializers import CurrentUserSerializer
from GitUserSearcher.utils import LogUtilMixin


class GitUserSearcherJSONWebTokenAuthentication(authentication.JSONWebTokenAuthentication, LogUtilMixin):

    def authenticate(self, request):
        """
        Returns a two-tuple of `User` and token if a valid signature has been
        supplied using JWT-based authentication.  Otherwise returns `None`.
        """
        user_token = super(GitUserSearcherJSONWebTokenAuthentication, self).authenticate(request)

        return user_token


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': CurrentUserSerializer(user, context={'request': request}).data
    }
