def unique(list):
    """ Returns an iterator that yields the unique elements of the list """
    found = []
    for l in list:
        if l not in found:
            found.append(l)
            yield l
