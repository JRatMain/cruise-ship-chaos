import queue
import random as rand
from time import sleep

import tabulate

import assignment

rooms = []
assignments = []
a_deck_rooms = 20
b_deck_rooms = 100
c_deck_rooms = 200
d_deck_rooms = 500


# Picks a random surname based on a randomly generated number.
# As a failsafe, 'Myers' will return.
def pick_surname(name_gen):
    if name_gen == 0:
        return 'Coppola'
    elif name_gen == 1:
        return 'Smith'
    elif name_gen == 2:
        return 'Sanchez'
    elif name_gen == 3:
        return 'Cahill'
    elif name_gen == 4:
        return 'Kuso'
    elif name_gen == 5:
        return 'Reyes'
    else:
        return 'Myers'


# Selects a name for a female based on a randomly generated number.
# 'April' will return as a failsafe in the event of a bug
def pick_female_name():
    name_gen = rand.randint(0, 5)
    if name_gen == 0:
        return 'Summer'
    elif name_gen == 1:
        return 'Beth'
    elif name_gen == 2:
        return 'Jasmine'
    elif name_gen == 3:
        return 'Sarah'
    elif name_gen == 4:
        return 'Sabrina'
    elif name_gen == 5:
        return 'Zelda'
    else:
        return 'April'


# Selects a name for a male based on a randomly generated number.
# 'Jerry' will return in the event of an error as a failsafe
def pick_male_name():
    name_gen = rand.randint(0, 5)
    if name_gen == 0:
        return 'Jake'
    elif name_gen == 1:
        return 'Rick'
    elif name_gen == 2:
        return 'Jonathan'
    elif name_gen == 3:
        return 'Morty'
    elif name_gen == 4:
        return 'Frank'
    elif name_gen == 5:
        return 'Rydell'
    else:
        return 'Jerry'


def passenger_check(line):
    global a_deck_rooms, b_deck_rooms, \
        c_deck_rooms, d_deck_rooms
    gender_num = rand.randint(0, 1)
    surname_num = rand.randint(0, 5)
    pass_color = ''

    if gender_num == 0:
        first_name = pick_female_name()
    elif gender_num == 1:
        first_name = pick_male_name()
    else:
        raise RuntimeError("Invalid gender number.")
    surname = pick_surname(surname_num)

    while pass_color == '':
        pass_num = rand.randint(0, 3)
        if pass_num == 0 and a_deck_rooms > 0:
            pass_color = 'Green'
            a_deck_rooms -= 1
        if pass_num == 1 and b_deck_rooms > 0:
            pass_color = 'Blue'
            b_deck_rooms -= 1
        if pass_num == 2 and c_deck_rooms > 0:
            pass_color = 'Orange'
            c_deck_rooms -= 1
        if pass_num == 3 and d_deck_rooms > 0:
            pass_color = 'Red'
            d_deck_rooms -= 1

    print('Passenger Admitted.')
    print('==========================')

    new_passenger = [first_name, surname, gender_num, pass_color]
    line.put(new_passenger)
    print('Sleeping for 1 second...')
    print('==========================')
    sleep(1)


def create_rooms():
    global rooms
    for i in range(820):
        num = i + 1
        new_room = [num]
        rooms.append(new_room)


def assign_rooms(line):
    global rooms, assignments
    while not line.empty():
        data = line.get()
        first_name = data[0]
        last_name = data[1]
        pass_color = data[3]
        room = rooms.pop()
        room_number = room[0]
        new_assignment = assignment.assignment(first_name, last_name, room_number, pass_color)
        assignments.append(new_assignment)


# Unpacks data from the assignments objects and prints them using the tabulate module.
def print_assignments():
    global assignments
    assignment_list = []
    for i in range(len(assignments)):
        data = assignments[i]
        first_name = data.__getattribute__('first_name')
        last_name = data.__getattribute__('last_name')
        room_num = data.__getattribute__('room_num')
        pass_color = data.__getattribute__('pass_color')
        assignment_list.append([first_name, last_name, room_num, pass_color])
    print(tabulate.tabulate(assignment_list,
                            headers=['First Name', 'Last Name', 'Room Number', 'Pass Color']))


if __name__ == '__main__':
    passenger_line = queue.Queue(820)
    while not passenger_line.full():
        passenger_check(passenger_line)
    create_rooms()
    assign_rooms(passenger_line)
    print('Room assignments complete. Results will print in 5 seconds.')
    sleep(5)
    print_assignments()
