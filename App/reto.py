"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad de Los Andes
 * 
 * Contribución de:
 *
 * Cristian Camilo Castellanos
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 """

"""
  Este módulo es una aplicación básica con un menú de opciones para cargar datos, contar elementos,
   y hacer búsquedas sobre una lista .
"""

import config as cf
import sys
import csv
from ADT import list as lt
from DataStructures import listiterator as it
from DataStructures import liststructure as lt
from Sorting import shellsort as shell
from Sorting import selectionsort as selection
from Sorting import insertionsort as insertion
from time import process_time


def print_menu():
    """
    Imprime el menu de opciones
    """
    print('\nBienvenido')
    print('1- Cargar Datos')
    print('2- Contar las películas de la Lista')
    print('3- Contar películas de un director')
    print('4- Consultar buenas películas de un director')
    print('5- Ordenar películas por votos')
    print('6- Conocer a un director y todas sus películas')
    print('7- Ranking de un género cinematográfico')
    print('0- Salir')


def load_csv_file(file_d, file_c, sep=';'):
    """
    Carga un archivo csv a una lista
    Args:
        file_d
            Archivo de texto del cual se cargaran los detalles de las películas.
        file_c
            Archivo de texto del cual se cargaran los castings de las películas.
        sep :: str
            Separadores código para diferenciar a los distintos elementos dentro del archivo.
    Try:
        Intenta cargar el archivo CSV a la lista que se le pasa por parametro, si encuentra algun error
        Borra la lista e informa al usuario
    Returns: None
    """
    # lst_d, lst_c = lt.newList('ARRAY_LIST'), lt.newList('ARRAY_LIST')  # Usando implementacion arraylist
    lst_d, lst_c = lt.newList('SINGLE_LINKED'), lt.newList('SINGLE_LINKED')  # Usando implementacion linkedlist
    print('Cargando archivos...')
    t1_start = process_time()  # Start time
    dialect, dialect.delimiter = csv.excel(), sep
    try:
        with open(file_d, encoding='utf-8-sig') as csvfile_d, open(file_c, encoding='utf-8-sig') as csvfile_c:
            spamreader_d, spamreader_c = (csv.DictReader(csvfile_d, dialect=dialect),
                                          csv.DictReader(csvfile_c, dialect=dialect))
            for row_d, row_c in zip(spamreader_d, spamreader_c):
                lt.addLast(lst_d, row_d)
                lt.addLast(lst_c, row_c)
    except:
        lst_d, lst_c = lt.newList('ARRAY_LIST'), lt.newList('ARRAY_LIST')
        print('Se presentó un error en la carga de los archivos')
    t1_stop = process_time()  # Final time
    print('Tiempo de ejecución ', t1_stop - t1_start, ' segundos')
    return lst_d, lst_c


def count_director_movies(director, column, lst):
    """
    Retorna cuantos elementos coinciden con un criterio para una columna dada
    Args:
        director:: str
            Critero sobre el cual se va a contar la cantidad de apariciones
        column
            Columna del arreglo sobre la cual se debe realizar el conteo
        lst
            Lista en la cual se realizará el conteo, debe estar inicializada
    Return:
        counter :: int
            la cantidad de veces ue aparece un elemento con el criterio definido
    """
    if lst['size'] == 0:
        print('La lista esta vacía')
        return 0
    else:
        t1_start = process_time()  # Start time.
        counter = 0
        iterator = it.newIterator(lst)
        while it.hasNext(iterator):
            element = it.next(iterator)
            if director.lower() in element[column].lower():  # filtrar por palabra clave
                counter += 1
        t1_stop = process_time()  # Final time.
        print('Tiempo de ejecución ', t1_stop - t1_start, ' segundos')
    return counter


def get_director_movie_ids(search, result, director):
    iterator = it.newIterator(search)
    while it.hasNext(iterator):
        element = it.next(iterator)
        if director.lower() in element['director_name'].lower():  # filtrar por nombre
            lt.addLast(result, element['id'])


def movies_total_average(movies):
    iterator = it.newIterator(movies)
    votes_sum = 0
    while it.hasNext(iterator):
        element = it.next(iterator)
        votes_sum += float(element['vote_average'])
    total_vote_average = votes_sum / movies['size']
    return round(total_vote_average, 1)


def find_good_movies(director, vote_average, lst_d, lst_c):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    if len(lst_d) == 0:
        print('Las listas están vacías')
        return 0, 0
    else:
        t1_start = process_time()  # Start time.
        all_director_movies, good_movies = (lt.newList('ARRAY_LIST') for _ in range(2))
        # Search all director movie ids and add them to a list.
        get_director_movie_ids(lst_c, all_director_movies, director)
        # Search good movies and add vote points to list.
        iterator_ids = it.newIterator(all_director_movies)
        while it.hasNext(iterator_ids):
            movie_id = it.next(iterator_ids)
            iterator_movies = it.newIterator(lst_d)
            while it.hasNext(iterator_movies):
                movie = it.next(iterator_movies)
                if movie_id == movie['id']:
                    actual_vote = float(movie['vote_average'])
                    if actual_vote >= vote_average:
                        lt.addLast(good_movies, movie)
        show_movies(good_movies, director)
        # Calculate number of good movies and total vote average of director.
        total_vote_average = movies_total_average(good_movies)
        t1_stop = process_time()  # Final time.
        print('Tiempo de ejecución ', t1_stop - t1_start, ' segundos')
    return good_movies['size'], total_vote_average


def know_director(director, lst_d, lst_c):
    """
    Retorna la cantidad de elementos que cumplen con un criterio para una columna dada
    """
    if len(lst_d) == 0:
        print('Las listas están vacías')
        return 0, 0
    else:
        t1_start = process_time()  # Start time.
        all_director_movies, movies_data = (lt.newList('ARRAY_LIST') for _ in range(2))
        # Search all director movie ids and add them to a list.
        get_director_movie_ids(lst_c, all_director_movies, director)
        # Search movies and add vote points to list.
        iterator_ids = it.newIterator(all_director_movies)
        while it.hasNext(iterator_ids):
            movie_id = it.next(iterator_ids)
            iterator_movies = it.newIterator(lst_d)
            while it.hasNext(iterator_movies):
                movie = it.next(iterator_movies)
                if movie_id == movie['id']:
                    lt.addLast(movies_data, movie)
        show_movies(movies_data, director)
        # Calculate number of movies and total vote average of director.
        total_vote_average = movies_total_average(movies_data)
        t1_stop = process_time()  # Final time.
        print('Tiempo de ejecución ', t1_stop - t1_start, ' segundos')
    return movies_data['size'], total_vote_average


def show_movies(movies, director):
    if director is not None:
        print('Las películas dirigidas por', director, 'son:')
        iterator = it.newIterator(movies)
        while it.hasNext(iterator):
            element = it.next(iterator)
            print('-', element['title'])
    else:
        iterator = it.newIterator(movies)
        while it.hasNext(iterator):
            element = it.next(iterator)
            print('-', element['title'] + ':',
                  '\n   con un puntaje promedio de', element['vote_average'],
                  'y un total de', element['vote_count'], 'votaciones')


def less_average(element1, element2):
    if float(element1['vote_average']) < float(element2['vote_average']):
        return True
    return False


def greater_average(element1, element2):
    if float(element1['vote_average']) > float(element2['vote_average']):
        return True
    return False


def less_count(element1, element2):
    if float(element1['vote_count']) < float(element2['vote_count']):
        return True
    return False


def greater_count(element1, element2):
    if float(element1['vote_count']) > float(element2['vote_count']):
        return True
    return False


def sort_movies(algorithm, function, lst_d, column):
    if algorithm == 'selection':
        if function == 'less':
            selection.selectionSort(lst_d, less_count) if column == 'vote_count' \
                else selection.selectionSort(lst_d, less_average)
        elif function == 'greater':
            selection.selectionSort(lst_d, greater_count) if column == 'vote_count' \
                else selection.selectionSort(lst_d, greater_average)
    elif algorithm == 'shell':
        if function == 'less':
            shell.shellSort(lst_d, less_count) if column == 'vote_count' \
                else shell.shellSort(lst_d, less_average)
        elif function == 'greater':
            shell.shellSort(lst_d, greater_count) if column == 'vote_count' \
                else shell.shellSort(lst_d, greater_average)
    elif algorithm == 'insertion':
        if function == 'less':
            insertion.insertionSort(lst_d, less_count) if column == 'vote_count' \
                else insertion.insertionSort(lst_d, less_average)
        elif function == 'greater':
            insertion.insertionSort(lst_d, greater_count) if column == 'vote_count' \
                else insertion.insertionSort(lst_d, greater_average)


def rank_movies(function, lst_d, req_elements, algorithm, column):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    if len(lst_d) == 0:
        print('Las listas están vacías')
    else:
        t1_start = process_time()  # Start time.
        sort_movies(algorithm, function, lst_d, column)
        t1_stop = process_time()  # Final time.
        print(req_elements, 'best' if function == 'greater' else 'worst',
              'count:' if column == 'vote_count' else 'average:')
        show_movies(lt.subList(lst_d, 0, int(req_elements)), None)
        print(get_average_count_points(lt.subList(lst_d, 0, int(req_elements))))
        print('Tiempo de ejecución ', t1_stop - t1_start, ' segundos')


def create_list_by_genres(lst_d, genres):
    iterator_movies = it.newIterator(lst_d)
    genres_movies = lt.newList('ARRAY_LIST')
    for genre in genres:
        while it.hasNext(iterator_movies):
            movie = it.next(iterator_movies)
            if genre.lower() in movie['genres'].lower():
                lt.addLast(genres_movies, movie)
    return genres_movies


def get_average_count_points(movies):
    iterator_movies, total_average, total_count = it.newIterator(movies), 0, 0
    while it.hasNext(iterator_movies):
        movie = it.next(iterator_movies)
        total_average += float(movie['vote_average'])
        total_count += float(movie['vote_count'])
    total_average /= lt.size(movies)
    total_count /= lt.size(movies)
    return f'\nVotaciones promedio del ranking: {total_count:.1f}\nPuntaje promedio del ranking: {total_average:.1f}\n'


def rank_movies_on_genres(function, lst_d, req_elements, algorithm, column, genres):
    """
    Retorna una lista con cierta cantidad de elementos ordenados por el criterio
    """
    if len(lst_d) == 0:
        print('Las listas están vacías')
    else:
        t1_start = process_time()  # Start time.
        filtered = create_list_by_genres(lst_d, genres)
        sort_movies(algorithm, function, filtered, column)
        t1_stop = process_time()  # Final time.
        print(req_elements, 'best' if function == 'greater' else 'worst',
              'count:' if column == 'vote_count' else 'average:')
        show_movies(lt.subList(filtered, 0, int(req_elements)), None)
        print(get_average_count_points(lt.subList(filtered, 0, int(req_elements))))
        print('Tiempo de ejecución ', t1_stop - t1_start, ' segundos')


def search_genres(lst_d):
    genres = input('Ingrese el género a rankear. Si son varios, separe por comas: ')
    genres = genres.replace(' ', '')
    genres = genres.split(',')
    found = False
    iterator_movies = it.newIterator(lst_d)
    for genre in genres:
        while it.hasNext(iterator_movies):
            movie = it.next(iterator_movies)
            if genre.lower() in movie['genres'].lower():
                found = True
                break
            else:
                found = False
    if found:
        return genres
    else:
        print('Un género no se encuentra. Intente de nuevo.')
        return search_genres(lst_d)


def get_type_of_sorting():
    algorithm = input('\nIngrese 1 para ordenar con selection sorting\n'
                      'o 2 para ordenar con shell sorting\n'
                      'o 3 para ordenar con insertion sorting: ')
    if algorithm == '1':
        return 'selection'
    elif algorithm == '2':
        return 'shell'
    elif algorithm == '3':
        return 'insertion'


def get_vote_criteria():
    column = input('\nIngrese 1 para ordenar por cantidad de votos\n'
                   'o 2 para ordenar por calificación promedio: ')
    if column == '1':
        return 'vote_count'
    elif column == '2':
        return 'vote_average'


def get_sorting_direction():
    function = input('\nIngrese 1 para orden descendente\no 2 para ascendente: ')
    if function == '1':
        return 'greater'
    elif function == '2':
        return 'less'


def get_required_movies():
    req = input('Ingrese el número de películas requeridas en el ranking: ')
    while int(req) < 10:
        req = input('Ingrese por lo menos 10 películas requeridas: ')
    return req


def main():
    """
    Método principal del programa, se encarga de manejar todos los metodos adicionales creados

    Instancia una lista vacia en la cual se guardarán los datos cargados desde el archivo
    Args: None
    Return: None
    """
    details_list = lt.newList('ARRAY_LIST')
    while True:
        print_menu()  # imprimir el menu de opciones en consola
        inputs = input('Seleccione una opción para continuar:\n')  # leer opción ingresada
        if len(inputs) > 0:
            if int(inputs[0]) == 1:  # opcion 1
                details_list, casting_list = load_csv_file('../Data/MoviesDetailsCleaned-small.csv',
                                                           '../Data/MoviesCastingRaw-small.csv')  # Cargar datos
                if len(details_list) == len(casting_list):
                    print('Datos cargados, ' + str(details_list['size']) + ' elementos cargados en listas')
                else:
                    print('Datos cargados, aunque inconsistentes')
            elif int(inputs[0]) == 2:  # opcion 2
                if details_list['size'] == 0:  # obtener la longitud de la lista
                    print('La lista esta vacía')
                else:
                    print('La lista tiene ' + str(details_list['size']) + ' elementos')
            elif int(inputs[0]) == 3:  # opcion 3
                director = input('Ingrese un director para consultar su cantidad de películas:\n')  # filtrar columna
                counter_movies = count_director_movies(director, 'director_name', casting_list)
                print('Coinciden', counter_movies, 'elementos con el director', director)
            elif int(inputs[0]) == 4:  # opcion 4
                director = input('Ingrese el nombre del director para conocer sus buenas películas:\n')
                counter, average = find_good_movies(director, 6, details_list, casting_list)
                print('Existen', counter, 'buenas películas del director', director, 'en el catálogo')
                print('Las buenas películas de este director tienen un promedio de votación de', average, 'puntos.')
            elif int(inputs[0]) == 5:  # opcion 5
                print('Ranking de películas')
                req = get_required_movies()
                function = get_sorting_direction()  # Sorting direction.
                column = get_vote_criteria()  # Column criteria for sorting.
                algorithm = get_type_of_sorting()  # Type of sorting.
                rank_movies(function, details_list, req, algorithm, column)  # Show results.
            elif int(inputs[0]) == 6:  # opcion 6
                director = input('Ingrese el nombre del director para conocer su trabajo:\n')
                counter, average = know_director(director, details_list, casting_list)
                print('Existen', counter, 'películas del director', director, 'en el catálogo')
                print('Las películas de este director tienen un promedio de votación de', average, 'puntos.')
            elif int(inputs[0]) == 7:  # opcion 7
                print('Ranking de películas en un género')
                req = get_required_movies()
                genres = search_genres(details_list)  # genres name to search.
                column = get_vote_criteria()  # Column criteria for sorting.
                function = get_sorting_direction()  # Sorting direction.
                algorithm = get_type_of_sorting()  # Type of sorting.
                rank_movies_on_genres(function, details_list, req, algorithm, column, genres)  # Show results.
            elif int(inputs[0]) == 0:  # opcion 0, salir
                sys.exit(0)


if __name__ == '__main__':
    main()
