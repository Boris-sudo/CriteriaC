def unpack(file, count):
    return 1

def get_labyrinth(number):
    filename = "myapp\static\maze\maze{}.kiva".format(number)
    with open(filename, "w") as file:
        data = unpack(file, 4)