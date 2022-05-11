import numpy as np
import random


class Node:
    def __init__(self, id):
        self.id = id
        self.attr = {
            "NEIGHBORS": [],
            "EDGES": [],
            "N_POS": np.array([random.random(), random.random()])
        }
        self.attr["DEGREE"] = len(self.attr["NEIGHBORS"])
