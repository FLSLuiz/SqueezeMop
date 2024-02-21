from django.conf import settings
from django.db import models
import os
from PIL import Image
from django.utils.text import slugify

# Create your models here.

"""
PRODUCT:
    name - char
    short_description - text
    long_description - text
    image - image
    slug - slug => tipo ID
    selling_price - float
    discounted_price - float
    type - choice ('v', 'variable' | 's' 'simple')
"""

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(
        upload_to = 'product_images/', blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    selling_price = models.FloatField(verbose_name='Price')
    discounted_price = models.FloatField(verbose_name='Discounted Price')
    type = models.CharField(
        default = 'V',
        max_length = 1,
        choices = (
            ('V', 'Variable'),
            ('S', 'Simple'),
        )
    )
    # Formatted selling price
    def get_formatted_price(self):
        return self.selling_price
    get_formatted_price.short_description = 'Price'

    # Formatted discounted price
    def get_formatted_discounted_price(self):
        return self.discounted_price
    get_formatted_discounted_price.short_description = 'Discounted Price'

    # Resizing image
    @staticmethod  
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return
        
        new_height = round((new_width * original_height) / original_width)
        
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.image:
            self.resize_image(self.image, max_image_size)

    def __str__(self): # returns the name of the product 
        return self.name
    

"""
    VARIATION:
        name - char
        product - FK product
        price - float
        discount_price - float
        stock - int
"""

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255, blank=True, null=True)
    price = models.FloatField()
    discount_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default = 1)

    def __str__(self): # returns the name of the variation
        return self.name or self.product.name
    
    class Meta:
        verbose_name = 'variation'
        verbose_name_plural = 'variations'



    