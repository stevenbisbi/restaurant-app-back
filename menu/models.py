from django.db import models
import uuid
from restaurant.models import Restaurant
# Create your models here.

class Menu(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menus")
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name


class MenuItem(models.Model):
  CATEGORY_CHOICES = [
    ("Entradas", "Entradas"),
    ("Plato Fuerte", "Plato Fuerte"),
    ("Postres", "Postres"),
    ("Bebidas", "Bebidas"),
    ("Combo", "Combo"),
    ("Salchipapas", "Salchipapas"),   
    ("Hamburguesas", "Hamburguesas"),   
    ("Emparedados", "Emparedados"),   
    ("Perros", "Perros"),      
  ]
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
  name = models.CharField(max_length=100)
  description = models.CharField(blank=False, null=False, max_length=200, default="Sin descripción")
  price = models.IntegerField()
  image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
  is_vegetarian = models.BooleanField(default=False)
  is_featured = models.BooleanField(default=False)
  is_promotion = models.BooleanField(default=False)
  is_available = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  

  def __str__(self):
      return self.name

class MenuItemVariant(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="variants")
  name = models.CharField(max_length=100)
  description = models.TextField(blank=True, null=True)
  price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  is_default = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.menu_item.name} - {self.name}"

class MenuItemOption(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name="options")
  name = models.CharField(max_length=100)
  price_adjustment = models.IntegerField(default=2000)
  allows_multiple = models.BooleanField(default=True)
  max_selections = models.IntegerField(default=5)
  image_url = models.URLField(max_length=255, blank=True, null=True)
  is_available = models.IntegerField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return f"{self.menu_item.name} - {self.name}"
