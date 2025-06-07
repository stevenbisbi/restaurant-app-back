from django.contrib import admin
from django.utils.html import format_html
from .models import Menu, MenuItem, MenuItemVariant, MenuItemOption

admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(MenuItemVariant)

@admin.register(MenuItemOption)
class MenuItemOptionAdmin(admin.ModelAdmin):
  list_display = ("menu_item", "name", "price_adjustment", "is_available", "image_preview")

  def image_preview(self, obj):
    if obj.image_url:
      return format_html(f'<img src="{obj.image_url}" style="height:30px;" />')
    return "No image"
  image_preview.short_description = "Icon"
  
  