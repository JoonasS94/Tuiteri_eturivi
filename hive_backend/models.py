from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    # Add any custom fields here, e.g.:
    profile_picture = models.ImageField(upload_to="profile_pics/", blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.username

CustomUser = get_user_model()  # This retrieves the custom user model

class Hashtag(models.Model):
    name = models.CharField(max_length=20, unique=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    text = models.CharField(max_length=144)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="posts")
    hashtags = models.ManyToManyField(Hashtag, related_name="posts")
    references = models.ManyToManyField(CustomUser, related_name="referenced_posts", blank=True)

    def __str__(self):
        return f"{self.text[:20]}... by {self.user.username}"

class LikedUsers(models.Model):
    liker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="liked_users")
    liked_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="users_liked_by")

    class Meta:
        unique_together = ("liker", "liked_user")

    def __str__(self):
        return f"{self.liker.username} likes {self.liked_user.username}"

class FollowedHashtags(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followed_hashtags")
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ("user", "hashtag")

    def __str__(self):
        return f"{self.user.username} follows #{self.hashtag.name}"

class LikedPosts(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="liked_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_by")

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.username} likes post {self.post.id}"

class FollowedUsers(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    followed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ("follower", "followed_user")

    def __str__(self):
        return f"{self.follower.username} follows {self.followed_user.username}"
