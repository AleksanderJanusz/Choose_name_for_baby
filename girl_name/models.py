from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Names(models.Model):
    GENDER_CHOICES = (
        (0, 'Chłopiec'),
        (1, 'Dziewczynka'),
        (2, 'Nie podano'),
    )
    name = models.CharField(max_length=256)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=2)
    user = models.ManyToManyField(User, through='Choice')

    def __str__(self):
        return self.name


class Choice(models.Model):
    CHOICES = (
        (0, 'Tak'),
        (1, 'Nie'),
        (2, 'Jeszcze nie wiem'),
    )
    choice = models.IntegerField(choices=CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.ForeignKey(Names, on_delete=models.CASCADE)
    choice_change_date = models.DateTimeField(auto_now=True, null=True)
