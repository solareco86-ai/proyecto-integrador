### Subtareas del aprendizaje: partición train/test y prevención de fugas (data leakage)

El proceso de inducción matemática requiere una metodología estricta para garantizar que el modelo no memorice los ejemplos de entrenamiento, sino que adquiera capacidad real de generalización.

#### Partición de Datos: Train y Test
Nunca debemos evaluar un modelo sobre los mismos datos utilizados para ajustar sus parámetros:
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
```

#### Prevención de Fugas de Información (Data Leakage)
Una fuga ocurre cuando información del conjunto de prueba contamina el proceso de entrenamiento (por ejemplo, normalizar todo el dataset junto antes de separarlo en train y test). 
- Los transformadores (escaladores MinMax, vectorizadores) deben ajustarse (`fit`) **únicamente** sobre `X_train`.
- Luego, se aplican (`transform`) sobre `X_test` y en el endpoint de la API.
