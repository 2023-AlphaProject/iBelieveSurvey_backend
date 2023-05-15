from django.db import models


class Category(models.Model):
    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    type = models.CharField(verbose_name="카테고리 타입", max_length=255, null=False)

    def __str__(self):
        return self.type
