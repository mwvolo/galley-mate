from django.db import models
import datetime
from positions.fields import PositionField
from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


class Source(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Source|name'))
    url = models.URLField(max_length=500, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Source')
        verbose_name_plural = _('Sources')
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=120,
                            unique=True,
                            help_text="Maximum 120 characters",
                            verbose_name=_('Category|name'))
    slug = models.SlugField(unique=True, help_text='Automatically generated from the title')
    order_index = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['order_index']


class FoodGroup(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('FoodGroup|name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('FoodGroup')
        verbose_name_plural = _('FoodGroups')
        ordering = ['name']


class Photo(models.Model):
    caption = models.CharField(max_length=200, verbose_name=_('Photo|caption'))
    recipe = models.ForeignKey('Recipe')
    image = models.ImageField(upload_to='images')
    # This field used because can't make ImageField core right now (see http://code.djangoproject.com/ticket/2534)
    keep = models.BooleanField(default=True, editable=False)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')


# def save(self):
# Don't save if there is no image (since core field is always set).


# if not self.id and not self.image:
# return
#        super(Photo, self).save()


class Recipe(models.Model):
    title = models.CharField(max_length=50, verbose_name=_('Recipe|title'))
    summary = models.CharField(max_length=500, blank=True, verbose_name=_('Recipe|summary'))
    description = models.TextField(blank=True, verbose_name=_('Recipe|description'))
    slug = models.SlugField(unique=True, max_length=50, null=False, blank=False)
    prep_time = models.CharField(max_length=100, blank=True)  # This field type is a guess.
    ctime = models.DateTimeField(auto_now_add=True)
    mtime = models.DateTimeField(auto_now=True)
    sources = models.ManyToManyField(Source, blank=True)
    category = models.ForeignKey(Category)
    serving_value = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('Recipe')
        verbose_name_plural = _('Recipies')

    def save(self):
        self.mtime = datetime.datetime.now()
        self.scale = 1.0
        super(Recipe, self).save()

    def get_directions(self):
        a = []
        for direction in self.directions.all():
            ingredients = []
            for ingredient in direction.ingredients.all():
                ingredients.append((ingredient.amount,
                                    ingredient.unit.name,
                                    ingredient.formatted_food(),
                                    ingredient.food.detail))
            a.append((direction.text, ingredients))
        return a


class DirectionManager(models.Manager):
    def all(self):
        return self.prefetch_related('ingredients', 'ingredients__unit', 'ingredients__food',)


class Direction(models.Model):
    """
    A direction is a step in a recipe's preparation and each recipe can have
    multiple directions but obviously, each direction only applies to one
    recipe.
    """
    text = models.TextField(blank=True, verbose_name=_('Direction|text'))
    recipe = models.ForeignKey(Recipe, related_name='directions')
    order = PositionField(blank=True, null=True, unique_for_field='recipe')

    objects = DirectionManager()

    def __str__(self):
        ret = self.text[:40]
        if len(self.text) > 40:
            ret += "..."
        return ret

    class Meta:
        verbose_name = _('Direction')
        verbose_name_plural = _('Directions')
        ordering = ['order', 'id']


class Unit(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=_('Unit|name'))
    name_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Unit|name_abbrev'))
    plural_abbrev = models.CharField(max_length=60, blank=True, verbose_name=_('Unit|plural_abbrev'))
    TYPE = Choices((0, 'other', 'Other'), (1, 'mass', 'Mass'), (2, 'volume', 'Volume'))
    type = models.IntegerField(choices=TYPE)
    SYSTEM = Choices((0, 'si', 'SI'), (1, 'imperial', 'Imperial'))
    system = models.IntegerField(choices=SYSTEM, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')
        ordering = ["name"]


class Food(models.Model):
    name = models.CharField(max_length=150, verbose_name=_('Food|name'))
    name_sorted = models.CharField(max_length=150, default='', verbose_name=_('Food|name_sorted'))
    group = models.ForeignKey(FoodGroup)
    name_plural = models.CharField(max_length=150, null=True, blank=True)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.name_sorted

    class Meta:
        verbose_name = _('Food')
        verbose_name_plural = _('Foods')
        ordering = ["name_sorted", ]


class Ingredient(models.Model):
    amount = models.FloatField(null=True, blank=True, verbose_name=_('Ingredient|amount'))
    unit = models.ForeignKey(Unit, null=True, blank=True)
    recipe = models.ForeignKey(Recipe)
    food = models.ForeignKey(Food)
    order_index = PositionField(blank=True, null=True, unique_for_field="direction")
    direction = models.ForeignKey(Direction, related_name='ingredients', null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(Ingredient, self).__init__(*args, **kwargs)

    def formatted_food(self):
        if self.food.name_plural != None and self.food.name_plural != '' and (
                        self.amount != 1):
            food_str = self.food.name_plural
        else:
            food_str = self.food.name
        return food_str

    def __str__(self):
        return self.formatted_food()

    class Meta:
        ordering = ["direction", "order_index", "id"]
        verbose_name = _('Ingredient')
        verbose_name_plural = _('Ingredients')

