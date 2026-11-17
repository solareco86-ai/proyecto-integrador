# Especificación de Requisitos de Software (SRS) - Módulo Fundamentos

## 1. Introducción
El presente documento especifica los requisitos técnicos y funcionales para el módulo de *Fundamentos de la Programación* del Proyecto Integrador.

## 2. Descripción General
El sistema provee una estructura modular en Markdown y YAML para la enseñanza de pseudocódigo (PSeInt) y lógica de programación, integrada con flujos de control de versiones en GitHub.

## 3. Requisitos Funcionales
* **RF01:** El repositorio debe almacenar las definiciones del curso en archivos estructurados (`curso.yaml` y lecciones en formato `.md`).
* **RF02:** El sistema de validación debe verificar la sintaxis de las lecciones para asegurar que cumplan con los estándares pedagógicos.
* **RF03:** Toda incorporación de contenido curricular debe realizarse exclusivamente a través de Pull Requests revisados y aprobados por al menos un par.

## 4. Criterios de Aceptación
* Validación exitosa de esquemas YAML sin errores de sintaxis.
* Renderizado correcto de las lecciones en Markdown dentro de la plataforma de visualización del curso.
