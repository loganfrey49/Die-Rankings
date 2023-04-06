class Player:
    def __init__(self, name, elo=1000):
        self.name = name
        self.elo = elo

    def update_elo(self, delta):
        self.elo += delta

    def __str__(self):
        return f"{self.name}: {self.elo}"