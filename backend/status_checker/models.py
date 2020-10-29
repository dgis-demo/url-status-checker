from django.db import models
from django.contrib.auth import get_user_model


class Url(models.Model):
    # Just for Pycharm highlighting
    objects = models.Manager()

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    url = models.URLField()
    status_code = models.IntegerField(null=True, blank=True)
    check_status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.url)
