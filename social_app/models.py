from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UploadedImage(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user')
    image = models.ImageField(upload_to='images/')
    desc = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User,related_name="likes",blank=True,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)


    def __str__(self):
        return self.image.name
    


class Comment(models.Model):
    image = models.ForeignKey(UploadedImage, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)

    def follow(self, user):
        if user != self.user:
            self.followers.add(user)

    def unfollow(self, user):
        self.followers.remove(user)

    def delete(self, *args, **kwargs):
        if self.profile_picture:
            self.profile_picture.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username

    


class UploadedVideo(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='video_author_user')
    video = models.FileField(upload_to='videos/')
    desc = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="video_likes", blank=True, null=True)
    savers = models.ManyToManyField(User,blank=True , related_name='saved')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)


    def __str__(self):
        return self.video.name


