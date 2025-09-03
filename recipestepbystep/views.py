from django.shortcuts import render, get_object_or_404
from .models import Recipe, Location, Timeofday, Ingredient, IngredientSubstitute


def index(request):
    recipes = Recipe.objects.all()
    locations = Location.objects.all()
    timeofdays = Timeofday.objects.all()

    selected_timeofday = None
    selected_recipe = None
    selected_location = None
    recipe_steps = None

    current_ingredients = []
    ingredient_percent_change = []
    changes = []

    total_ingredient_emissions_current = 0
    total_ingredient_emissions_previous = 0
    percent_emissions_reduced = 0

    ingredient_replacements_dictionary = request.session.get(
        'ingredient_replacements', {})

    # pressing a button fetches old ingredient and new ingredient
    if request.method == 'POST' and 'replaced_ingredient_id' in request.POST:
        replaced_ingredient_id = request.POST.get('replaced_ingredient_id')
        replacing_ingredient_id = request.POST.get('replacing_ingredient_id')

        # replacements is a dictionary (old id: new id)
        if replaced_ingredient_id and replacing_ingredient_id:
            ingredient_replacements_dictionary[replaced_ingredient_id] = replacing_ingredient_id
            request.session['ingredient_replacements'] = ingredient_replacements_dictionary
            request.session.modified = True

    # changes is a named list (old ingredient, new ingredient)
    for old_id, new_id in ingredient_replacements_dictionary.items():
        try:
            previous_ingredient = Ingredient.objects.get(id=old_id)
            current_ingredient = IngredientSubstitute.objects.get(id=new_id)
            changes.append((previous_ingredient.name,
                           current_ingredient.name))
        except (Ingredient.DoesNotExist, IngredientSubstitute.DoesNotExist):
            continue

    # get user's selected values from dropdown list
    if request.method == 'POST':
        recipe_id = request.POST.get('selected_recipe')
        location_id = request.POST.get('selected_location')
        timeofday_id = request.POST.get('selected_timeofday')

        # what happens if new recipe is picked
        if recipe_id:
            request.session['selected_recipe_id'] = recipe_id
            request.session['ingredient_replacements'] = {}
            ingredient_replacements_dictionary = {}
            total_ingredient_emissions_current = 0
            total_ingredient_emissions_previous = 0
            current_ingredients = []
            changes = []
            ingredient_percent_change = []

        if location_id:
            request.session['selected_location_id'] = location_id

        if timeofday_id:
            request.session['selected_timeofday_id'] = timeofday_id

    # store user selections
    if 'selected_recipe_id' in request.session:
        selected_recipe = get_object_or_404(
            Recipe, id=request.session['selected_recipe_id'])

    if 'selected_location_id' in request.session:
        selected_location = get_object_or_404(
            Location, id=request.session['selected_location_id'])

    if 'selected_timeofday_id' in request.session:
        selected_timeofday = get_object_or_404(
            Timeofday, id=request.session['selected_timeofday_id'])

    # store all previous ingredient emissions into a single vlaue
    if selected_recipe:
        for ingredient in selected_recipe.ingredients.all():
            try:
                total_ingredient_emissions_previous += float(
                    ingredient.emissions)
            except (ValueError, TypeError):
                continue
        if selected_timeofday:
            total_ingredient_emissions_previous += float(
                selected_timeofday.emission_multiplier)
        if selected_location:
            total_ingredient_emissions_previous += float(
                selected_location.location_emission_factor)

    if selected_recipe:
        recipe_steps = selected_recipe.recipe_steps.all()
        current_ingredients = list(selected_recipe.ingredients.all())
    else:
        recipe_steps = []
        current_ingredients = []

    # to display substitutions made
    for i, ingredient in enumerate(current_ingredients):
        replaced_id = ingredient_replacements_dictionary.get(
            str(ingredient.id))
        if replaced_id:
            try:
                old_ingredient = Ingredient.objects.get(id=ingredient.id)
                new_ingredient = IngredientSubstitute.objects.get(
                    id=replaced_id)

                if total_ingredient_emissions_previous > 0:
                    percent_change = (
                        (old_ingredient.emissions - new_ingredient.emissions) / total_ingredient_emissions_previous * 100)
                else:
                    percent_change = 0

                ingredient_percent_change.append(
                    (old_ingredient.name, new_ingredient.name, percent_change))

                current_ingredients[i] = new_ingredient
            except (Ingredient.DoesNotExist, IngredientSubstitute.DoesNotExist,):
                continue

    # calculate emissions from replacment ingredients
    if ingredient_replacements_dictionary:
        for ingredient in current_ingredients:
            try:
                total_ingredient_emissions_current += float(
                    ingredient.emissions)
                if selected_timeofday:
                    total_ingredient_emissions_current += float(
                        selected_timeofday.emission_multiplier)
                if selected_location:
                    total_ingredient_emissions_current += float(
                        selected_location.location_emission_factor)
            except (ValueError, TypeError):
                continue
    else:
        total_ingredient_emissions_current = total_ingredient_emissions_previous

    # if user makes all 3 drop drown slections, then calculate percentage
    if selected_recipe and selected_location and selected_timeofday:
        if total_ingredient_emissions_previous and total_ingredient_emissions_current > 0:
            percent_emissions_reduced = ((total_ingredient_emissions_previous -
                                          total_ingredient_emissions_current) / total_ingredient_emissions_previous * 100)
        else:
            percent_emissions_reduced = 0

    return render(request, 'index.html', {
        'recipes': recipes,
        'locations': locations,
        'timeofdays': timeofdays,
        'selected_recipe': selected_recipe,
        'selected_timeofday': selected_timeofday,
        'selected_location': selected_location,
        'recipe_steps': recipe_steps,
        'total_ingredient_emissions_current': total_ingredient_emissions_current,
        'total_ingredient_emissions_previous': total_ingredient_emissions_previous,
        'current_ingredients': current_ingredients,
        'changes': changes,
        'percent_emissions_reduced': percent_emissions_reduced,
        'ingredient_percent_change': ingredient_percent_change,
    },)
