from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    GENDER = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),

    ]

    contact_no = models.IntegerField(null=True)
    gender = models.CharField(max_length=50, choices=GENDER, null=True)
    profile_pic=models.ImageField(upload_to='Media/Profile_Pic',null=True)
    age = models.IntegerField(null=True)

class Category(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, null=True)
    keywords = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    post_image=models.ImageField(upload_to='Media/Post_images',null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    is_trashed = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.title
    


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    content = models.TextField(null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"


