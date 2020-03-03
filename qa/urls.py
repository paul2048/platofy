from django.urls import path, include
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile/<int:uid>/', views.profile, name='profile'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('vote/', views.vote, name='vote'),
    path('delete_qa/', views.delete_qa, name='delete_qa'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='logout'),
    path('avatar/', include('avatar.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)