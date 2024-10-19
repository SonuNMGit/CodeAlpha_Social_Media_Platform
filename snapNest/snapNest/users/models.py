from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='user_follows', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='user_followed_by', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    privacy = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    is_private = models.BooleanField(default=False)  # Add this field to manage privacy
    followers = models.ManyToManyField(User, related_name='profile_followers', blank=True)
    following = models.ManyToManyField(User, related_name='profile_following', blank=True)

    def __str__(self):
        return self.user.username


    def __str__(self):
        return f'{self.user.username} Profile'
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # User who created the post
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1, related_name='profile_posts')
    title = models.CharField(max_length=100, default='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"Post by {self.user.username} on {self.created_at}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    is_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} to {self.recipient}: {self.content}"
