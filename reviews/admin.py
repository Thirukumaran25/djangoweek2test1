

# Register your models here.
from django.contrib import admin
from .models import Book, Review,Category

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'book__author')
    search_fields = ('comment', 'user__username')


admin.site.register(Category)