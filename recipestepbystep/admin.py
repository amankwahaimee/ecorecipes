from django.contrib import admin
from .models import Recipe, Timeofday, Location
from .models import RecipeStep, Nutrient, CookingAppliance, CookingMethod
from .models import SubstituteCookingMethod, Ingredient, IngredientSubstitute


class CookingApplianceAdmin(admin.ModelAdmin):
    list_display = ('name', 'CO2')


class CookingMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'CO2', 'nutrition_loss')


class NutrientAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')


class TimeofdayAdmin(admin.ModelAdmin):
    list_display = ('time_of_day', 'emission_multiplier')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_name', 'location_emission_factor')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'nutritional_value_key', 'nutritional_value',
                    'emissions_key', 'emissions')


class IngredientSubstituteAdmin(admin.ModelAdmin):
    list_display = ('name',
                    'nutritional_value_key', 'nutritional_value',
                    'emissions_key', 'emissions')


class SubstituteCookingMethodAdmin(admin.ModelAdmin):
    list_display = ('substitute_cooking_method', 'fuel', 'emissions')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'cooking_time_minutes', 'cooking_method',
                    'serving_size', 'foodtags', 'emissions_key', 'nutritional_value_key')


class RecipeStepAdmin(admin.ModelAdmin):
    list_display = ('order', 'content', 'ventilation')


admin.site.register(Timeofday, TimeofdayAdmin)
admin.site.register(Location, LocationAdmin, )
admin.site.register(SubstituteCookingMethod, SubstituteCookingMethodAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientSubstitute, IngredientSubstituteAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeStep, RecipeStepAdmin)
admin.site.register(CookingAppliance, CookingApplianceAdmin)
admin.site.register(CookingMethod, CookingMethodAdmin)
admin.site.register(Nutrient, NutrientAdmin)
