from django.db import models

class Part(models.Model):
    """
    Parts model
    """
    class IsActiveOptions(models.IntegerChoices):
        ACTIVE = 1
        INACTIVE = 0

    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=30)
    description = models.CharField(max_length=1024)
    weight_ounces = models.IntegerField()
    is_active = models.SmallIntegerField(choices=IsActiveOptions.choices)

    class Meta:
        db_table = 'part'
