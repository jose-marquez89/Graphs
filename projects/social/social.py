import random
from queue import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif (friend_id in self.friendships[user_id] or
              user_id in self.friendships[friend_id]):
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment ID for new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than
        the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        """
        Originally, I thought I might have to pick from a range of possible
        values, which is why this 'friend_pos_rng variable is here. Didn't end
        up needing it - Me, from the past
        """
        # friend_pos_rng = list(range(0, (avg_friendships*2)+1))

        # create a list of all possible friendships
        possible_friendships = []
        for x in range(1, num_users+1):
            for y in range(1, num_users+1):
                if x == y:
                    continue
                elif x > y:
                    continue
                else:
                    possible_friendships.append((x, y))

        random.shuffle(possible_friendships)
        total_friendships = avg_friendships*num_users
        friend_i_verse = possible_friendships[:((total_friendships)//2)]

        # Add users
        for user in range(1, num_users+1):
            self.add_user(user)

        # Create friendships
        for user, friend in friend_i_verse:
            self.add_friendship(user, friend)

        return

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        paths = {}  # Note that this is a dictionary, not a set
        node_q = Queue()
        node_q.put(user_id)
        while not node_q.empty():
            current_user = node_q.get()
            print(current_user)

            if current_user not in paths:
                paths[current_user] = [current_user]

            for immediate in self.friendships[current_user]:
                if immediate in paths:
                    continue
                paths[immediate] = list(paths[current_user])
                paths[immediate].append(immediate)
                node_q.put(immediate)

        return paths


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
