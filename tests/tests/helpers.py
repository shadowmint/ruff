import random
import ruff


def touch_file(path):
    """ Write some random content to the given path """
    lines = """
        Origen saith that the Magical Art doth not contain anything subsisting,
        although it should, yet that it must not be Evil, or subject to contem
        doth distinguish the Natural Magic Diabolical. Apollonius Tyannaeus
        Natural Magic , by the which he did perform wonderful things. Philo
        of the Secret Works of Nature, is so far from being contemptible that
        Monarchs and Kings have studied it. Nay! among the Persians none might
        unless he was skilful in this Noble Science often degenerateth, from
    """.split('\n')
    with open(path, 'w') as fp:
        for r in range(random.randint(5, 20)):
            line = lines[random.randint(0, len(lines) - 1)]
            fp.write(line)


def path(*largs):
    """ Return a relative path """
    return ruff.path(__file__, *largs)
