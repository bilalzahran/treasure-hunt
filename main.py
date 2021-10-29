from random import randint

probable_location = []
GRID_SIZE = 7
MAX_TREASURE = 5
grid = [
    # 0     1    2    3    4    5    6    7
    ["#", "#", "#", "#", "#", "#", "#", "#"],  # 0
    ["#", ".", ".", ".", ".", ".", ".", "#"],  # 1
    ["#", ".", ".", ".", ".", ".", ".", "#"],  # 2
    ["#", ".", ".", ".", ".", ".", ".", "#"],  # 3
    ["#", ".", "#", "#", "#", ".", ".", "#"],  # 4
    ["#", ".", ".", ".", "#", ".", "#", "#"],  # 5
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
    generate_probable_treasure_coordinate()

    return player_location, treasure_count, treasure_list


def game_loop():
    player_location, treasure_count, treasure_list = init_game()
    print("Availabel Command:")
    print("1. up")
    print("2. down")
    print("3. right")
    print("4. left")
    print("5. check: check the probable location of treasure")
    print("6. show: show the location of the treasure")
    print("7. grid: show grid with the probable location of treasure")
    print("\nYour Treasure: ", treasure_count)
    print(f"You are at {player_location.to_string()} now\n")
    while True:
        command = input(" Where to go: ")
        command_combination = command.split(" ")

        direction = command_combination[0].lower()
        player_location = process_command(direction, player_location)

        # Check if user not hitting the wall or out of bound
        if not check_on_grid(player_location):
            print("You are hitting the wall! Go back!")
            player_location = process_command(
                undo_direction_dict[direction], player_location)

        # Update the probable location of treasure
        update_probable_treasure_coordinate(player_location)

        # Check if user get the treasure
        treasure, treasure_status = check_treasure(
            player_location, treasure_list)
        if treasure_status:
            print(f"Congrats! You got {treasure} treasure!")
            treasure_count += treasure

        # Check if user get all the treasure, if yes end the game
        if treasure_count == MAX_TREASURE:
            print("You got all treasure!")
            break

        print("\nYour treasure: ", treasure_count)
        print(f"You are at {player_location.to_string()} now \n")


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

        if not_wall or not (treasure_location.x == 6 and treasure_location.y == 1):
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
    elif direction == "check":
        check_probable_treasure_coordinate()
    elif direction == "grid":
        show_grid_with_probable_treasure()
    else:
        print("I dont understand the direction")

    return player_location


def check_treasure(player_location: Point, treasure_list):
    treasure = 0
    for item in treasure_list:
        item: Point = item
        if(item.is_equal(player_location)):
            treasure += 1
    if treasure > 0:
        return treasure, True
    else:
        return 0, False


def generate_probable_treasure_coordinate():
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == ".":
                probable_location.append(Point(i, j))


def check_probable_treasure_coordinate():
    for item in probable_location:
        print(item.to_string())


def show_grid_with_probable_treasure():
    for i, row in enumerate(grid):
        print("")
        for j, col in enumerate(row):
            if col == ".":
                print("$", end="")
            else:
                print(col, end="")
    print("")


def update_probable_treasure_coordinate(point: Point):
    for i, item in enumerate(probable_location):
        if item.is_equal(point):
            probable_location.pop(i)


if __name__ == "__main__":
    game_loop()
