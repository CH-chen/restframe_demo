from .models import *

from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
class UserTokenCheck(BaseAuthentication):
    def authenticate(self,request):
        token = request.GET.get("token")
        token_obj = UserToken.objects.filter(token=token).first()
        if not token_obj:
            raise exceptions.AuthenticationFailed("验证失败")
        else:
            return token_obj.userinfo.name,token_obj.token

#权限组件
from rest_framework.permissions import BasePermission
class SVIPPermission(BasePermission):  #继承于BasePermission，/authous/2/才能查看每个具体的作者。否则报错
    message = "只有超级用户才能访问"
    def has_permission(self,request,view):
        username = request.user
        print(username)
        user_type = UserInfo.objects.filter(name=username).first().user_type
        if user_type == 3:
            return True
        else:
            return False