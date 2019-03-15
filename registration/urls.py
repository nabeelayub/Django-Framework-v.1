from django.conf.urls import url
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView

from . import views
from django.contrib.auth import views as auth_views



urlpatterns=[
    url(r'^$',views.Indexview,name='index'),
    url(r'^login/$',views.loginform.as_view(),name='login'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'^password_reset/$',auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"),name='password_reset'),
    url(r'^password_reset/done$',
    auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
        name='password_reset_done'),
    #url(r'^password_reset/done/$',auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    url(r'^reset/done/$',auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),name="password_reset_complete"),
    url(r'^phone/$',views.phoneverify.as_view(),name='verify'),
    url(r'^verify/$',views.phoneverification.as_view(),name='phoneverification'),
    url(r'^confirm/$', views.ConfirmView.as_view(), name='confirm'),
    url(r'^(?P<pk>[0-9]+)/home/$',views.home.as_view(),name='home'),
    #url(r'^secpage/$',views.second.as_view(),name='sec_page'),
    #url(r'^uploadprofile/$', views.second.as_view(), name='sec_page'),
    url(r'^viewprofile_1/$',views.seeprofile.as_view(),name='viewprofile_1'),
    url(r'^(?P<pk>[0-9]+)/update/$', views.editView.as_view(), name='edit_view'),
    url(r'^logout/$', LogoutView.as_view(), name='user_logout'),

    #####              REST_FRAMEWORK      ####

    url(r'^create_user/$', views.Createuser.as_view()),
    url(r'^update_user/(?P<pk>\d+)/$', views.Updateuser.as_view()),
    url(r'^delete_user/(?P<pk>\d+)/$', views.Deleteuser.as_view()),


]