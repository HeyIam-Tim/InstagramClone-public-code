from django.db import models
from django.contrib.auth.models import User


class InstagramUser(models.Model):
  user = models.OneToOneField(User, blank=True, on_delete=models.CASCADE, primary_key=True)
  profile_pic = models.ImageField(default='default_user_icon.png', null=True, blank=True)
  follower = models.ManyToManyField(User, related_name='follower', default=None, blank=True)
  following = models.ManyToManyField(User, related_name='following', default=None, blank=True)
  date_created = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return self.user.username

  @property
  def followers(self):
    return self.follower.all().count()

  @property
  def followings(self):
    return self.following.all().count()


class Publication(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
  liked = models.ManyToManyField(User, related_name='publication_like', default=None, blank=True)
  pub_date = models.DateTimeField(auto_now_add=True, null=True)
  image = models.ImageField(null=True, blank=True)
  description = models.CharField(max_length=200, null=True, blank=True)

  def __str__(self):
    return self.description

  @property
  def likes(self):
    return self.liked.all().count()


class SwitchTheme(models.Model):
  user = models.OneToOneField(InstagramUser, blank=True, on_delete=models.CASCADE, primary_key=True)
  theme = models.CharField(default='https://timbucketaws.s3.amazonaws.com/static/css/main.css', max_length=200, null=True, blank=True)

  def __str__(self):
    return self.theme


class Comment(models.Model):
  publication = models.ForeignKey(Publication, related_name='comments', blank=True, on_delete=models.CASCADE)
  author = models.CharField(max_length=200, null=True, blank=True)
  body = models.TextField()
  date_added = models.DateTimeField(auto_now_add=True, null=True)

  def __str__(self):
    return '%s - %s - %s' % (self.author, self.publication.description, self.body[:20])