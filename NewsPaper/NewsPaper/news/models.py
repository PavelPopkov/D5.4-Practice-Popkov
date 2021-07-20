from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from datetime import datetime


class Author(models.Model):
    author = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author

    # .aggregate(Sum("rating"))
    def update_rating(self):
        auth = Author.objects.get(author=self.author)
        sum_rat_post = 0
        posts = auth.post_set.all()
        for post in posts:
            sum_rat_post += post.rating_post * 3

        usr = auth.one_to_one_rel
        sum_rat_comm = 0
        comments = usr.comment_set.all()
        for comm in comments:
            sum_rat_comm += comm.rating_comm

        sum_rat_auth = 0
        # comments_posts = auth.post_set.comment_set.all()
        for post in posts:
            comm_posts = post.comment_set.all()
            for comm_post in comm_posts:
                sum_rat_auth += comm_post.rating_comm

        self.rating = sum_rat_post + sum_rat_comm + sum_rat_auth
        self.save()


class Category(models.Model):
    category = models.CharField(max_length=100, unique=True)

class Post(models.Model):
    article = 'AR'
    new = 'NE'
    POSITIONS = [
        (article, 'Статья'),
        (new, 'Новость')
    ]
    ar_or_new = models.CharField(max_length=2,
                                 choices=POSITIONS,
                                 default=article)
    created = models.DateTimeField(auto_now_add=True)
    post_name = models.CharField(max_length=250)
    content = models.TextField()
    rating = models.IntegerField(default=0)

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        if self.rating_comm < 0:
            self.rating_comm = 0
        self.save()

    def preview(self):
        prev = self.content[:124] + '...'
        return prev

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        if self.rating < 0:
            self.rating = 0
        self.save()
