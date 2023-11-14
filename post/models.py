from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User=get_user_model()
# Create your models here.


class Post(models.Model):
    image=models.ImageField(upload_to="uploads/")
    caption=models.TextField(default="")
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    is_active=models.BooleanField(default=True)
    date_created=models.DateTimeField(default=timezone.now)
    date_updated=models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.date_updated=timezone.now()
        super(Post,self).save(*args, **kwargs)

    @property
    def comment(self):
        return self.comment_set.all().order_by('date_created')
    
    @property
    def likes(self):
        return self.likes.filter(is_active=True)
    
    def is_liked_by(self, user=None):
        if user and hasattr(user, "id"):
            return self.likes.filter(is_active=True, user=user.id).exists()  
        return False


class Comment(models.Model):
    message=models.CharField(max_length=400)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created=models.DateTimeField(default=timezone.now)
    date_updated=models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.date_updated=timezone.now()
        super(Comment,self).save(*args,**kwargs)

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="likes", on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    is_active=models.BooleanField(default=True)
    date_updated=models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.date_updated=timezone.now()
        super(Like,self).save(*args,**kwargs)


