from asyncio.windows_events import NULL
from locale import currency
from random import randint
from sqlite3 import connect
from sys import maxsize
from math import sqrt
from itertools import permutations

from cv2 import connectedComponents
from numpy import allclose, nonzero

class City:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.edges = []
        self.visited = False
        self.ID = id
        self.connectedTo = []

#Funckja zwracająca listę howMany miast o współrzędnych wylosowanych z zakresu od 0 do maxX i maxY
def generateCities(howMany, maxX, maxY):
    cities = []
    for i in range(howMany):
        cities.append(City(randint(0, maxX), randint(0,maxY), i))
    return cities

#Funkcja zwracająca odległość euklidesową pomiędzy dwoma maistami
def distance(x1, y1, x2, y2):
    return sqrt( (x2-x1)**2 + (y2-y1)**2 )

#Funckja zwraca listę długości krawędzi pomiędzy miastami
def calculateEdges(cities):
    for current_city in cities:
        for city in cities:
            city.edges.append(distance(current_city.x, current_city.y, city.x, city.y))

def unVisit(cities):
    for city in cities:
        city.visited = False

def TSP_bruteforce(cities, start):
    edges = [] #Lista kosztów dróg dla każdego miasta
    for city in cities:
        edges.append(city.edges) #Ekstraktuję koszty dróg z obiektu
    vertices = []

    for edge in range(len(edges)): #Dodaję wszystkie miasta jako liczby do listy vertices
        if edge != start:
            vertices.append(edge)
    
    minimal_path = maxsize
    all_permutations = permutations(vertices) #Tworzę permutację wszystkich miast
    for permutation in all_permutations:
        current_pathWeight = 0
        
        #Liczę koszt przebycia drogi w danej permutacji
        i = start
        for vertex in permutation:
            current_pathWeight += edges[i][vertex]
            i = vertex
        current_pathWeight += edges[i][start]
        minimal_path = min(minimal_path, current_pathWeight) #Sprawdzam czy wartość przebycia drogi w tej permutacji jest mniejsza od minimalnej
    return minimal_path

def min_no_zero(list, exclusions = []):
    min = maxsize
    minIndex = 0
    for index, element in enumerate(list):
        if element > 0 and element < min and element not in exclusions:
            min = element
            minIndex = index
    return minIndex, min

def all_visited(cities):
    for city in cities:
        if not city.visited:
            return False
    return True

def TSP_NN(cities, start):
    path = 0
    current_city = cities[start] #Oznaczam jako aktualne miasto to startowe
    current_city.visited = True #Oznaczam je jako odwiedzone
    while(not all_visited(cities)):
        found = False
        excluded = []
        while not found: #Szukam najkrótszej drogi do następnego nieodwiedzonego miasta
            res = min_no_zero(current_city.edges, excluded)
            if cities[res[0]].visited:
                excluded.append(res[1])
            else:
                found = True
                path += res[1] #Dodaję do drogi całkowitej
                current_city = cities[res[0]] #Przechodzę do następnego miasta
                current_city.visited = True #Oznaczam je jako odwiedzone
    path += current_city.edges[start] #Dodaję koszt drogi powrotu do miasta startowego
    unVisit(cities)
    return path

