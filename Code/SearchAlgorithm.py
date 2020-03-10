# This file contains all the required routines to make an A* search algorithm.
#
__authors__ = '1491858'
__group__ = 'DL.15'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Grau en Enginyeria Informatica
# Curs 2016- 2017
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    path_list = list()
    for station in map.connections[path.last]:
        aux = copy.deepcopy(path)
        aux.add_route(station)
        path_list.append(aux)
    return path_list
    pass


def remove_cycles(path_list):
    aux_path_list = copy.deepcopy(path_list)
    for path in aux_path_list:
        i = 0
        max = len(path.route)
        surt = False
        while surt == False and i < max:
            if path.route[i] in path.route[i+1:]:
                surt = True
                path_list.remove(path)
            i += 1
    return path_list
    pass


def insert_depth_first_search(expand_paths, list_of_path):
    return expand_paths + list_of_path
    pass

def depth_first_search(origin_id, destination_id, map):
    llista = [Path(origin_id)]
    i = 0
    while llista[0].route[-1] != destination_id and len(llista) != 0:
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        llista = insert_depth_first_search(E, llista)
    if (llista is None):
        return 'No hi ha solució'
    else:
        return llista[0]

    pass


def insert_breadth_first_search(expand_paths, list_of_path):
    return list_of_path + expand_paths
    pass


def breadth_first_search(origin_id, destination_id, map):
    llista = [Path(origin_id)]
    i = 0
    while llista[0].route[-1] != destination_id and len(llista) != 0:
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        llista = insert_breadth_first_search(E, llista)
    if (llista is None):
        return 'No hi ha solució'
    else:
        return llista[0]

    pass


def calculate_cost(expand_paths, map, type_preference):

    if type_preference == 0:
        for path in expand_paths:
            path.update_g(1)
    elif type_preference == 1:
        for path in expand_paths:
            path.update_g(map.connections[path.penultimate][path.last])
    elif type_preference == 2:
        for path in expand_paths:
            if(map.stations[path.penultimate]['name'] != map.stations[path.last]['name'] ):
                path.update_g(map.velocity[map.stations[path.penultimate]['line']] * map.connections[path.penultimate][path.last])
    elif type_preference == 3:
        for path in expand_paths:
            if map.stations[path.penultimate]['line'] != map.stations[path.last]['line']:
                path.update_g(1)

    return expand_paths
    pass


def insert_cost(expand_paths, list_of_path):
    for path in expand_paths:
        trobat = False
        index = 0
        if len(list_of_path) == 0:
            list_of_path.append(path)
        else:
            while index < len(list_of_path) and trobat == False:
                if path.g < list_of_path[index].g:
                    list_of_path.insert(index, path)
                    trobat = True
                index+=1
            if trobat == False:
                list_of_path.append(path)

    return list_of_path

    pass


def uniform_cost_search(origin_id, destination_id, map, type_preference):
    llista = [Path(origin_id)]
    i = 0
    while llista[0].route[-1] != destination_id and len(llista) != 0:
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        E = calculate_cost(E, map, type_preference)
        llista = insert_cost(E, llista)
    if (llista is None):
        return 'No hi ha solució'
    else:
        return llista[0]

    pass


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    pass



def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g in this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
    """
    pass


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    pass


def coord2station(coord, map):
    possible_origins = list()
    min = euclidean_dist(coord, [map.stations[1]['x'], map.stations[1]['y']])
    possible_origins = [1]
    max = len(map.stations)
    for index in range(2, max):
        min_aux = euclidean_dist(coord, [map.stations[index]['x'], map.stations[index]['y']])
        if min_aux < min:
            min = min_aux
            possible_origins = []
            possible_origins = [index]
        elif min_aux == min:
            possible_origins.append(index)
    return possible_origins
    pass


def Astar(origin_coor, dest_coor, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (list): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pass