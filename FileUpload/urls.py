from django.conf.urls.static import static
from django.urls import path

from CloudStorageDeduplication import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    # path('my-login/', views.login, name='my-login'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('logout/', views.logout1, name='logout'),
    path('file-upload/', views.file_upload, name='file-upload'),
    path('delete-file/<int:id>', views.delete_file, name='delete-file'),
    path('download-file/<int:id>', views.download_file, name='download-file')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)