from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length=200, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="user_Posts")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="post_likes")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return str(self.user) + ' ' + str(self.date.date()) 



class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to = "user_ProfilePics",default="default/defaultuser.png")
    about = models.CharField(max_length=200, blank=True)
    connection = models.CharField(max_length =200, blank=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user)

class Likepost(models.Model):
    user = models.ManyToManyField(User, related_name="linkedUser")
    post = models.OneToOneField(Post, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)



    @classmethod
    def liked(cls, post, userliking):
        obj , create = cls.objects.get_or_create(post = post)
        obj.user.add(userliking)

    @classmethod
    def dislike(cls, post, userdislike):
        obj , create = cls.objects.get_or_create(post = post)
        obj.user.remove(userdislike)

    def __str__(self):
        return str(self.post)

class Following(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    followed= models.ManyToManyField(User, related_name="followed")
    follower = models.ManyToManyField(User, related_name="follower")

    @classmethod
    def follow(cls, user, another_account):
        obj,create = cls.objects.get_or_create(user = user)
        obj.followed.add(another_account)
        print("followed")

    @classmethod
    def unfollow(cls, user, another_account):
        obj,create = cls.objects.get_or_create(user = user)
        obj.followed.remove(another_account)
        print("unfollowed")

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete= models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add= True)
    reply = models.ForeignKey('Comment', null = True, related_name="replies", on_delete=models.CASCADE)


    def __str__(self):
        return '{}-{}'.format(self.post.pk, str(self.user.username))

    


