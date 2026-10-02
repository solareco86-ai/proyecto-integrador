### Serialización y persistencia de artefactos con joblib

El entrenamiento de modelos suele realizarse offline o en procesos batch de cómputo intensivo. Una vez optimizados los parámetros, el artefacto se congela y persiste en disco mediante serialización binaria.

#### ¿Por qué joblib sobre pickle tradicional?
La librería `joblib` está optimizada para estructuras de datos científicas de Python (arrays de NumPy y modelos de scikit-learn), comprimiendo arrays grandes y acelerando los tiempos de lectura y escritura en disco.

#### Guardado y Carga de Modelos
```python
import joblib
from sklearn.naive_bayes import GaussianNB
import numpy as np

# Datos sintéticos de calibración
X_train = np.array([[20.0, 1.2], [85.0, 8.5], [22.0, 1.5], [90.0, 9.0]])
y_train = np.array(["normal", "critico", "normal", "critico"])

modelo = GaussianNB()
modelo.fit(X_train, y_train)

# Persistir el artefacto entrenado
joblib.dump(modelo, "modelos/bayes_v1.joblib")

# Cargar en un entorno de inferencia
modelo_recuperado = joblib.load("modelos/bayes_v1.joblib")
pred = modelo_recuperado.predict([[82.0, 7.8]])
print(f"Predicción recuperada: {pred[0]}")
```
