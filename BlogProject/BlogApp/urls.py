from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', loginPage, name='loginPage'),
    path('register/', register, name='register'),
    path('profile/', profilePage, name='profile'),
    path('contact/', contact, name='contact'),
    path('edit_profile/', editProfile, name='editProfile'),
    path('logout/', logoutPage, name='logoutPage'),
    path('change_password/', changePassword, name='change_password'),
    path('add_post/', add_post, name='add_post'),
    path('manage_post/', manage_post, name='manage_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('trash_post/<int:post_id>/', trash_post, name='trash_post'),
    path('post/<int:post_id>/', single_post, name='single_post'),    
    path('trash/', view_trashed_posts, name='view_trashed_posts'),
    path('restore/<int:post_id>/', restore_post, name='restore_post'),
    path('delete/<int:post_id>/', delete_post_permanently, name='delete_post_permanently'),
    path('search/', search_content, name="search_content"),
    path('blog/', blog, name="blog"),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/delete/', delete_comment, name='delete_comment'),
    path('delete-reply/<int:comment_id>/', delete_reply, name='delete_reply'),
]
