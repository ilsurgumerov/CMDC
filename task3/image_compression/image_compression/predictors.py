import numpy as np

def predictor_none(row: int, col: int, image: np.ndarray) -> int:
    """Пустой предиктор (всегда 0)"""
    return 0

def predictor_left(row: int, col: int, image: np.ndarray) -> int:
    """Левый сосед (A)"""
    return int(image[row, col - 1]) if col > 0 else 0

def predictor_up(row: int, col: int, image: np.ndarray) -> int:
    """Верхний сосед (B)"""
    return int(image[row - 1, col]) if row > 0 else 0

def predictor_average(row: int, col: int, image: np.ndarray) -> int:
    """Среднее A и B"""
    a = predictor_left(row, col, image)
    b = predictor_up(row, col, image)
    return (a + b) // 2

def predictor_paeth(row: int, col: int, image: np.ndarray) -> int:
    """Предиктор Paeth"""
    a = predictor_left(row, col, image)
    b = predictor_up(row, col, image)
    c = int(image[row - 1, col - 1]) if row > 0 and col > 0 else 0
    p = a + b - c
    pa, pb, pc = abs(p - a), abs(p - b), abs(p - c)
    return a if pa <= pb and pa <= pc else b if pb <= pc else c

# Все доступные предикторы, при добавлении стоит добавлять в конце этого списка
PREDICTORS = [
    predictor_none, 
    predictor_left, 
    predictor_up,
    predictor_average,
    predictor_paeth
]