from django.db import models

class Info(models.Model): 
    cv = models.FileField()
    mainImage = models.ImageField(null=True, blank=True, default="default.jpg")
    short_intro = models.TextField(null=True, blank=True)
    linkedin = models.CharField(max_length=2000, null=True, blank=True)
    twitter = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return str(self.short_intro)

class Skill(models.Model): 
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

class Work(models.Model):
    startdate = models.CharField(max_length=60,null=True, blank=True)
    enddate = models.CharField(max_length=60,null=True, blank=True)
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    publication_link = models.TextField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Publication(models.Model):
    no = models.CharField(max_length=60)
    title = models.TextField(max_length=2000)
    link = models.TextField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.no

    class Meta:
        ordering = ['-no']

# class Contact(models.Model):
#     name = models.CharField(max_length=60)
#     email = models.EmailField(max_length=300)
#     subject = models.CharField(max_length=200)
#     message = models.TextField(max_length=1000)
#     is_read = models.BooleanField(default=False, null=True)
#     created = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ['is_read', '-created']