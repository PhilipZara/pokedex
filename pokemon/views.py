from django.shortcuts import render
from .models import Pokedex
import requests
from django.contrib import messages


def pokemon_crawler():
    # The link below is the one that the API suggests of using to get all Pokemons.
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon?limit=100000&offset=0").json()
    pokemons = response["results"]
    for poke in pokemons:
        response = requests.get(poke["url"])
        if response.status_code == 404:
            continue
        else:
            name = response.json()["name"]

            abilities = response.json()["abilities"]

            stats = response.json()["stats"]

            sprite = response.json()["sprites"]["front_default"]

            ability_names = [ability["ability"]["name"] for ability in abilities]

            poke_stats = [stat["stat"]["name"] + ": " + str(stat["base_stat"]) for stat in stats]

            if Pokedex.objects.filter(name=name):
                Pokedex.objects.filter(name=name).update(abilities=ability_names, stats=poke_stats, sprite=sprite)
            else:
                if name or ability_names or poke_stats or sprite is None:
                    continue
                else:
                    Pokedex.objects.create(name=name, abilities=ability_names, stats=poke_stats, sprite=sprite)


def home(request):
    pokemons = Pokedex.objects.all()
    if request.GET.get('Update Database') == 'Update Database':
        pokemon_crawler()
        messages.success(request, "Your database has been updated!")
    return render(request, 'home.html', {'pokemons': pokemons})


def pokemon(request):
    if request.method == "POST":
        searched = request.POST["searched"].lower()
        if Pokedex.objects.filter(name=searched):
            pokedex = Pokedex.objects.get(name=searched)
            abilities = pokedex.abilities
            stats = pokedex.stats
            return render(request, 'pokemon.html', {"pokedex": pokedex,
                                                    "abilities": abilities,
                                                    "stats": stats})
        else:
            not_valid = "Not a valid Pokemon!"
            return render(request, 'pokemon.html', {"not_valid": not_valid})
