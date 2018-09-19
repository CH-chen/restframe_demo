"""restframe_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from book import views
#URL路由分发
from rest_framework import routers
routers=routers.DefaultRouter()
routers.register("authors",views.AuthorViewSet)
#会自动添加以下地址
# ^authors/$ [name='author-list']
# ^authors\.(?P<format>[a-z0-9]+)/?$ [name='author-list']
# ^authors/(?P<pk>[^/.]+)/$ [name='author-detail']
# ^authors/(?P<pk>[^/.]+)\.(?P<format>[a-z0-9]+)/?$ [name='author-detail']

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^books/$',views.BookView.as_view()),
    url(r'^books/(?P<pk>\d+)/',views.BookDetailView.as_view()),
    url(r'^publish/$',views.PublishView.as_view()),
    url(r'^publish/(?P<pk>\d+)/',views.PublishDetailView.as_view(),name="publish_detail"),
    #第四种
    # url(r'^books/$', views.BookViewSet.as_view({"get": "list", "post": "create"}), name="book_list"),
    # url(r'^books/(?P<pk>\d+)/$', views.BookViewSet.as_view({'get': 'retrieve',
    #                                                     'put': 'update','patch': 'partial_update',
    #                                                     'delete': 'destroy'}), name="book_detail"),

    url(r'^authors/$', views.AuthorViewSet.as_view({"get": "list", "post": "create"}), name="author_list"),
    url(r'^authors/(?P<pk>\d+)/$', views.AuthorViewSet.as_view({'get': 'retrieve',
                                                        'put': 'update','patch': 'partial_update',
                                                        'delete': 'destroy'}), name="author_detail"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
]