def TSP_NI(cities, start): #Nearest Insertion Alghoritm 
    
    connected_cities = []
    path_weight = 0.0
    connected_cities.append(cities[start]) #Do połączonych miast dodaję miasto startowe
    cities[start].visited = True #Oznaczam miasto startowe jako odwiedzone
    res = min_no_zero(cities[start].edges) #Znajduje najbliższe miasto do startowego
    cities[res[0]].visited = True #Oznaczam je jako odwiedzone
    path_weight += res[1] #Dodaje drogę pomiędzy nimi do drogi całkowitej
    connected_cities.append(cities[res[0]]) #Dodaje drugie miasto do miast połączonych
    connected_cities[0].connectedTo.append(connected_cities[1]) #Wskazuję że miasto startowe jest połączone z miastem drugim w polu obiektu miasta startowego
    connected_cities[1].connectedTo.append(connected_cities[0]) #Analogicznie jak wyżej
    
    #Znajduję trzecie miasto najbliższe do któregokolwiek z miast połączonych
    min = maxsize
    minID = 0
    closest_city = connected_cities[0]
    for city in connected_cities:
            res = min_no_zero(city.edges)
            if res[1] < min:
                min = res[1]
                minID = res[0]
                closest_city = city
    
    #Trzecie najbliższe miasto łączę z dwoma pozostałymi
    current_city = cities[minID]
    path_weight += min #Dodaję drogę pomiędzy miastem najbliższym do trzeciego miasta
    path_weight += closest_city.connectedTo[0].edges[minID] #Dodaje drogę pomiędzy trzecim miastem a dalszym miastem 
    for city in connected_cities:
        city.connectedTo.append(current_city) #Do miasta 1 i 2 dodaję informację o połączeniu z miastem 3
    connected_cities.append(current_city) #Dodaję trzecie miasto do miast połączonych
    
    current_city.visited = True 
    current_city.connectedTo.append(connected_cities[0]) #Do 3 miasta dodaje informację o połączeniu z miastem 1 i 2
    current_city.connectedTo.append(connected_cities[1])
    
    while(not all_visited(cities)):
        min = maxsize
        minID = 0
        closest_city_ID = 0
        found = False
        excluded = []
        #Odnajduję nieodwiedzone miasto które jest najbliżej jednego z odwiedzonych miast
        while not found:
            for city in connected_cities:
                min = maxsize
                res = min_no_zero(city.edges, excluded)
                if res[1] < min:
                    min = res[1]
                    minID = res[0]
                    closest_city_ID = city.ID
            if cities[minID].visited:
                excluded.append(min)
            else: found = True 
        closest_city = cities[closest_city_ID]
        #Sprawdzam czy miasto po lewej czy po prawej miasta najbliższego jest najbliżej dołączanego miasta
        min = closest_city.connectedTo[0].edges[minID]
        second_closest_city = closest_city.connectedTo[0]
        if closest_city.connectedTo[1].edges[minID] < min:
            second_closest_city = closest_city.connectedTo[1]
        #Odejmuję drogę pomiędzy parą miast rozłączanych i wstawiam koszt dróg utworzonych pomiędzy miastem wstawianym a parą miast
        path_weight -= closest_city.edges[second_closest_city.ID]
        path_weight += closest_city.edges[minID]
        path_weight += second_closest_city.edges[minID]
        
        current_city = cities[minID]
        #Usuwam z pary miast informację o połączeniu między nimi i dodaję informacje o połączeniu z nowym miastem
        closest_city.connectedTo.remove(second_closest_city)
        closest_city.connectedTo.append(current_city)

        second_closest_city.connectedTo.remove(closest_city)
        second_closest_city.connectedTo.append(current_city)

        #Dodaje nowe miasto do listy maist połączonych i dodaję do niego informację z jakimi miastami jest połączone
        connected_cities.append(current_city)
        current_city.visited = True
        current_city.connectedTo.append(closest_city)
        current_city.connectedTo.append(second_closest_city)
    unVisit(cities)
    return path_weight



if __name__ == "__main__":
    print("Ze względu na długie obliczenia wartość dla algorytmu Bruteforce jest wyświetlana tylko dla liczby miast poniżej 11")
    all_correct = False
    while not all_correct:
        try:
            n = int(input("Ile miast wygenerować?: "))
            if n < 4:
                print("Conajmniej 4 miasta")
                continue
            maxX = int(input("Maksymalna wartość x: "))
            maxY = int(input("Maksymalna wartość y: "))
            if maxX <= 0 or maxY <= 0:
                print("Wartosc x oraz y musi być większa od 0 i musi być liczbą całkowitą")
                continue
            all_correct = True
        except ValueError:
            print("Tylko liczby całkowite")
        except:
            exit()
            
    cities = generateCities(n, maxX, maxY)
    calculateEdges(cities)
    if n <= 10:
        min_path = TSP_bruteforce(cities, 0)
    min_path2 = TSP_NN(cities, 0)
    min_path3 = TSP_NI(cities, 0)
    if n <= 10:
        print("BF: " + str(round(min_path, 2)))
    print("NN: " + str(round(min_path2, 2)))
    print("NI: " + str(round(min_path3, 2)))

    ## Kod do wygenerowania wartości do sprawozdania
    # print("Max x and max y = 50")
    # print("-------------------------------")
    # for i in range(4,9):
    #     print("Number of cities: ", i)
    #     cities = generateCities(i, 50, 50)
    #     calculateEdges(cities)
    #     min_path = TSP_bruteforce(cities, 0)
    #     min_path2 = TSP_NN(cities, 0)
    #     min_path3 = TSP_NI(cities, 0)
    #     print("BF: " + str(round(min_path, 2)))
    #     print("NN: " + str(round(min_path2, 2)))
    #     print("NI: " + str(round(min_path3, 2)))
    #     print("-------------------------------")