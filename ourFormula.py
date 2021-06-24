class Atom:
    """
    This class represents propositional logic variables in modal logic formulas.
    """

    def __init__(self, name):
        self.name = name

    def semantic(self, ks, world_to_test):
        """Function returns assignment of variable in Kripke's world.
        """
        # if self.name in world_to_test:
        #     return True
        # else:
        #     return False
        return world_to_test.assignment.get(self.name, False)

    def __eq__(self, other):
        return isinstance(other, Atom) and other.name == self.name

    def __str__(self):
        return str(self.name)