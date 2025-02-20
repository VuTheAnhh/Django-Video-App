from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from video.models import Video
from django.utils.text import slugify

GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class User(AbstractUser):
    uid = ShortUUIDField(length=10, max_length=10, alphabet='qwertyuiopasdfghjklzxcvbnm')

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
    def __unicode__(self):
        return self.username
    
class Group(models.Model):
    group_name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="branch_group", default="venesa.png")
    member = models.ManyToManyField(User, related_name='members', blank=True)
    video = models.ManyToManyField(Video, related_name='videos', blank=True)
    slug = models.SlugField(unique=True, max_length=200, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Branch_Group"
    
    def __str__(self):
        return self.group_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.group_name)
        super().save(*args, **kwargs)
    
    
