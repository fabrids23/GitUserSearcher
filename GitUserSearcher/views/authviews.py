from django.contrib.auth.models import User
from rest_framework import status
from GitUserSearcher.integrations.serializers import CurrentUserSerializer
from GitUserSearcher.utils import LogUtilMixin
from rest_framework_jwt.views import ObtainJSONWebToken


class MyObtainJSONWebToken(ObtainJSONWebToken, LogUtilMixin):

    def post(self, request, *args, **kwargs):

        response = super(MyObtainJSONWebToken, self).post(request, args, kwargs)

        if response.status_code == status.HTTP_400_BAD_REQUEST:
            response.status_code = status.HTTP_401_UNAUTHORIZED

        if response.status_code == status.HTTP_200_OK:
            response.data['user'] = CurrentUserSerializer(User.objects.get(username=request.data['username'])).data
        return response


obtain_jwt_token = MyObtainJSONWebToken.as_view()
