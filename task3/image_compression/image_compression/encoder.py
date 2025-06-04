import numpy as np
from .predictors import PREDICTORS

class ImageEncoder:
    def __init__(self, window_size: int = 10):
        self.N = window_size
    
    def encode(self, image: np.ndarray) -> np.ndarray:
        """Кодирует изображение в вектор остатков"""
        if len(image.shape) != 2:
            raise ValueError("Only grayscale images are supported")
        
        image = image.astype(np.int16)
        h, w = image.shape
        residuals = np.zeros_like(image, dtype=np.int16)

        for row in range(h):
            row_errors = np.zeros((self.N, len(PREDICTORS)))

            for col in range(w):
                actual = image[row, col]
                
                if col == 0:
                    if row == 0:
                        residuals[row, col] = actual
                    else:
                        pred = PREDICTORS[2](row, col, image)  # predictor_up
                        residuals[row, col] = actual - pred
                    continue

                best_idx = self._select_best_predictor(col, row_errors)
                pred = PREDICTORS[best_idx](row, col, image)
                residuals[row, col] = actual - pred
                self._update_errors(row, col, row_errors, image, actual)

        return residuals.reshape(-1)
    
    def _select_best_predictor(self, col: int, row_errors: np.ndarray) -> int:
        """Выбирает лучший предиктор на основе ошибок"""
        if col > 1:
            row_means = row_errors[0:min(col, self.N), :].mean(axis=0)
            return int(np.argmin(row_means))
        return 1  # predictor_left по умолчанию для первых элементов в строке
    
    def _update_errors(self, row: int, col: int, row_errors: np.ndarray, 
                      image: np.ndarray, actual: int):
        """Обновляет матрицу ошибок"""
        row_errors = np.roll(row_errors, shift=1, axis=0)
        for k, predictor in enumerate(PREDICTORS):
            p = predictor(row, col, image)
            row_errors[0, k] = (actual - p) ** 2