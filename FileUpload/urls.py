from django.conf.urls.static import static
from django.urls import path

from CloudStorageDeduplication import settings
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('logout/', views.logout1, name='logout'),
    path('file-upload/', views.file_upload, name='file-upload'),
    path('delete-file/<int:id>', views.delete_file, name='delete-file'),
    path('download-file/<int:id>', views.download_file, name='download-file'),
    path('password-change', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password-reset'),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)