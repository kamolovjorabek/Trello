from rest_framework.response import Response
from rest_framework.views import APIView
from v1.user.serializers import UserRegisterSerializer
# Create your views here.


class UserRegisterApi(APIView):
    def post(self, request):
        data = request.data
        serializer = UserRegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
