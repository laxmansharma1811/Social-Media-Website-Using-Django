from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'), 
    path('home/',views.home, name='home'),
    path('login/', views.login_user, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('upload/', views.upload_image, name='upload'),
    path('edit_image/<int:image_id>/', views.edit_image, name='edit_image'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('like/<int:image_id>/', views.like, name='like'),
    path('comment/<int:image_id>/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('settings/', views.settings, name='settings'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('reels/', views.reels, name='reels'),
    path('upload_video/', views.upload_video, name='upload_video'),
    path('edit_video/<int:video_id>/', views.edit_video, name='edit_video'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),
    path('like_video/<int:video_id>/', views.like_video, name='like_video'),
    path('profile/<int:user_id>/', views.view_profile, name='view_profile'),
    path('show_comments/<int:image_id>/', views.show_comments, name='show_comments'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
