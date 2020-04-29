from django.db import models

class Reporter(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

class Article(models.Model):
    headline = models.CharField(max_length=100)
    pub_date = models.DateField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ['headline']


>>> new_article = r.article_set.create(headline="John's second story", pub_date=date(2005, 7, 29))
>>>r.article_set.filter(headline__startswith='This')
>>> Article.objects.filter(reporter__first_name='John')
>>> Article.objects.filter(reporter__pk=1)
>>> Article.objects.filter(reporter=1)
>>> Article.objects.filter(reporter=r)
>>> Article.objects.filter(reporter__in=[1,2]).distinct()
>>> Article.objects.filter(reporter__in=[r,r2]).distinct()
>>> Reporter.objects.filter(article=1)
>>> Reporter.objects.filter(article=a)
>>> Reporter.objects.filter(article__headline__startswith='This')
>>> Reporter.objects.filter(article__headline__startswith='This').distinct()
>>> Reporter.objects.filter(article__reporter__first_name__startswith='John').distinct()
>>> Reporter.objects.filter(article__reporter=r).distinct()
>>> Article.objects.all()
>>> Reporter.objects.order_by('first_name')
>>> r2.delete()
>>> Article.objects.all()
>>> Reporter.objects.order_by('first_name')
