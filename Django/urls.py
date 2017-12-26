"""Django URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from dashboard import views #signup_view,login_view,feed_view,post_view,like_view

urlpatterns = [
    url(r'^$',views.signup_view),
    url(r'^$login/',views.login_view),
    url(r'^$feed/',views.feed_view),
    url(r'^$like/',views.like_view),
    url(r'^$post/',views.post_view),
    url(r'^admin/', views.admin.site.urls),
]
