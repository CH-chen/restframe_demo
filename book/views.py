from django.shortcuts import render
from .models import *

# Create your views here.

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

class PublisherSerializers(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.CharField()

# class BookSerializers(serializers.Serializer):
#     title = serializers.CharField()
#     price = serializers.IntegerField()
#     pub_date = serializers.DateField()
#     publisher = serializers.CharField(source="publisher.email")
#     # authors = serializers.CharField(source="authors.all") #多对多不好用
#     authors =serializers.SerializerMethodField()
#     def get_authors(self,obj):
#         temp = []
#         for obj in obj.authors.all():
#             temp.append(obj.name)
#             print(temp)
#         return temp

class PublishSeria(serializers.ModelSerializer):
    class Meta:
        model = Publish
        fields = "__all__"

class BookSeria(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = "__all__"
    #显示超链接
    publish = serializers.HyperlinkedIdentityField(
        view_name='publish_detail',
        lookup_field="publish_id",
        lookup_url_kwarg="pk")
    # 改成连接之后，重新增加book表的话会出错，显示找不到publish_id
        #自定义显示字段 可以不加，不加自定义字段就显示全部字段  用自定义的话post请求要重写create方法
    # publisher = serializers.CharField(source="publisher.pk",read_only=True)#一对多可以用 自定义字段
    # authors = serializers.CharField(source="authors.all") #多对多不好用
    #多对多用下面这个
    # authors =serializers.SerializerMethodField() 自定义字段
    # def get_authors(self,obj):
    #     temp = []
    #     for obj in obj.authors.all():
    #         temp.append(obj.name)
    #         print(temp)
    #     return temp
    # 自定义显示字段 用自定义的话post请求要重写create方法,不自定义用默认的就不需要create方法
    # def create(self, validated_data):
    #     print("validated_data",validated_data)
    #     book = Book.objects.create(title=validated_data["title"],price=validated_data["price"],pub_date=validated_data["pub_date"],publisher_id=validated_data["publisher"]["pk"])
    #     book.authors.add(*validated_data["authors"])
    #     return book

class AuthorSeria(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

# 第一种：  以APIView方式
#认证组件 验证用户名  局部验证
# from rest_framework import exceptions
# from rest_framework.authentication import BaseAuthentication
# class UserTokenCheck(BaseAuthentication):
#     def authenticate(self,request):
#         token = request.GET.get("token")
#         token_obj = UserToken.objects.filter(token=token).first()
#         if not token_obj:
#             raise exceptions.AuthenticationFailed("验证失败")
#         else:
#             return token_obj.userinfo.name,token_obj.token
        #如果继承于BaseAuthentication，authenticate_header就不用写了
        #如果不继承就要加上
    # def authenticate_header(self,request):
    #     pass


#解析器
from rest_framework.parsers import JSONParser,FormParser,MultiPartParser,FileUploadParser

#分页
from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

class MyPageNumberPagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page"
    page_size_query_param = "size"
    max_page_size = 3
# #http://127.0.0.1:8000/books/?page = 2   #页面显示
# #http://127.0.0.1:8000/books/?page=1&size=3#临时用每页显示最大3条数据

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1
class BookView(APIView):

    # authentication_classes = [UserTokenCheck,]
    def get(self,request,):
        book_list = Book.objects.all()
        # 分页*****************

        # page_num = MyPageNumberPagination()
        page_num = MyLimitOffsetPagination()
        books_pagenum = page_num.paginate_queryset(book_list, request, self)
        bs = BookSeria(books_pagenum, many=True, context={"request": request})
        # bs = BookSeria(book_list,many=True)
        # bs = BookSeria(book_list, many=True,context={"request":request})
        bookser = BookSeria(book_list,many=True,context={'request': request})
        return Response(bookser.data)
    def post(self,request):
        print(request.data)
        bookser = BookSeria(data=request.data,context={'request': request})
        print(bookser)
        if bookser.is_valid():
            bookser.save()
            return Response(bookser.data)
        else:
            return Response(bookser.errors)



class BookDetailView(APIView):
    def get(self,request,pk):
        book_obj = Book.objects.filter(pk=pk).first()
        bookser = BookSeria(book_obj,context={'request': request})
        return Response(bookser.data)
    def put(self,request,pk):
        book_obj = Book.objects.filter(pk=pk).first()
        bookser = BookSeria(book_obj, data=request.data,context={'request': request})
        print(bookser)

        if bookser.is_valid():
            bookser.save()
            return Response(bookser.data)
        else:
            return Response(bookser.errors)
    def delete(self,request,pk):
        Book.objects.filter(pk=pk).first().delete()
        return Response()

class PublishView(APIView):
    def get(self, request, *args, **kwargs):
        publish_list = Publish.objects.all()
        bs = PublishSeria(publish_list, many=True, context={'request': request})
        return Response(bs.data)

    def post(self, request, *args, **kwargs):

        bs = PublishSeria(data=request.data, many=False)
        if bs.is_valid():
            # print(bs.validated_data)
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)
class PublishDetailView(APIView):
    def get(self, request, pk):

        publish_obj = Publish.objects.filter(pk=pk).first()
        bs = PublishSeria(publish_obj, context={'request': request})
        return Response(bs.data)

    def put(self, request, pk):
        publish_obj = Publish.objects.filter(pk=pk).first()
        bs = PublishSeria(publish_obj, data=request.data, context={'request': request})
        if bs.is_valid():
            bs.save()
            return Response(bs.data)
        else:
            return Response(bs.errors)
#
# # 第二种  通过mixins  generics
#
# from rest_framework import mixins
# from rest_framework import generics

# class BookView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#
#     queryset = Book.objects.all()
#     serializer_class = BookSeria
#
#     def get(self,request,*args,**kwargs):
#
#         return self.list(request,*args,**kwargs)
#
#     def post(self, request, *args, **kwargs):
#         print("===========")
#         print(request.data)
#         return self.create(request, *args, **kwargs)
#
# class BookDetailView(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSeria
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
#
# class PublishView(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#
#     queryset = Publish.objects.all()
#     serializer_class = PublishSeria
#
#     def get(self,request,*args,**kwargs):
#
#         return self.list(request,*args,**kwargs)
#
#     def post(self, request, *args, **kwargs):
#         print("===========")
#         print(request.data)
#         return self.create(request, *args, **kwargs)
#
# class PublishDetailView(mixins.RetrieveModelMixin,
#                     mixins.UpdateModelMixin,
#                     mixins.DestroyModelMixin,
#                     generics.GenericAPIView):
#
#     queryset = Publish.objects.all()
#     serializer_class = PublishSeria
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#第三种 简化通用类视图
# class BookView(generics.ListCreateAPIView):
#
#     queryset = Book.objects.all()
#     serializer_class = BookSeria
#
# class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSeria
# class PublishView(generics.ListCreateAPIView):
#
#     queryset = Publish.objects.all()
#     serializer_class = PublishSeria
#
# class PublishDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Publish.objects.all()
#     serializer_class = PublishSeria
#
#第四种
# from rest_framework import viewsets
# class BookViewSet(viewsets.ModelViewSet):
#     queryset = Book.objects.all()
#     serializer_class = BookSeria

# #权限组件
# from rest_framework.permissions import BasePermission
# class SVIPPermission(BasePermission):  #继承于BasePermission，/authous/2/才能查看每个具体的作者。否则报错
#     message = "只有超级用户才能访问"
#     def has_permission(self,request,view):
#         username = request.user
#         print(username)
#         user_type = UserInfo.objects.filter(name=username).first().user_type
#         if user_type == 3:
#             return True
#         else:
#             return False

# from book.service import SVIPPermission
from rest_framework import viewsets

    #*********频率组件*********

from rest_framework.throttling import BaseThrottle

VISIT_RECORD={}
class VisitThrottle(BaseThrottle):

    def __init__(self):
        self.history=None

    def allow_request(self,request,view):
        remote_addr = request.META.get('REMOTE_ADDR')
        print(remote_addr)
        import time
        ctime=time.time()

        if remote_addr not in VISIT_RECORD:
            VISIT_RECORD[remote_addr]=[ctime,]
            print(VISIT_RECORD[remote_addr])
            return True

        history=VISIT_RECORD.get(remote_addr)
        self.history=history

        while history and history[-1]<ctime-60:
            history.pop()

        if len(history)<10:
            history.insert(0,ctime)
            return True
        else:
            return False

    def wait(self):
        import time
        ctime=time.time()
        return 60-(ctime-self.history[-1])

class AuthorViewSet(viewsets.ModelViewSet):
    # authentication_classes = [UserTokenCheck, ] #局部验证
    # permission_classes = [SVIPPermission,]
    throttle_classes = [VisitThrottle]
    pagination_class = MyPageNumberPagination
    queryset = Author.objects.all()
    serializer_class = AuthorSeria

#生成随机token
def get_random_Str(name):
    import hashlib,time
    currenttime = str(time.time())
    md5 = hashlib.md5(bytes(currenttime,encoding="utf-8"))
    return md5.hexdigest()

#用户登录
import json
from django.http import JsonResponse
class LoginView(APIView):
    authentication_classes = [] #全局配置后，不让login验证，直接加空列表就不验证
    def post(self,request):
        print(request.data)
        name = request.data.get("name")
        pwd = request.data.get("pwd")
        user_obj = UserInfo.objects.filter(name=name,pwd=pwd).first()
        ret = {"status":"1000","msg":"验证成功"}
        if user_obj:
            random_str = get_random_Str(user_obj.name)
            UserToken.objects.update_or_create(userinfo=user_obj,defaults={"token":random_str})
            ret["token"]=random_str


        else:
            ret["status"] = 404
            ret["msg"] = "用户名或者密码错误"
            return JsonResponse(ret)
        return Response(json.dumps(ret,ensure_ascii=False))


