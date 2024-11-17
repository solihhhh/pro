from django.contrib import admin
from .models import Product, Like, Comment, Cart

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ['name']

class LikeAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'liked', 'created_at')
    list_filter = ['liked']
    search_fields = ('user__username', 'product__name')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'comment_text', 'created_at')
    search_fields = ('user__username', 'product__name')

class CartAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'quantity', 'created_at')
    search_fields = ('user__username', 'product__name')

admin.site.register(Product, ProductAdmin)
admin.site.register(Like, LikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Cart, CartAdmin)
# admin panel: user: admin password:12345