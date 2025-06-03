import numpy as np
from .predictors import PREDICTORS

class ImageDecoder:
    def __init__(self, window_size: int = 10):
        self.N = window_size
    
    def decode(self, residuals: np.ndarray, height: int, width: int) -> np.ndarray:
        """Восстанавливает изображение из остатков"""
        residuals = residuals.reshape((height, width))
        image = np.zeros((height, width), dtype=np.int16)

        for row in range(height):
            row_errors = np.zeros((self.N, len(PREDICTORS)))

            for col in range(width):
                if col == 0:
                    if row == 0:
                        image[row, col] = residuals[row, col]
                    else:
                        pred = PREDICTORS[2](row, col, image)  # predictor_up
                        image[row, col] = pred + residuals[row, col]
                    continue

                best_idx = self._select_best_predictor(col, row_errors)
                pred = PREDICTORS[best_idx](row, col, image)
                image[row, col] = pred + residuals[row, col]
                self._update_errors(row, col, row_errors, image)

        return np.clip(image, 0, 255).astype(np.uint8)
    
    def _select_best_predictor(self, col: int, row_errors: np.ndarray) -> int:
        """Аналогично методу в encoder"""
        if col > 1:
            row_means = row_errors[0:min(col, self.N), :].mean(axis=0)
            return int(np.argmin(row_means))
        return 1
    
    def _update_errors(self, row: int, col: int, row_errors: np.ndarray, 
                      image: np.ndarray):
        """Обновляет матрицу ошибок"""
        row_errors = np.roll(row_errors, shift=1, axis=0)
        actual = image[row, col]
        for k, predictor in enumerate(PREDICTORS):
            p = predictor(row, col, image)
            row_errors[0, k] = (actual - p) ** 2