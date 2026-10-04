# 3.3 Selección de features: importancia, correlación, varianza

## Objetivo

Elegir qué features usar. Más features ≠ mejor modelo. Reducir dimensionalidad, evitar overfitting.

## Contenidos

### 1. Correlación con target

```python
import pandas as pd

df = pd.read_csv('data/raw/sensores_energia_2026.csv')

# ¿Qué features correlacionan con power_kw (target)?
correlations = df[['power_kw', 'voltage_v', 'current_a', 'pf']].corr()['power_kw'].sort_values(ascending=False)

# Mantener features con |correlación| > 0.3
selected_features = correlations[abs(correlations) > 0.3].index.tolist()
```

### 2. Importancia según Random Forest

```python
from sklearn.ensemble import RandomForestRegressor

X = df[['voltage_v', 'current_a', 'pf', 'power_kw_lag1']]
y = df['power_kw']

rf = RandomForestRegressor()
rf.fit(X, y)

importances = pd.Series(rf.feature_importances_, index=X.columns).sort_values(ascending=False)
print(importances)

# Mantener features con importancia > 0.05
selected = importances[importances > 0.05].index
```

### 3. Multicolinealidad (VIF)

```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif = pd.DataFrame({
    'feature': X.columns,
    'VIF': [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
})

# Eliminar features con VIF > 5 (alta correlación con otras)
high_vif = vif[vif['VIF'] > 5]['feature'].tolist()
X_selected = X.drop(columns=high_vif)
```

### 4. Permutation Importance

```python
from sklearn.inspection import permutation_importance

rf = RandomForestRegressor()
rf.fit(X, y)

perm_importance = permutation_importance(rf, X, y, n_repeats=10)
print(pd.Series(perm_importance.importances_mean, index=X.columns).sort_values(ascending=False))
```

## Actividad práctica

1. Calcular correlación con target
2. Usar Random Forest para importancia
3. Chequear VIF
4. Seleccionar final: Top 5-10 features

## Palabras clave

Selección, importancia, correlación, VIF, multicolinealidad, dimensionalidad

## Referencias

- [scikit-learn feature_importance](https://scikit-learn.org/stable/auto_examples/inspection/plot_feature_importance.html)
- [statsmodels VIF](https://www.statsmodels.org/stable/generated/statsmodels.stats.outliers_influence.variance_inflation_factor.html)
