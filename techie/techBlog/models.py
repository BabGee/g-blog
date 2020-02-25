from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

STATUS = ((0, 'Draft'), (1, 'Publish'),)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    description = models.TextField(max_length=400, default='')
    phone = models.IntegerField(default=0)
    website = models.URLField(default='')

    def __str__(self):
        return self.user.username


def post_save_profile_create(sender, instance, created,*args, **kwargs):
	if created:
		Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=User)        
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    decription = models.TextField(default='This Category includes the following areas: ')

    def __str__(self):
        return self.name

class Post(models.Model):
    image = models.ImageField(default='default.jpg', upload_to='post_pics')
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts'
    )
    updated_on = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse('post_detail', kwargs={'slug': str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {} of email {}'.format(self.body, self.name, self.email)

