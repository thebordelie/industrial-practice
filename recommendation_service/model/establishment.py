class Establishment:

    def __init__(self, name: str, description: str, address: str, score: float):
        self.address = address
        self.description = description
        self.name = name
        self.score = score

    def to_json(self) -> str:
        json = f"'name':'{self.name}', 'description': '{self.description}', 'address': '{self.address}', 'score': '{self.score}'"
        json = "{" + json + "}"
        return json

    def __lt__(self, other):
        return self.score > other.score
