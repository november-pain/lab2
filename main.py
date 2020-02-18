import folium
from geopy.extra.rate_limiter import RateLimiter
from geopy.geocoders import Nominatim

geolocator = Nominatim(timeout=100)
geocode = RateLimiter(geolocator.geocode, error_wait_seconds=0.5,
                      max_retries=0, swallow_exceptions=False, return_value_on_exception=True)


def read_file(path):
    """
    reads file and makes a dict with title as key and year and location as a value
    :param path: str
    :return: dct
    """
    film_dct = {}
    s = 1000
    with open(path, encoding='utf-8', errors='ignore') as f:
        for m, line in enumerate(f):
            if line.startswith('"'):
                title = ""
                i = 0
                for char in line[1:]:
                    title += char
                    i += 1
                    if char == '"':
                        break
                title = title[:-2]
                film_dct[title] = []
                year = ''
                for char in line[i:]:
                    i += 1
                    if char == '(':
                        year += line[i:i + 4]
                        i += 5
                        break

                film_dct[title].append(year)

                location = line[i:].split('}')[-1].split("(")[0].strip('\t').replace('\n', '')
                film_dct[title].append(location)

                if m == s:
                    break
    return film_dct


def movie_mark(year, film_dict, map):
    """
    makes a mark on map
    :param year:
    :param film_dict:
    :return: None
    """
    films_layer = folium.FeatureGroup(name="films of {} year".format(str(year)))
    films_of_year = list(filter(lambda x: x[1][0] == year, film_dict.items()))
    for film in films_of_year:
        location = geolocator.geocode(film[1])

        if location is None:
            pass
        else:
            films_layer.add_child(folium.Marker(location=[location.latitude, location.longitude],
                                                popup=film[0]))
    map.add_child(films_layer)


if __name__ == '__main__':
    map = folium.Map()
    year = input("Please enter a year you would like to have a map for:")
    print(movie_mark(year, read_file("locations.list"), map))
    map.add_child(folium.LayerControl())
    map.save('Map.html')
