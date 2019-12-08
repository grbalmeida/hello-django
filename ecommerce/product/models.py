import os
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from PIL import Image
from utils import format_price

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=255)
    long_description = models.TextField()
    image = models.ImageField(upload_to='product_images/%Y/%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    price_marketing = models.FloatField()
    promotional_price_marketing = models.FloatField(default=0)
    product_type = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variation'),
            ('S', 'Simple')
        )
    )

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)

        if self.image:
            self.resize_image(self.image, new_width=800)

    def get_formatted_price_marketing(self):
        return format_price.format_price(self.price_marketing)

    get_formatted_price_marketing.short_description = 'Price Marketing'

    def get_formatted_promotional_price_marketing(self):
        return format_price.format_price(self.promotional_price_marketing)

    get_formatted_promotional_price_marketing.short_description = 'Promotional Price Marketing'

    @staticmethod
    def resize_image(image, new_width=800):
        image_full_path = os.path.join(settings.MEDIA_ROOT, image.name)
        image_pil = Image.open(image_full_path)

        original_width, original_height = image_pil.size

        if original_width <= new_width:
            image_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_image = image_pil.resize((new_width, new_height), Image.LANCZOS)

        new_image.save(
            image_full_path,
            optimize=True,
            quality=60
        )

    def __str__(self):
        return self.name

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    promotional_price = models.FloatField(default=0)
    stock = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'

    def __str__(self):
        return self.name or self.product.name
