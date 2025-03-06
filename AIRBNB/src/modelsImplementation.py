import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

import numpy as np

class LinearRegressionNormalEquation:
    def __init__(self):
        self.theta = None

    def fit(self, X, y):
        if y.ndim == 1:
            y = y.reshape(-1, 1)  # Asegurar vector columna
        
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # Agregar término de sesgo
        self.theta = np.linalg.pinv(X_b.T @ X_b) @ X_b.T @ y  # Usar pseudoinversa

    def predict(self, X):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        return X_b @ self.theta


class LinearRegressionSVD:
    def __init__(self):
        self.theta = None

    def fit(self, X, y):
        # Agregar una columna de unos para el término de sesgo
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        
        # Realizar la descomposición en valores singulares (SVD)
        U, S, Vt = np.linalg.svd(X_b, full_matrices=False)
        
        # Invertir S (matriz diagonal de los valores singulares)
        S_inv = np.diag(1.0 / S)
        
        # Calcular theta usando la descomposición SVD
        self.theta = Vt.T.dot(S_inv).dot(U.T).dot(y)

    def predict(self, X):
        # Agregar una columna de unos para el término de sesgo
        X_b = np.c_[np.ones((X.shape[0], 1)), X]
        return X_b.dot(self.theta)

class LinearRegressionBatchGD:
    def __init__(self, learning_rate=0.01, n_iterations=1000, tolerance=1e-6):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.tolerance = tolerance  # Umbral de convergencia
        self.theta = None

    def fit(self, X, y):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # Añadir el término independiente
        self.theta = np.random.randn(X_b.shape[1])  # Inicialización aleatoria de parámetros
        m = X_b.shape[0]

        for iteration in range(self.n_iterations):
            # Calcular el gradiente
            gradients = 2 / m * X_b.T.dot(X_b.dot(self.theta) - y)
            
            # Actualizar los parámetros
            self.theta -= self.learning_rate * gradients

            # Verificar si los gradientes son pequeños (condición de convergencia)
            if np.linalg.norm(gradients) < self.tolerance:
                print(f'Convergió en la iteración {iteration + 1}')
                break

    def predict(self, X):
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # Añadir el término independiente
        return X_b.dot(self.theta)

class LinearRegressionSGD:
    def __init__(self, epochs=10000, learning_rate=0.01, lr_init_sch=5, lr_end_sch=50, tol=1e-6):
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.tol = tol
        self.lr_init_sch = lr_init_sch
        self.lr_end_sch = lr_end_sch
        self.theta = None  # Se inicializa en None hasta llamar a `fit`

    def fit(self, X, y):
        if not isinstance(X, np.ndarray) or not isinstance(y, np.ndarray):
            raise ValueError("X e y deben ser arrays de NumPy.")

        m, n = X.shape
        X_b = np.c_[np.ones((m, 1)), X]  # Agrega el término de sesgo (bias)
        y = y.reshape(-1, 1)  # Asegurar que y sea una matriz columna
        self.theta = np.zeros((n + 1, 1))  # Inicialización en ceros

        for epoch in range(self.epochs):
            for i in range(m):
                random_index = np.random.randint(m)
                xi = X_b[random_index:random_index+1]  # Selección de una muestra (1, n+1)
                yi = y[random_index:random_index+1]  # Selección del valor correspondiente (1,1)

                gradients = 2 * xi.T.dot(xi.dot(self.theta) - yi)  # Cálculo del gradiente (n+1, 1)
                eta = self.learning_rate / (epoch * m + i + self.lr_end_sch)  # Programación del aprendizaje
                
                if np.linalg.norm(gradients) < self.tol:
                    print(f"Convergencia alcanzada en la época {epoch}, iteración {i}")
                    return  # Detener el entrenamiento si la norma del gradiente es menor que `tol`
                
                self.theta -= eta * gradients  # Actualización de parámetros

    def predict(self, X):
        if self.theta is None:
            raise ValueError("El modelo no ha sido entrenado. Llama a `fit` antes de predecir.")
        X_b = np.c_[np.ones((X.shape[0], 1)), X]  # Agregar la columna de unos para el término de sesgo
        return X_b.dot(self.theta)
