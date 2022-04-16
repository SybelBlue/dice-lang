from cProfile import label
from typing import Iterable, Tuple
from dice import *

import matplotlib.pyplot as plt


def get_dist_data(dice: Dice) -> Tuple[str, list[int], list[float]]:
    dist = sorted(dice.distribution().items())
    return str(dice), list(x for x, _ in dist), list(y for _, y in dist)

def plot_dists(dists: Iterable[Dice]):
    dists_data = tuple(map(get_dist_data, dists))

    col_width = 1 / (len(dists_data) + 0.5)
    # min_x = min(n for data in dists_data for n in data[0])
    # max_x = max(n for data in dists_data for n in data[0])

    # x_bar_baseline = np.arange(max_x - min_x)


    for i, (l, xs, ys) in enumerate(dists_data):
        position = [x + col_width * i for x in xs]
        plt.bar(position, ys, width=col_width, label=l)



plot_dists((
    3 * D(4),
    D(6) + D(4) + 2
))

plt.legend()
plt.show()
