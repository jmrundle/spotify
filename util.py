import numpy as np


def random_weighted_select(items, limit):
    """
    Generates a new list of length "limit" with a strong preference
    towards items near the beginning of the list
    """
    # quadratic inverse weights
    size = len(items)
    weights = np.arange(size, 0, -1)
    weights = np.square(weights)
    weights = np.divide(weights, np.sum(weights))

    indexes = np.random.choice(size, limit, p=weights, replace=False)
    return [items[i] for i in indexes]


def random_select(items, limit):
    size = len(items)
    indexes = np.random.choice(size, limit, replace=False)
    return [items[i] for i in indexes]


if __name__ == "__main__":
    letters = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()"
    rand_w = random_weighted_select(letters, 15)
    rand = random_select(letters, 15)

    string = "["
    string2 = "["
    for letter in letters:
        if letter in rand:
            string += letter
        else:
            string += "_"
        if letter in rand_w:
            string2 += letter
        else:
            string2 += "_"
    string += "]"
    string2 += "]"

    print("Non-Weighted: ", string)
    print("Weighted:     ", string2)
