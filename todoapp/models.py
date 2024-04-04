from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# def get_default_user():
#     return User.objects.get(username='admin') if User.objects.filter(username='admin').exists() else None
def get_default_user():
    pass

class TODO(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    is_done = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True) 
    image = models.ImageField(upload_to= 'images/', blank=True,null=True)

    def __str__(self):
        return self.title