from random import randint


GRID_SIZE = 7
MAX_TREASURE = 5
grid = [
    # 0     1    2    3    4    5    6    7
    ["#", "#", "#", "#", "#", "#", "#", "#"],  # 0
    ["#", ".", ".", ".", ".", ".", ".", "#"],  # 1
    ["#", ".", ".", ".", ".", ".", ".", "#"],  # 2
    ["#", ".", ".", ".", ".", ".", ".", "#"],  # 3
    ["#", ".", "#", "#", "#", ".", ".", "#"],  # 4
    ["#", ".", ".", ".", "#", ".", ".", "#"],  # 5
    ["#", ".", "#", ".", ".", ".", ".", "#"],  # 6
    ["#", "#", "#", "#", "#", "#", "#", "#"],  # 7
]

undo_direction_dict = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left"
}


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_string(self):
        return f"({self.x},{self.y})"

    def is_equal(self, point):
        if self.x == point.x and self.y == point.y:
            return True

        return False

    def add_x(self, x):
        self.x += x

    def add_y(self, y):
        self.y += y


def init_game():
    global treasure_list
    global player_location
    global treasure_count

    player_location = Point(6, 1)
    treasure_list = generate_treasure()
    treasure_count = 0

    return player_location, treasure_count, treasure_list


def check_on_grid(point: Point):
    if grid[point.x][point.y] != "#":
        return True

    return False


def generate_treasure():
    treasure_location_list = []
    treasure_count = 0
    while True:
        treasure_location = Point(
            randint(1, GRID_SIZE-1), randint(1, GRID_SIZE))
        not_wall = check_on_grid(treasure_location)

        if not_wall:
            treasure_location_list.append(treasure_location)
            treasure_count += 1

        if treasure_count == MAX_TREASURE:
            break
    return treasure_location_list


def show_grid_with_treasure():
    for item in treasure_list:
        print(item.to_string())


def process_command(direction: str, player_location: Point):
    if direction == "up":
        player_location.add_x(-1)
    elif direction == "down":
        player_location.add_x(1)
    elif direction == "left":
        player_location.add_y(-1)
    elif direction == "right":
        player_location.add_y(1)
    elif direction == "show":
        show_grid_with_treasure()
    else:
        print("I dont understand the direction")

    return player_location


def check_treasure(player_location: Point, treasure_list):
    for item in treasure_list:
        item: Point = item
        if(item.is_equal(player_location)):
            return True

    return False


def game_loop():
    player_location, treasure_count, treasure_list = init_game()
    print("Insert Command: ", treasure_count)
    print(f"You are at {player_location.to_string()} now\n")
    while True:
        command = input(" Where to go: ")
        command_combination = command.split(" ")

        direction = command_combination[0].lower()
        player_location = process_command(direction, player_location)

        if not check_on_grid(player_location):
            print("You are hitting the wall! Go back!")
            player_location = process_command(
                undo_direction_dict[direction], player_location)

        if check_treasure(player_location, treasure_list):
            print("You got one treasure!")
            treasure_count += 1

        if treasure_count == MAX_TREASURE:
            print("You got all treasure!")
            break
        print("\nYour treasure: ", treasure_count)
        print(f"You are at {player_location.to_string()} now \n")


game_loop()
