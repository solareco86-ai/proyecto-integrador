### Niveles de ejecución y apagado

El sistema operativo distingue **estados de funcionamiento** y ofrece un **apagado ordenado** de la máquina y de la sesión. Hacerlo correctamente evita pérdida de datos y daños en los archivos.

### Niveles de ejecución (runlevels)

En los sistemas con systemd, los estados de funcionamiento se gestionan con **targets**:

| Target | Estado |
| :--- | :--- |
| `poweroff.target` | Apagado |
| `rescue.target` | Mantenimiento con lo mínimo |
| `multi-user.target` | Modo texto con red |
| `graphical.target` | Escritorio gráfico (el habitual) |

Para ver el estado actual:

```bash
systemctl get-default
```

Para entrar a modo de mantenimiento:

```bash
sudo systemctl isolate rescue.target
```

### Apagado correcto

| Comando | Acción |
| :--- | :--- |
| `shutdown` | Apaga el sistema de forma ordenada |
| `shutdown -r now` | Reinicia de inmediato |
| `shutdown +5` | Apaga dentro de 5 minutos |
| `poweroff` | Apaga la máquina |
| `reboot` | Reinicia |
| `halt` | Detiene el sistema |

> Apagar con el botón físico sin avisar al sistema puede provocar pérdida de datos o archivos dañados.

### Cerrar la sesión

En XFCE, cerrar la sesión se hace desde el menú *Acciones → Cerrar sesión*, o con:

```bash
logout
```

Cerrar la sesión termina tus programas y vuelve a la pantalla de acceso, dejando la máquina encendida.

### Suspender y bloquear

- **Bloquear la sesión:** protege el equipo sin cerrar programas (el menú XFCE o `xflock4`).
- **Suspender:** detiene el consumo de energía y mantiene la sesión en memoria.

### Micro-desafío práctico

> Consultá el target por defecto con `systemctl get-default`. Configurá un apagado programado con `shutdown +5` y cancelalo con `shutdown -c`. Explicá en tu cuaderno por qué conviene apagar con `shutdown` en lugar de cortar la energía directamente.

### Resumen

- Los targets de systemd representan los estados del sistema.
- `shutdown` apaga de forma ordenada; `reboot` reinicia.
- Cerrar la sesión vuelve a la pantalla de acceso.
- Apagar correctamente protege los datos y el sistema.
