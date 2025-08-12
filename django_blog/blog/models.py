from django.db import models  # Import Django's ORM base classes
from django.contrib.auth.models import User   
from django.db.models.signals import post_save  # signal triggered after saving a model instance
from django.dispatch import receiver  # Decorator to register signal handlers
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

class Profile(models.Model):

    # one-to-one relationship with User; each user has exactly one profile
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)  # Optional user bio, can be left blank
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Optional profile picture stored in 'avatars/' directory 
   
    def __str__(self):
        # String representation for this object, useful in admin and shell
        return f"{self.user.username} Profile " 
# Signal reciever to create Profile automatically when a user is created
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    if created:
        # If new user created, create an associated Profile object
        Profile.objects.create(user=instance)

# Signal reciever to save Profile whenever the user is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Save the related Profile (to persist changes)
    instance.profile.save()
    