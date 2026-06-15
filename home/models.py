from django.db import models


class Info(models.Model):
    cv = models.FileField()
    mainImage = models.ImageField(null=True, blank=True, default="default.jpg")
    profile_image = models.ImageField(null=True, blank=True, default="default.jpg")
    short_intro = models.TextField(null=True, blank=True)
    linkedin = models.CharField(max_length=2000, null=True, blank=True)
    google_scholar = models.URLField(max_length=2000, null=True, blank=True)
    github = models.URLField(max_length=2000, null=True, blank=True)
    email = models.EmailField(max_length=300, null=True, blank=True)

    def __str__(self):
        return "MyInformation"


class Skill(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class Work(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)  # null = Present
    title = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = [models.F("end_date").desc(nulls_first=True), "-start_date"]


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


# This model allows you to add related publications to each project.
class RelatedPublication(models.Model):
    project = models.ForeignKey(
        "Project",
        on_delete=models.CASCADE,
        related_name="related_publications",
    )
    title = models.CharField(max_length=500)
    url = models.URLField(max_length=2000)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created"]
        verbose_name = "Related publication"
        verbose_name_plural = "Related publications"

    def __str__(self):
        title = str(self.title)
        return f"{title[:50]}... - {self.project.title}"


class TechStackGroup(models.Model):
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class TechStackItem(models.Model):
    group = models.ForeignKey(
        TechStackGroup,
        on_delete=models.CASCADE,
        related_name="items",
    )
    name = models.CharField(max_length=200)
    icon_url = models.URLField(max_length=2000, blank=True)
    label = models.CharField(max_length=20, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name
