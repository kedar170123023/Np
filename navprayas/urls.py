from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # *****************************
    # urls for home_links
    # *****************************

    path('videos_list/', views.videos_list, name='videos_list'),
    path('upload/', views.file_upload, name='upload'),
    path('play/<int:video_id>/', views.play, name='play'),
    path('index/', views.index, name='index'),
    path('results/', views.results_out, name='results'),
    path('results19/', views.results_out_19, name='results_19'),
    path('about/', views.about, name='about'),
    path('events/', views.events, name='events'),
    path('notifications/', views.notifications, name='notifications'),
    path('team/', views.team, name='contact'),
    path('', views.index, name='index'),

    # *****************************
    # urls for registering to exams
    # *****************************
	path('signup/', views.register, name='signup'),
    path('profile/', views.profile, name='profile'),  #not created the profile
    path('edit_profile/', views.edit_profile, name='edit_profile'),  #not created the profile
    path('login/', auth_views.LoginView.as_view(template_name ='navprayas/users/login.html'), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(template_name= 'navprayas/users/logout.html'), name='logout'),


    # *****************************
    # urls for Forget Password
    # *****************************

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name= 'navprayas/users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name= 'navprayas/users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name= 'navprayas/users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name= 'navprayas/users/password_reset_complete.html'), name='password_reset_complete'),

    # path('password_reset/', auth_views.password_reset, name='password_reset'),
    # path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    # path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #    auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),

    # path('', include('django.contrib.auth.urls')),

    # *****************************
    # urls for registering to exams
    # *****************************

    path('MTSE_register/', views.MTSE_register, name='MTSE_register'),
    path('PR_register/', views.PR_register, name='PR_register'),
    path('CC_register/', views.CC_register, name='CC_register'),
    path('RANGOTSAV_register/', views.RANGOTSAV_register, name='RANGOTSAV_register'),
    path('FHS_register/', views.FHS_register, name='FHS_register'),
    path('CHESS_register/', views.CHESS_register, name='CHESS_register'),

   # *****************************
    # paytm
    # *****************************


    # path("payment/", views.payment, name="payment"),
    path("handlerequest/", views.handlerequest, name="handlerequest"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
