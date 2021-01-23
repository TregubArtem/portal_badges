import random


def read_file_by_lines(file_name, randomize):
    result = []

    for line in open(file_name, "r", encoding="utf-8"):
        line = line.strip()

        result.append(line)

    if randomize:
        random.shuffle(result)

    return result


def get_random_item(array, remove_after):
    index = random.randint(0, len(array) - 1)

    result = array[index]

    if remove_after:
        array.remove(result)

    return result
