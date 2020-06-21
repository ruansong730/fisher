class NoneLocal:
    def __init__(self, v):
        self.v = v


n = NoneLocal(1)

print(n.v)