from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group

paper = 'PP'
news = 'NW'

KINDS = [
    (paper, 'статья'),
    (news, 'новость')
]

class Author(models.Model):
    author_rating = models.IntegerField(default=0)
    author = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username

    def update_rating(self):
        auth = Author.objects.get(author=self.author)
        postRat = auth.post_set.all().aggregate(rating=Sum('post_rating'))
        pRat = 0
        pRat += postRat.get('rating')

        usr = User.objects.get(username=auth.author)
        commentRat = usr.comment_set.all().aggregate(crating=Sum('comment_rating'))
        cRat = 0
        cRat += commentRat.get('crating')
        self.author_rating = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    news_category = models.CharField(max_length=150, unique=True)
    subscribers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.news_category

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    kind = models.CharField(max_length=2, choices=KINDS, default=paper)
    post_data = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    heading = models.CharField(max_length=255)
    content = models.TextField()
    post_rating = models.IntegerField(default=0)


    def get_absolute_url(self):
        return f'/news/{self.id}'

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating > 0:
            self.post_rating -= 1
            self.save()

    def preview(self):
        return self.content[:124] + '...'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post.heading} - {self.category.news_category}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    comment_data = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        if self.comment_rating > 0:
            self.comment_rating -= 1
            self.save()


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user