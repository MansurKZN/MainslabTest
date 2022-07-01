import random

def fraudDetector(s: str) -> float:
    return random.random()


def serviceClassifier(s: str) -> dict:
    d = {1: 'консультация', 2: 'лечение', 3: 'стационар', 4: 'диагностика', 5: 'лаборатория'}
    rand = random.randint(1, 5)
    return {rand: d.get(rand)}
