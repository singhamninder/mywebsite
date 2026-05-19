from django.db import models

# from captcha.fields import ReCaptchaField
# from captcha.widgets import ReCaptchaV2Checkbox


class Info(models.Model):
    cv = models.FileField()
    mainImage = models.ImageField(null=True, blank=True, default="default.jpg")
    profile_image = models.ImageField(null=True, blank=True, default="default.jpg")
    short_intro = models.TextField(null=True, blank=True)
    linkedin = models.CharField(max_length=2000, null=True, blank=True)
    twitter = models.CharField(max_length=2000, null=True, blank=True)

    def __str__(self):
        return "MyInformation"


class Skill(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Work(models.Model):
    startdate = models.CharField(max_length=60, null=True, blank=True)
    enddate = models.CharField(max_length=60, null=True, blank=True)
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]


class Project(models.Model):
    title = models.CharField(max_length=200)
    impact_summary = models.CharField(max_length=280, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    image1 = models.ImageField(null=True, blank=True, default="default.jpg")
    image2 = models.ImageField(null=True, blank=True, default="default.jpg")
    image3 = models.ImageField(null=True, blank=True, default="default.jpg")
    code_url = models.URLField(max_length=2000, null=True, blank=True)
    demo_url = models.URLField(max_length=2000, null=True, blank=True)
    project_link = models.TextField(max_length=500, null=True, blank=True)
    publication_link = models.TextField(max_length=2000, null=True, blank=True)
    featured = models.BooleanField(default=False)
    tags = models.ManyToManyField("Tag", blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created"]


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
        ordering = ["-no"]


class Contact(models.Model):
    contactName = models.CharField(max_length=60)
    contactEmail = models.EmailField(max_length=300)
    contactSubject = models.CharField(max_length=200)
    contactMessage = models.TextField(max_length=1000)
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

    is_read = models.BooleanField(default=False, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contactName

    class Meta:
        ordering = ["is_read", "-created"]


# This model allows you to add references to each project, with a title and URL.
class Reference(models.Model):
    project = models.ForeignKey(
        "Project", on_delete=models.CASCADE, related_name="references"
    )
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"{self.title[:50]}... - {self.project.title}"
