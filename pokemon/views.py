from django.shortcuts import render
from .models import Pokedex
import requests


def pokemon_crawler():
    pokemon_id = 1
    while pokemon_id >= 1:
        ability_names = ""
        poke_stats = ""
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}/")
        if response.status_code == 404:
            break
        else:
            name = response.json()["name"]

            abilities = response.json()["abilities"]
            for ability in abilities:
                ability_names += ability["ability"]["name"] + "\n"

            stats = response.json()["stats"]
            for stat in stats:
                stat_base = stat["base_stat"]
                stat_name = stat["stat"]["name"]
                poke_stats += stat_name + ": " + str(stat_base) + "\n"

            sprite = response.json()["sprites"]["front_default"]
            if Pokedex.objects.filter(name__contains=name):
                Pokedex.objects.filter(name__contains=name).update(abilities=ability_names, stats=poke_stats, sprite=sprite)
            else:
                Pokedex.objects.create(name=name, abilities=ability_names, stats=poke_stats, sprite=sprite)
            pokemon_id += 1


def home(request):
    if request.GET.get('Update Database') == 'Update Database':
        pokemon_crawler()
    return render(request, 'home.html', {})


def pokemon(request):
    if request.method == "POST":
        searched = request.POST["searched"].lower()
        if Pokedex.objects.filter(name=searched):
            pokedex = Pokedex.objects.get(name=searched)
            abilities = pokedex.abilities.rsplit("\n")
            abilities.pop()
            stats = pokedex.stats.rsplit("\n")
            stats.pop()
            return render(request, 'pokemon.html', {"pokedex": pokedex,
                                                    "abilities": abilities,
                                                    "stats": stats})
        else:
            not_valid = "Not a valid Pokemon!"
            return render(request, 'pokemon.html', {"not_valid": not_valid})
