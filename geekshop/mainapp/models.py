from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название', unique=True)
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'#{self.pk} {self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ('pk', )


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=128, verbose_name='Название')
    product_code = models.CharField(max_length=20, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    price_our = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Старая_Цена')
    link_text = models.CharField(max_length=128, verbose_name='Ссылка')
    link_img = models.CharField(max_length=128, verbose_name='Ссылка_на_изображение')

    def __str__(self):
        return f'#{self.pk} {self.product_code} {self.name} ({self.category.name})'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ('pk',)


