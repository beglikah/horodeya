from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
from django.urls import reverse


# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=100)
    document = models.FileField(upload_to='documents/')
    slug = models.SlugField(
        _('Slug'),
        default='slug',
        max_length=200,
        help_text=_(
            """Slug will be generated automatically from the title of the
            document!""")
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,
        related_name='uploaded_by_user'
    )

    def doc_name(self):
        return self.document.name.split('/')[-1]

    def get_absolute_url(self):
        return reverse('documents:document_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Document, self).save(*args, **kwargs)
