from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.

# Class for posts
class Post(models.Model):
    # The author is a superuser on the website
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    # After post is made, this function directs user to the post detail page/view
    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return self.title
    
# Class for comments
class Comment(models.Model):

    # Anone can be a comment author
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    # After user has left a comment, it does not make sense to take them to the post details
    # instead it goes to the list of posts (post listview)

    def get_absolute_url(self):
        return reverse("blog:posts_list")
    

    def __str__(self):
        return self.text