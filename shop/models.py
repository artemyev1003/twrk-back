import os
from PIL import Image
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Product(models.Model):
    class Meta:
        verbose_name = _('product')
        verbose_name_plural = _('products')

        ordering = ['title']

    class Status(models.TextChoices):
        IN_STOCK = 'in_stock', _('in stock')
        ON_ORDER = 'on_order', _('on order')
        EXPECTED = 'expected', _('expected to arrive')
        OUT_OF_STOCK = 'out_of_stock', _('out of stock')
        NOT_PRODUCED = 'not_produced', _('not produced')

    title = models.CharField(_('title'), max_length=255)
    sku = models.CharField(_('sku'), max_length=255, unique=True)
    price = models.DecimalField(_('price'), max_digits=6, decimal_places=2, null=True)
    status = models.CharField(_('status'), max_length=20, choices=Status.choices,
                              default=Status.IN_STOCK)
    image = models.ImageField(_('image'), blank=True, upload_to='images/')
    slug = models.SlugField(_('slug'), max_length=255)
    category = models.ForeignKey(verbose_name=_('category'), to='Category',
                                 on_delete=models.PROTECT, related_name='products')

    def convert_to_webp(self):
        f_name = self.image.name.rsplit('.', 1)
        # Check if the image has .jpg/.png extension
        # and if it already exists it the media directory
        if f_name[-1] in ['jpg', 'png'] \
                and not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'images', self.image.name)):

            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'images')):
                os.makedirs(os.path.join(settings.MEDIA_ROOT, 'images'))

            img = Image.open(self.image)
            webp_file_name = f'{f_name[0]}.webp'
            image_path = os.path.join(settings.MEDIA_ROOT, 'images', webp_file_name)
            img.save(image_path, 'webp')

    def save(self, *args, **kwargs):
        if self.image:
            self.convert_to_webp()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Category(models.Model):
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

        ordering = ['title']

    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), max_length=255)

    property_objects = models.ManyToManyField(verbose_name=_('properties'), to='PropertyObject')

    def __str__(self):
        return self.title


class PropertyObject(models.Model):
    class Meta:
        verbose_name = _('property object')
        verbose_name_plural = _('properties objects')

        ordering = ['title']

    class Type(models.TextChoices):
        STRING = 'string', _('string')
        DECIMAL = 'decimal', _('decimal')

    title = models.CharField(_('title'), max_length=255)
    code = models.SlugField(_('code'), max_length=255)
    value_type = models.CharField(_('value type'), max_length=10, choices=Type.choices)

    def __str__(self):
        return f'{self.title} ({self.get_value_type_display()})'


class PropertyValue(models.Model):
    class Meta:
        verbose_name = _('property value')
        verbose_name_plural = _('properties values')

        ordering = ['value_string', 'value_decimal']

    property_object = models.ForeignKey(to=PropertyObject, on_delete=models.PROTECT)

    value_string = models.CharField(_('value string'), max_length=255, blank=True, null=True)
    value_decimal = models.DecimalField(_('value decimal'),
                                        max_digits=11, decimal_places=2, blank=True, null=True)
    code = models.SlugField(_('code'), max_length=255)

    products = models.ManyToManyField(to=Product, related_name='properties')

    def __str__(self):
        return str(getattr(self, f'value_{self.property_object.value_type}', None))
