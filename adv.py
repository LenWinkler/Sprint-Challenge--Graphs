from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# print(player.current_room.id)
# print('get exits', player.current_room.get_exits())
# player.travel('n')
# print(player.current_room.id)
# print('get exits after moving', player.current_room.get_exits())


# fn to convert room ids to directions in bfs
def convert(adjacency_dict, next_room):
    for direction, id in adjacency_dict.items():
        if id == next_room:
            return direction

graph = {}

room_count = 0

curr_room = 0
prev_room = None

opposite = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
}

# outer while loop
while room_count < 9:

    # DFS while loop
    while True:
        # when visiting each room
        # if room is not already in the graph, add it and increment room_count
        if not curr_room in graph:
            graph[player.current_room.id] = {i: '?' for i in player.current_room.get_exits()}
            room_count += 1
        # if it is
        else:
        # if unvisited exits
            if '?' in graph[player.current_room.id].values():
                # pick one, add exit to traversal_path
                choice = random.choice(list(graph[player.current_room.id].keys()))
                while graph[player.current_room.id][choice] != '?':
                    choice = random.choice(list(graph[player.current_room.id].keys()))
                prev_room = curr_room
                player.travel(choice)
                # check if you're in a different room (exit wasn't dead end)
                curr_room = player.current_room.id
                if curr_room != prev_room:
                    traversal_path.append(choice)
                    # set adjacency values
                    graph[prev_room][choice] = curr_room
                    # if room is not already in the graph, add it and increment room_count
                    if not curr_room in graph:
                        graph[player.current_room.id] = {i: '?' for i in player.current_room.get_exits()}
                        room_count += 1
                    graph[curr_room][opposite[choice]] = prev_room
                else:
                    graph[curr_room][choice] = 'x'

            # if no unvisited exits, go to next loop
            else:
                proceed = True
                break


    
    # do a bfs for the nearest room with an unvisited exit
    # once the room is found, append the path to get to it to traversal path
    proceed = True
    while proceed:
        # create queue and enqueue current_room
        queue = Queue()
        queue.enqueue([curr_room])
        # create visited set
        visited = set()
        # while queue not not empty
        while queue.size() > 0:
            # dequeue path
            path = queue.dequeue()
            path_directions = []
            # if last room in path has unvisited exit
            print('asdf', graph[path[-1]].values())
            if '?' in graph[path[-1]].values():
                # convert room ids into path directions
                for i in range(len(path)):
                    path_directions.append(convert(graph[curr_room], path[i]))
                    curr_room = path[i]
                traversal_path = traversal_path + path_directions[1:]
                proceed = False
                break
            # if room not in visited
            if not path[-1] in visited:
                # add it
                visited.add(path[-1])
            # enqueue this rooms exits
            for exit in graph[path[-1]].values():
                if exit != '?' and exit not in visited:
                    # create copy of path
                    new_path = list(path)
                    # add neighbor to it
                    new_path.append(exit)
                    # enqueue the new path
                    queue.enqueue(new_path)


# # # populate graph with empty dicts
# # for i in range(0, 3):
# #     graph[i] = {}

# # vars to track which room we're in
# curr_room = 0
# prev_room = 0

# # var to track # of rooms visited
# number_visited = 1

# # each direction's opposite
# opposite = {
#     'n': 's',
#     's': 'n',
#     'e': 'w',
#     'w': 'e'
# }

# # populate graph
# while number_visited < len(graph):
#     curr_room = player.current_room.id
#     exits = player.current_room.get_exits()
#     print('curr room', curr_room)
#     print('exits', exits)

#     exits_dict = {}
    
#     # add exits to current room's adjacency dict
#     for exit in exits:
#         exits_dict[exit] = '?'
#     graph[curr_room] = exits_dict
    
#     print(graph)
    
#     # loop through and pick an unexplored exit
#     for exit in exits:
#         # if exit unexplored, go there
#         if graph[curr_room][exit] == '?':
#             player.travel(exit)
#             # make sure we're not in the same room ()
#             curr_room = player.current_room.id
#             if curr_room == prev_room:
#                 graph[curr_room][exit] = 'x'
#                 continue
#             else:
#                 traversal_path.append(exit)
#                 graph[prev_room][exit] = curr_room
#                 graph[curr_room][opposite[exit]] = prev_room
#                 number_visited += 1
#                 prev_room = curr_room
#                 exits_dict = {}

# print('graph', graph)

# travel there and log the direction in traversal_path


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
