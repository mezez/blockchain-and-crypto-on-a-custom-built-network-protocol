
class Printable:
    def __repr__(self):
        # define how objects of this class and it's childreen will be printed
        return str(self.__dict__)