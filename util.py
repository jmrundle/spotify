import random


def random_weighted_select(items, limit):
    """
    Generates a new list of length "limit" with a strong preference
    towards items near the beginning of the list
    """
    # quadratic inverse weights
    size = len(items)
    weights = [pow(size - i, 2) for i in range(size)]

    return random.choices(items, weights=weights, k=limit)


def random_select(items, limit):
    return random.choices(items, k=limit)


if __name__ == "__main__":
    letters = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
    rand = random_weighted_select(letters, 15)

    string = "["
    for letter in letters:
        if letter in rand:
            string += letter
        else:
            string += "_"
    string += "]"

    print(string)
