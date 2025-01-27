from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^blogs/$', views.BlogListView.as_view(), name='blogs'),
    url(r'^blog/(?P<pk>\d+)$', views.BlogDetailView.as_view(), name='blog_detail'),
    url(r'^bloggers/$', views.BloggerListView.as_view(), name='bloggers'),
    url(r'^bloggers/(?P<pk>\d+)/$', views.BloggerDetailView.as_view(), name='blogger_detail'),
    url(r'^blog/(?P<pk>\d+)/create$', views.CommentAdd.as_view(), name='add_comment'),
]