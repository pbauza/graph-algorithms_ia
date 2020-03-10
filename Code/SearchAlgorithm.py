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
    for path in reversed(path_list):
        """
        #SEMPRE nlog(n):
        if len(path.route) != len(set(path.route)):
            path_list.remove(path)
        """

        #ES SUPOSA QUE AQUESTA ES LA MES RAPIDA:
        setofElems = set()
        for elem in path.route:
            if elem in setofElems:
                path_list.remove(path)
                break
            else:
                setofElems.add(elem)

        """        
        #AQUESTA ES LA QUE FEIA FINS ARA
        i = 0
        max = len(path.route)
        surt = False
        while surt == False and i < max:
            if path.route[i] in path.route[i + 1:]:
                surt = True
                path_list.remove(path)
            i += 1
        """

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


def calculate_heuristics(expand_paths, map, destination_id, type_preference):
    if type_preference == 0:
        for path in expand_paths:
            if path.last != destination_id:
                path.update_h(1)
            else:
                path.update_h(0)
    elif type_preference == 1:
        max_velocity = max(map.velocity.values())
        for path in expand_paths:
            path.update_h(euclidean_dist([map.stations[path.last]['x'], map.stations[path.last]['y']], [map.stations[destination_id]['x'], map.stations[destination_id]['y']])/max_velocity)
    elif type_preference == 2:
        for path in expand_paths:
            path.update_h(euclidean_dist([map.stations[path.last]['x'], map.stations[path.last]['y']], [map.stations[destination_id]['x'], map.stations[destination_id]['y']]))
    elif type_preference == 3:
        for path in expand_paths:
            if map.stations[path.last]['line'] != map.stations[destination_id]['line']:
                path.update_h(1)
            else:
                path.update_h(0)

    return expand_paths
    pass

    pass



def update_f(expand_paths):

    for path in expand_paths:
        path.update_f()
    return expand_paths
    pass


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):

    for path in reversed(expand_paths):
        if path.last in visited_stations_cost.keys():
            if path.g < visited_stations_cost[path.last]:
                visited_stations_cost[path.last] = path.g
                for path1 in reversed(list_of_path):
                    if path1.last == path.last:
                        list_of_path.remove(path1)
            else:
                expand_paths.remove(path)

    return expand_paths, list_of_path, visited_stations_cost
    pass


def insert_cost_f(expand_paths, list_of_path):

    for path in expand_paths:
        trobat = False
        index = 0
        if len(list_of_path) == 0:
            list_of_path.append(path)
        else:
            while index < len(list_of_path) and trobat == False:
                if path.f < list_of_path[index].f:
                    list_of_path.insert(index, path)
                    trobat = True
                index+=1
            if trobat == False:
                list_of_path.append(path)

    return list_of_path
    pass


def coord2station(coord, map):
    possible_origins = list()
    min = euclidean_dist(coord, [map.stations[1]['x'], map.stations[1]['y']])
    possible_origins = [1]
    max = len(map.stations)+1
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


def Astar(origin_coor, dest_coor, map, type_preference):

    origin_list = coord2station(origin_coor, map)
    destination_list = coord2station(dest_coor, map)
    origin_id = origin_list[0]
    destination_id = destination_list[0]

    llista = [Path(origin_id)]
    visited_station_cost = {origin_id: 0}
    i = 0

    #print(origin_list)
    #print(destination_list)
    while llista[0].route[-1] != destination_id and len(llista) != 0:
        C = llista.pop(0)
        E = expand(C, map)
        E = remove_cycles(E)
        E = calculate_cost(E, map, type_preference)
        E, llista, visited_station_cost = remove_redundant_paths(E, llista, visited_station_cost)
        E = calculate_heuristics(E, map, destination_id, type_preference)
        E = update_f(E)
        llista = insert_cost_f(E, llista)
        for path in E:
            if path.last in visited_station_cost.keys():
                if visited_station_cost[path.last] < path.g:
                    visited_station_cost[path.last] = path.g
            else:
                visited_station_cost[path.last] = path.g


    if (llista is None):
        return 'No hi ha solució'
    else:
        #print(llista[0].route)
        #print(llista[0].f)
        return llista[0]

    pass
    pass