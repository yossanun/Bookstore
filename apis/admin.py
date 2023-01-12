from django.contrib import admin
from .models import Author, Book, Member, Transaction, Configuration

# Register your models here.
admin.site.register(Author)

class AuthorModelAdmin(admin.ModelAdmin):
    list_display = '__all__'


admin.site.register(Book)

class BookModelAdmin(admin.ModelAdmin):
    list_display = '__all__'


admin.site.register(Member)

class MemberModelAdmin(admin.ModelAdmin):
    list_display = '__all__'


admin.site.register(Transaction)

class TransactionModelAdmin(admin.ModelAdmin):
    list_display = '__all__'


admin.site.register(Configuration)

class ConfigurationModelAdmin(admin.ModelAdmin):
    list_display = '__all__'


