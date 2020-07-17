import random
from queue import Queue
from ast import literal_eval
from pdb import set_trace as bp
import logging

from player import Player
from world import World

FORMAT = "%(asctime)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)
logging.disable(logging.DEBUG)
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)


def room_bfs(initial: int, target: int, p_map: dict) -> list:
    """
    Execute a breadth-first search for the shortest
    path back to the last room with unexplored paths

    initial: starting node

    target: target node

    p_map: player map
    """
    steps = {}
    q = Queue()
    q.put(initial)
    while not q.empty():
        cur = q.get()
        # print(cur)
        for direction in p_map[cur]:
            q.put(p_map[cur][direction])
            if cur not in steps:
                steps[p_map[cur][direction]] = [direction]
            else:
                steps[p_map[cur][direction]] = list(steps[cur])
                steps[p_map[cur][direction]].append(direction)
            if p_map[cur][direction] == target:
                shortest_path = steps[p_map[cur][direction]]
                return shortest_path
    return


def path_finder(plyr):
    """
    Returns path (list) that ensures visitation of every room in map
    """
    # Solution 2:
    path = []
    # enqueue starting room
    nav_stack = []
    done = False
    player_map = {}
    prv = None
    opposite_dirs = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}
    change_dir = False
    starting_room = plyr.current_room.id

    # while queue is not empty
    while not done:
        cur_room = plyr.current_room.id
        # fill out map
        if cur_room not in player_map:
            exits = plyr.current_room.get_exits()
            player_map[cur_room] = {e: '' for e in exits}

        logging.debug(f"prv is {prv}")
        if prv is not None:
            player_map[cur_room][opposite_dirs[current_dir]] = prv
            player_map[prv][current_dir] = cur_room
            logging.debug(f"executing player map fill for room {cur_room}")

        unexplored = [direction for direction in player_map[cur_room]
                      if player_map[cur_room][direction] == '']

        logging.debug("Player map: " + str(player_map))
        logging.debug(f"cur_room: {cur_room}, unexplored: {unexplored}")
        logging.debug(f"change dir: {change_dir}")
        logging.debug(f"nav_stack {nav_stack}")

        if not prv:  # check if this will work sans condition 2
            if cur_room == starting_room:
                if len(unexplored) == 0:
                    done = True
                    break
            current_dir = random.choice(unexplored)

        if len(unexplored) > 1:
            nav_stack.append(cur_room)
            # change directions if current is not available
            if current_dir in player_map[cur_room]:
                plyr.travel(current_dir)
                path.append(current_dir)
                prv = cur_room
            else:
                current_dir = random.choice(unexplored)
                plyr.travel(current_dir)
                path.append(current_dir)
                prv = cur_room
        elif len(unexplored) == 0:
            # perform search and navigate back to room
            if len(nav_stack) > 0:
                origin_room = nav_stack.pop()
            else:
                done = True
                break
            # check if final room has been directionally exhausted
            if len(nav_stack) == 0:
                if '' in player_map[origin_room].values():
                    nav_stack.append(origin_room)
                else:
                    done = True
                    break
            navigation = room_bfs(cur_room, origin_room, player_map)
            for step in navigation:
                plyr.travel(step)
                path.append(step)
                prv = None
        else:
            # change directions if player hits a corner
            if current_dir in player_map[cur_room]:
                plyr.travel(current_dir)
                path.append(current_dir)
                prv = cur_room
            else:
                current_dir = unexplored.pop()
                plyr.travel(current_dir)
                path.append(current_dir)
                prv = cur_room

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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
