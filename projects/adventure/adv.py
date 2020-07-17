import random
import random
from queue import Queue
from ast import literal_eval

from player import Player
from world import World

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


def room_bfs(initial, target):
    """
    Execute a breadth-first search for the shortest
    path back to the last room with unexplored paths
    """
    return


def path_finder(plyr):
    # First pass solution:
    # Pick a random direction (or not)
    # Move in that direction until exhausted
    # Reverse direction until you reach starting point
    # Move in an unexplored direction

    # Solution 2:
    # Enqueue starting room
    q = Queue()
    q.put(plyr.current_room.id)
    player_map = {}
    prv = None
    opposite_dirs = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

    # While queue is not empty
    while not q.empty():
        cur = q.get()
        exits = plyr.current_room.get_exits()
        # fill out map
        if cur not in player_map:
            player_map[cur] = {e: '' for e in exits}

        if prv:
            player_map[cur][]
        # pick a direction
        current_dir = random.choice(exits)

        # move in this direction

        # at every room, check if unexplored > 1
        # if unexplored
           # queue this room
        # when direction is exhausted
           # search for shortest path back to queued room
    path = []
    return path


# Fill this out with directions to walk
# traversal_path = ['n', 'n']
# traversal_path = ['n', 'n', 's', 's', 's', 's', 'n', 'n', 'e', 'e',
#                   'w', 'w', 'w', 'w']
traversal_path = path_finder(player)


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, "
          f"{len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
