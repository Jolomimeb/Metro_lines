"""
File:    metro_lines.py
Author:  Oritsejolomisan Mebaghanje
Date:    4/30/2022
Section: 11
E-mail:  xz94254@umbc.edu
Description:
  This program creates a trip plaanner which tells the user how to get from one station to another.
  
"""

def plan_trip(locations, current, end_locations, visited):
    if current == end_locations:
        return [end_locations]

    visited.append(current)

    for new_place in locations[current]:
        if new_place not in visited:
            trip_plan = plan_trip(locations, new_place, end_locations, visited)
            if trip_plan:
                return [current] + trip_plan

    return []


def play_game():
    user_input = input('>>> ')
    locations = {}
    my_dict = {}
    train_dict = {}

    new_user_input = input(f'[{user_input}] >>> ')
    while new_user_input.lower() != 'exit':

        # checks to make sure the user enters the correct command
        input_checker = new_user_input.split()

        # creates the stations
        if 'create station' in new_user_input and len(input_checker) == 3:
            station_create = new_user_input.split('create station')
            my_dict[station_create[1].strip()] = []

            # this is for the plan trip
            station_split = new_user_input.split()
            locations[station_split[2]] = []

        # connects the stations
        elif 'connect stations' in new_user_input and len(input_checker) == 5:
            station_connect = new_user_input.split()[2:]
            line_connect = station_connect[2]
            # line_connect = station_connect[2].split('-')

            # adds the line to my_dict as a list
            my_dict[station_connect[0].strip()].append(line_connect)
            my_dict[station_connect[1].strip()].append(line_connect)

            # this is for the plan trip
            connect_split = new_user_input.split()[2:]
            loc_1 = connect_split[0]
            loc_2 = connect_split[1]
            locations[loc_1].append(loc_2)
            locations[loc_2].append(loc_1)

        # creates the trains
        elif 'create train' in new_user_input and len(input_checker) == 5:
            train_create = new_user_input.split()[2:]
            my_dict[train_create[2]].append(train_create[0])

            # adds to the dictionary where the train id is the key
            train_dict[train_create[0]] = [train_create[1], train_create[2]]

        # displays the stations
        elif new_user_input == 'display stations' and len(input_checker) == 2:
            for keys in my_dict:
                keys.join('\n')
                print(f'    {keys}')

        # displays the trains
        elif new_user_input == 'display trains' and len(input_checker) == 2:
            for key in train_dict:
                print(f'*** Information for Train {key} ***')
                print(f'    Line: {train_dict[key][0]}')
                print(f'    Current position: {train_dict[key][1]}')

        # displays specific train info
        elif 'get train info' in new_user_input and len(input_checker) == 4:
            train_info = ''.join(new_user_input.split()[3:])

            print(f'*** Information for Train {train_info} ***')
            print(f'    Line: {train_dict[train_info][0]}')
            print(f'    Current position: {train_dict[train_info][1]}')

        # displays specific station info
        elif 'get station info' in new_user_input and len(input_checker) == 4:
            station_info = ''.join(new_user_input.split()[3:])

            print(f'*** Information for Station {station_info} ***')
            print(f'    {my_dict[station_info][0]} Line - Next station: {locations[station_info][0]}')

        # plans the trip
        elif 'plan trip' in new_user_input and len(input_checker) == 4:
            plan_split = new_user_input.split()[2:]
            loc_1 = plan_split[0]
            loc_2 = plan_split[1]
            visited = []
            new_ans = plan_trip(locations, loc_1, loc_2, visited)
            joiner = ' --> '.join(new_ans)
            current_line = my_dict[new_ans[0]][0]
            new_string = ''
            for i in range(len(new_ans) - 1):
                for connections in my_dict[new_ans[i]]:
                    if connections != current_line and connections in my_dict[new_ans[i + 1]]:
                        new_string = new_string + f'--> at {new_ans[i]} transfer from {current_line} line to {connections} line'
                        current_line = connections
                    # elif connections in my_dict[new_ans[i + 1]]:
                new_string = new_string + ' --> ' + new_ans[i]

            print(f'start on {my_dict[new_ans[0]][0]}' + new_string + ' --> ' + new_ans[-1])

        # step - moves all the train to the next station
        elif new_user_input == 'step':
            for i in train_dict:
                split_pos = train_dict[i][0].split('-')
                if train_dict[i][1] == split_pos[0]:
                    print(f'{i} has moved from {split_pos[0]} to {split_pos[1]}')
                    train_dict[i][1] = split_pos[1]
                else:
                    print(f'{i} has moved from {split_pos[1]} to {split_pos[0]}')
                    train_dict[i][1] = split_pos[0]

        else:
            print('unknown command')

        new_user_input = input(f'[{user_input}] >>> ')
    return my_dict


if __name__ == '__main__':
    play_game()
