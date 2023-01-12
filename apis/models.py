from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    price = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    def __str__(self):
        return f"Title:{self.name} {self.price} Bath, Get {self.point} Point"


class Member(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    point = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Transaction(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    is_use_point = models.BooleanField(default=False, blank=True, null=True)
    is_use_cash = models.BooleanField(default=False, blank=True, null=True)
    use_point = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)
    use_cash = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)
    add_point = models.DecimalField(max_digits=10, decimal_places=3, default=0, blank=True, null=True)


class Configuration(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
