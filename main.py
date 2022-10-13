import random

from tabulate import tabulate
import mysql.connector
from geopy import distance

testDB = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='flight_game',
    user='root',
    password='',
    autocommit=True
)

my_cursor = testDB.cursor()


#
name_of_player = input("Hi! Welcome to the Moomin's Travelling game! Please enter your name: ")
print(f"Hi, {name_of_player}! Happy to see you! Let me tell you more about the rules of the game. \n"
      f"Moomin's girlfriend Snorkmaiden is in Ivalo and you are in Helsinki.\n"
      f"Your task is to fly to Ivalo via the shortest route. Your ticket has 3 connecting flights.\n"
      f"Choose 3 airports to transit which will make your flight distance as short as possible. Goof luck!")
def calculate_distance(icao_1, icao_2):
    my_cursor.execute(f"select name from airport where ident = '{icao_1}';")
    name1 = my_cursor.fetchall()
    name1 = tabulate(name1, tablefmt="fancy_grid")
    my_cursor.execute(f"select name from airport where ident = '{icao_2}';")
    name2 = my_cursor.fetchall()
    name2 = tabulate(name2, tablefmt="fancy_grid")
    my_cursor.execute(
        f"select latitude_deg, longitude_deg from airport where ident = '{icao_1}' or ident = '{icao_2}';")
    list_deg = []
    for x in my_cursor:
        list_deg.append(x)
    return name1, name2, distance.distance(list_deg[0], list_deg[1]).km



player1_total_distance = 0
player1_airports = []
player2_total_distance = 0
player2_airports = []
# 1
A = "EFHK"
for x in range(0, 3):
    B = input("Now you can choose 1st airport to transit. Please type in ICAO of the airport: ")
    result = calculate_distance(A, B)
    player1_airports.append(result[0])
    player1_total_distance += result[2]
    print(f"You travelled from\n{result[0]} \nto\n{result[1]}")
    A = B

result = calculate_distance(B, "EFIV")
player1_airports.append(result[0])
player1_airports.append(result[1])
player1_total_distance += result[2]
print("All the airports you travelled:")
for airport in player1_airports:
    print(airport)

# 2
A = "EFHK"
name_of_second_player = input("Second player, please enter your name: ")
print(f"Hi, {name_of_second_player}! Welcome onboard!")
for x in range(0, 3):
    B = input(f"{name_of_second_player}, choose an airport to transit: ")
    result = calculate_distance(A, B)
    player2_airports.append(result[0])
    player2_total_distance += result[2]
    print(f"You travelled from\n{result[0]} \nto\n{result[1]}")
    A = B

result = calculate_distance(B, "EFIV")
player2_airports.append(result[0])
player2_airports.append(result[1])
player2_total_distance += result[2]

print("All the airports you travelled:")
for airport in player2_airports:
    print(airport)

print(f"{name_of_player}went a total of {player1_total_distance:.2f}km to find Snorkmaiden")
print(f"{name_of_second_player} went a total of {player2_total_distance:.2f}km to find Snorkmaiden")
if player1_total_distance < player2_total_distance:
    print(f"{name_of_player} is Moomin!\n{name_of_second_player} lost the game;(")
else:
    print(f"{name_of_player} lost the game ;(\n{name_of_second_player} is Moomin!")
