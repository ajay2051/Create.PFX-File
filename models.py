from django.db import models

class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save()

    def hard_delete(self):
        super().delete()

    objects = SoftDeleteManager()


class Certificates(BaseModel):
    certificate_name = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )
    certificate_description = models.CharField(max_length=255, null=False, blank=False)
    certificate_file_path = models.FileField(
        upload_to="client/certificate/", blank=True, null=True
    )
    certificate_password = models.CharField()

    def __str__(self):
        return self.certificate_name


class ExternalUsers(BaseModel):
    external_user_name = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )
    external_user_email = models.CharField(
        max_length=255, unique=True, null=False, blank=False
    )
    external_user_password = models.CharField()
    certificates = models.OneToOneField(
        Certificates, null=True, on_delete=models.SET_NULL
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.external_user_name