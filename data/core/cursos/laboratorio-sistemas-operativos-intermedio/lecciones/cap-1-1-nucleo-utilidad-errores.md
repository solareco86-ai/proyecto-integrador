### El núcleo del sistema operativo

El **núcleo (kernel)** es el componente central que administra los recursos. En esta lección vemos cómo organiza el trabajo y **su utilidad ante situaciones de error**: cuando algo falla, el núcleo es quien detecta el problema, registra información y decide cómo responder.

### Responsabilidades del núcleo

| Responsabilidad | Qué hace |
| :--- | :--- |
| Gestión de procesos | Reparte la CPU entre los programas |
| Gestión de memoria | Asigna y protege la RAM |
| Sistema de archivos | Organiza los datos en disco |
| Control de dispositivos | Atiende el hardware y sus controladores |
| Gestión de errores | Detecta fallas y registra información |

### El núcleo y los errores

Cuando un programa falla, el núcleo:

1. **Detecta** el error (por ejemplo, un acceso inválido a memoria).
2. **Registra** el evento en los registros del sistema.
3. **Termina** el programa problemático sin caer todo el sistema.
4. En fallas graves, muestra el **panic** del kernel (pantalla de error del núcleo).

Los mensajes del núcleo se revisan con:

```bash
dmesg
journalctl -k
```

### El núcleo en la práctica

Para conocer el núcleo en uso:

```bash
uname -r      # versión del núcleo
uname -m      # arquitectura
cat /proc/version
```

### Los módulos del núcleo

El núcleo de Linux es **modular**: los controladores de dispositivos son módulos que se cargan y descargan según hace falta.

```bash
lsmod                 # módulos cargados
modinfo <módulo>      # información de un módulo
```

### Micro-desafío práctico

> Ejecutá `uname -r` y anotá la versión del núcleo. Revisá `dmesg` (o `journalctl -k | tail`) y buscá líneas de error o advertencia (palabras *error* o *fail*). Listá los módulos con `lsmod` y elegí tres para explicar qué dispositivo controlan.

### Resumen

- El núcleo administra procesos, memoria, archivos y dispositivos.
- Ante errores registra información y aísla el problema.
- `dmesg` y `journalctl -k` muestran los mensajes del núcleo.
- El núcleo de Linux es modular: los drivers se cargan como módulos.
