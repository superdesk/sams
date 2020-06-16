

def dict_contains(object, tests):
    for key, value in tests.items():
        if object.get(key) != value:
            return False

    return True
