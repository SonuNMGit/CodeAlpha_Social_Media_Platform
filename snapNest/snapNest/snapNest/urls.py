"""
URL configuration for snapNest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user_views.home, name='home'),
    path('register/', user_views.register, name='register'),
    path('login/', user_views.login_user, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset-password/', user_views.password_reset_view, name='password_reset'),
    path('profile/<int:user_id>/', user_views.profile, name='profile'),
    path('profile/update', user_views.update_profile, name='update_profile'),
    path('delete_post/<int:post_id>/', user_views.delete_post, name='delete_post'),
    path('add_post/', user_views.add_post, name='add_post'), 
    path('search/', user_views.search_user, name='search_user'),
    path('follow/<int:user_id>/', user_views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', user_views.unfollow_user, name='unfollow_user'),
    path('remove_follower/<int:follower_id>/', user_views.remove_follower, name='remove_follower'),
    path('posts/', user_views.public_posts_view, name='public_posts'),
    path('like/<int:post_id>/', user_views.like_post, name='like_post'),
    path('like_post/<int:post_id>/', user_views.toggle_like_post, name='toggle_like_post'),
    path('post/<int:post_id>/comment/', user_views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', user_views.delete_comment, name='delete_comment'),
    path('msg_reg/', user_views.msg_req, name='messages'),
    path('accept_request/<int:message_id>/', user_views.accept_follow_request, name='accept_follow_request'),
    path('reject_request/<int:message_id>/', user_views.reject_follow_request, name='reject_follow_request'),
    path('messages/delete/<int:message_id>/', user_views.delete_message, name='delete_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

