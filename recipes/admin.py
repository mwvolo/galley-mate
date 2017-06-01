from django.contrib import admin
from .models import *


class SourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order_index')
    prepopulated_fields = {'slug': ('name',)}


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name_sorted', 'name', 'group',)
    list_filter = ('group',)
    search_fields = ('name',)


class PhotoInlineAdmin(admin.StackedInline):
    model = Photo
    extra = 2


class DirectionInlineAdmin(admin.TabularInline):
    model = Direction
    extra = 3


class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'name_abbrev', 'plural_abbrev', 'system', 'type',)


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ('food', 'unit', 'amount', 'direction',)


class IngredientInlineAdmin(admin.TabularInline):
    model = Ingredient
    extra = 6

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # if db_field.name == "direction":
        #     recipe = request.resolver_match.args[0]
        #     kwargs["queryset"] = Direction.objects.filter(recipe=recipe)
        return super(IngredientInlineAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'summary', 'slug', 'prep_time',)
    fields = ('title', 'slug', 'category', 'summary', 'description', 'serving_value', 'sources', 'prep_time',)
    list_filter = ('title', 'sources',)
    search_fields = ('title', 'description', 'summary',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    model = Recipe
    inlines = [DirectionInlineAdmin, IngredientInlineAdmin, PhotoInlineAdmin]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs["queryset"] = Category.objects.all().order_by('name')
        return super(RecipeAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Source, SourceAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(FoodGroup)
admin.site.register(Food, FoodAdmin)
admin.site.register(Photo)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Ingredient, IngredientAdmin)
