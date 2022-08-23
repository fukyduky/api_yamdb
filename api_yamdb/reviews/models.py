from django.db import models


class Category(models.Model):
    """Категории (типы) произведений («Фильмы», «Книги», «Музыка»)"""

    name = models.CharField(
        max_length=256,
        verbose_name="Название категории",
    )
    # Поле slug каждой категории должно быть уникальным.
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Идентификатор категории",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений"""

    name = models.CharField(
        max_length=256,
        verbose_name="Название жанра",
    )
    # Поле slug каждой категории должно быть уникальным.
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name="Идентификатор жанра",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы"""

    name = models.CharField("Название", max_length=50)
    year = models.IntegerField("Год выпуска")
    description = models.CharField("Описание", max_length=256)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="category",
        verbose_name="Категория",
        help_text="Категория, к которой относится произведение",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"

    def __str__(self):
        return self.name
