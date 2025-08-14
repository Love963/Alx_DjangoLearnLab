from django.db import models  # Import Django's ORM base classes
from django.contrib.auth.models import User     # Import User model for authors
from django.db.models.signals import post_save  # signal triggered after saving a model instance
from django.dispatch import receiver  # Decorator to register signal handlers
from django.urls import reverse       # Build URLs dynamically from URL names
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=200)    # Post title, Short text
    content = models.TextField()                # Full blog content, long text
    # auto_now_add sets timestamp automatically when a Post is created
    published_date = models.DateTimeField(auto_now_add=True) 
    # author link to User; cascade delete removes posts if user deleted
    # related_name allows user.posts.all() to fetch all posts by user
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-published_date']   # newest first in lists

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
    

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

class Comment(models.Model):
    # Many-to-one relationship: a post can have many comments
    # related name='comments' allows post.comments.all() to fetch them.
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # Each comment is linked to a user
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # The actual text of the comment
    content = models.TextField()
    # Timestamp when comment is created
    created_at =models.DateTimeField(auto_now_add=True)
    # Timestamp updated whenever comment is saved (for edits)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created_at']   # comments are displayed oldest first by default
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    def get_absolute_url(self):
        # Redirect back to the post detail page after comment actions.
        return reverse("post_detail", kwargs={"pk": self.post.pk})
    
   


    