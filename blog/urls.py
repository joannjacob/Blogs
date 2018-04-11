from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'^home/$',views.home),
    url(r'^home/login$',views.login),
    url(r'^home/signup$',views.signup),
    url(r'^login/$',views.login),
    url(r'^login/user$',views.enter_login),
    url(r'^login/add_blog$',views.add_blog),
    url(r'^login/add_blogentry$',views.add_blogentry),
    url(r'^login/my_blogs$', views.my_blogs),
    url(r'^login/all_blogs$', views.all_blogs),
    url(r'^signup/$', views.signup),
    url(r'^signup/login$', views.add_signup),
    url(r'^login/logout$',views.logout),
    url(r'^login/login$',views.login),
    url(r'^login/forgot_password$',views.forgot_password),
    url(r'^login/password_update$',views.password_update),




]