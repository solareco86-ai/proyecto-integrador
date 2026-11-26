# Registro de contribuciones individuales y proceso de desarrollo — Proyecto Integrador

**Autora:** Solange Areco (`Sol`, GitHub `solareco86-ai`)
**Proyecto:** Portal Institucional del ISFT N.º 199
**Repositorio:** `solareco86-ai/proyecto-integrador`
**Fecha de elaboración:** 22 de noviembre de 2026

---

## 1. Introducción

Este documento registra, con evidencia verificable de Git y GitHub, las contribuciones individuales que realicé al Proyecto Integrador del ISFT N.º 199. Su objetivo es dejar constancia concreta de qué desarrollé, qué problema resolvía cada aporte, y cómo puede verificarse, cumpliendo con la indicación del profesor de anotar en la documentación "qué cambiaste, por qué y cómo se prueba, con enlaces a tus commits y PRs". El Proyecto Integrador es un trabajo colaborativo entre varios estudiantes; este informe distingue explícitamente mi trabajo individual del trabajo del resto del equipo, y mi rol de integración/administración del repositorio del trabajo de desarrollo propiamente dicho.

## 2. Participación individual

A lo largo del proyecto cumplí un doble rol: como desarrolladora, implementé el módulo de administración de contenidos institucionales (noticias, eventos y comunicados), desarrollando su estructura y funcionalidades; y como administradora del repositorio, participé en la integración de los aportes de mis compañeros hacia `develop` y de `develop` hacia `main` para su publicación. Este documento separa ambos roles para distinguir mi trabajo de desarrollo del trabajo colaborativo de integración.

## 3. Desarrollo del panel de administración de contenidos institucionales

**Objetivo:** dotar al sitio institucional de un panel de administración que permitiera gestionar noticias, eventos y comunicados institucionales sin intervención técnica directa.

**Problema que resolvía:** antes de este desarrollo, el sitio no tenía ninguna forma de publicar o actualizar noticias, eventos o comunicados institucionales de manera autónoma; cualquier contenido nuevo hubiera requerido un cambio de código.

**Funcionalidades desarrolladas** (integradas en conjunto en el [PR #2](https://github.com/solareco86-ai/proyecto-integrador/pull/2)):

- **Autenticación y panel de administración**, con contraseñas protegidas mediante `bcrypt` y control de sesión ([`628b226`](https://github.com/solareco86-ai/proyecto-integrador/commit/628b2265eac86de0d621ef4061f4c0416b9ccaed)).
- **Protección CSRF** propia para los formularios del panel, mediante token de sesión ([`3f3a84e`](https://github.com/solareco86-ai/proyecto-integrador/commit/3f3a84e5015b69507098b17a2e8b57691d603885)).
- **Gestión CRUD completa de noticias** (crear, editar, eliminar), con sus respectivas pantallas y validaciones ([`7303a5f`](https://github.com/solareco86-ai/proyecto-integrador/commit/7303a5f3a15767e84c190f3fbaa897fa53c51f4e), [`fc320a3`](https://github.com/solareco86-ai/proyecto-integrador/commit/fc320a39574329ef9503abdb28b7a315ae94c1e9)).
- **Gestión CRUD completa de eventos**, implementada en un único desarrollo integral ([`4ecdbe4`](https://github.com/solareco86-ai/proyecto-integrador/commit/4ecdbe46891df05168b7dcfa43d01480f4e16cc3)).
- **Gestión CRUD completa de comunicados**, en cuatro etapas sucesivas (listar, crear, editar, eliminar: [`e37d0cc`](https://github.com/solareco86-ai/proyecto-integrador/commit/e37d0cc0e1c7d19bb76fc9454290b87911e23149), [`d3386ea`](https://github.com/solareco86-ai/proyecto-integrador/commit/d3386ea89666ec638cc9be9bbe72766df6a17374), [`2b958b8`](https://github.com/solareco86-ai/proyecto-integrador/commit/2b958b8d9c02a1918fd48b53e73b239c1e1a1b9c), [`fdd7fba`](https://github.com/solareco86-ai/proyecto-integrador/commit/fdd7fba2acfb1075432bad9962216ecee8165ad1)).
- **URLs amigables (slugs)** para cada contenido publicado ([`9295433`](https://github.com/solareco86-ai/proyecto-integrador/commit/92954332c8669922698393d82777dd1eab9794e7)).
- **Estados de publicación**, para que un contenido pueda guardarse como borrador antes de hacerse público ([`f7cc048`](https://github.com/solareco86-ai/proyecto-integrador/commit/f7cc048b746f13cf797cef9923a86d763c221dc8)).
- **Páginas públicas** de listado y detalle para que cualquier visitante consulte las noticias, eventos y comunicados publicados ([`c85e65b`](https://github.com/solareco86-ai/proyecto-integrador/commit/c85e65bff0fffe0d6025e24723658d8b3697e614), [`84ead55`](https://github.com/solareco86-ai/proyecto-integrador/commit/84ead55afad10de55f70fbc58b21073e2a8095a3), [`c6150b7`](https://github.com/solareco86-ai/proyecto-integrador/commit/c6150b7e2e72fbc07f20286940d91b91467753b0)).

**Decisiones y aspectos técnicos relevantes:** implementé un esquema uniforme para las operaciones de listar, crear, editar y eliminar en los tres tipos de contenido, manteniendo criterios comunes de protección CSRF, autorización y estructura de casos de uso. Esto permitió mantener una organización consistente entre las funcionalidades desarrolladas.

**Evidencias de GitHub:** el conjunto completo se integró a `develop` mediante el [PR #2](https://github.com/solareco86-ai/proyecto-integrador/pull/2) ("feat(panel): integrar Panel de Autoridades en develop"). El nombre histórico del PR se conserva como referencia de GitHub; el módulo desarrollado corresponde al panel de administración de contenidos institucionales (noticias, eventos y comunicados). El PR reúne los commits correspondientes al desarrollo del módulo y constituye la evidencia principal de su integración en `develop`.

## 4. Validaciones del formulario de consultas

**Problema inicial:** el formulario de contacto del sitio podía enviarse sin que ningún campo relevante fuera obligatorio, lo que permitía recibir consultas vacías o sin ningún dato de contacto utilizable.

**Solución implementada** (commit [`e780b24`](https://github.com/solareco86-ai/proyecto-integrador/commit/e780b246766f8f3d39e487740a258dcd35a4f1a9)):

- **Backend:** incorporé un validador (`@model_validator`) que exige al menos un medio de contacto — email o teléfono — antes de aceptar la consulta.
- **Frontend:** marqué como obligatorios el nombre y apellido (`contacto-nombre`), la carrera de interés (`contacto-servicio`) y la situación de estudios secundarios (`contacto-tarifa`). Email y teléfono quedan individualmente opcionales, porque la regla exige uno de los dos, no ambos. El campo de comentario, en cambio, pasó a ser opcional, ya que no es un dato indispensable para procesar la consulta.

**Pruebas y evidencia:** el archivo `tests/test_contact_form_validation.py` fue incorporado en este mismo commit y contempla distintos escenarios de validación, incluyendo campos ausentes, email sin teléfono, teléfono sin email y ausencia de ambos medios de contacto. Verifiqué que estas reglas siguen exactamente vigentes en `main` a la fecha de este informe.

## 5. Gestión de imágenes institucionales

**Funcionalidad:** permití que, al crear o editar una noticia, evento o comunicado, se pudiera adjuntar una imagen, con un mecanismo de almacenamiento propio (commit [`eeaa143`](https://github.com/solareco86-ai/proyecto-integrador/commit/eeaa143a5c43ad490635be9b36798a9314ff2123)).

**Validaciones y aspectos técnicos:** en lugar de confiar en la extensión del archivo declarada por quien lo sube, la implementación re-verifica el formato real del archivo con la librería Pillow, y reduce el riesgo de manipulación de rutas, ya que el nombre almacenado se genera mediante un identificador único (UUID) en lugar de utilizar directamente el nombre proporcionado por el usuario.

**Evidencias:** `tests/test_local_image_storage_gateway.py` y los tests específicos de imágenes de cada módulo (noticias, eventos, comunicados) cubren estos casos.

## 6. Mejoras complementarias

Además del desarrollo principal, realicé una serie de ajustes menores de contenido, diseño y operación:

- Reemplacé el favicon genérico por el logo real del instituto ([`95dad24`](https://github.com/solareco86-ai/proyecto-integrador/commit/95dad240290c33c8abba2bdd3a44138b698de5d6)).
- Reorganicé la estructura de la página de inicio ([`a90289b`](https://github.com/solareco86-ai/proyecto-integrador/commit/a90289b83ea06eed577e9a0109b55fe605d034d5)) y ajusté el bloque de hero y el flujo de preinscripción ([`0863873`](https://github.com/solareco86-ai/proyecto-integrador/commit/0863873427a309b7fbf18cb5fa2c8e7d64e9648c)).
- Unifiqué la identidad visual del sitio y corregí el comportamiento del menú en dispositivos móviles ([`f840670`](https://github.com/solareco86-ai/proyecto-integrador/commit/f8406707525d5fbea9d4902d6feef93e9a806938)).
- Corregí textos y datos de contacto institucionales para que reflejaran la información real ([`80dc0ca`](https://github.com/solareco86-ai/proyecto-integrador/commit/80dc0ca9ba07c2d2033ba24449e1b7fed84bf83a)).
- Mejoré la robustez del arranque de la aplicación ante un archivo de versión vacío o dañado, con su test correspondiente ([`55c74e9`](https://github.com/solareco86-ai/proyecto-integrador/commit/55c74e960bdd2f577d653a01adefd807d488e6df)).
- Mejoré la robustez del script de despliegue para que no abortara el rollback ante directorios sin permisos de escritura ([`8fdcef4`](https://github.com/solareco86-ai/proyecto-integrador/commit/8fdcef45a643b001223ba7b47ea9902337d6c233)).

Algunos de estos ajustes de diseño (la portada y el encabezado) fueron retomados y ampliados más adelante por otros integrantes del equipo; mi aporte corresponde a la versión original de cada uno de estos cambios, no a su estado final.

## 7. Pruebas y verificaciones

Las funcionalidades desarrolladas cuentan con pruebas automatizadas específicas: autenticación y sesión del panel, protección CSRF, los tres CRUD de contenidos (noticias, eventos, comunicados), slugs, estados de publicación, páginas públicas, gestión de imágenes, y las validaciones del formulario de contacto. Estas pruebas forman parte de la suite del proyecto y contribuyen al proceso de validación de las funcionalidades implementadas. No consigno aquí porcentajes de cobertura ni resultados de ejecución puntuales, ya que esos valores varían según el estado del repositorio en cada momento y corresponden a una verificación del proyecto en su conjunto, no a mi aporte individual.

## 8. Proceso de trabajo con Git y GitHub

Mi flujo de trabajo siguió el esquema acordado para el proyecto: desarrollo en una rama propia, commits organizados por funcionalidad (cada commit del módulo institucional corresponde a una etapa concreta del CRUD o a una funcionalidad específica, antes que a cambios mezclados), y la integración del trabajo completo del módulo hacia `develop` mediante el Pull Request #2. Las validaciones del formulario de contacto, en cambio, se incorporaron mediante un commit puntual y acotado. Además de mi rol como desarrolladora, participé en tareas de administración y coordinación del repositorio, revisando y fusionando Pull Requests de otros compañeros hacia `develop` y realizando, en distintas ocasiones, la integración de `develop` hacia `main` para la publicación de cambios en producción.

## 9. Participación en releases e integración

Participé en la integración y publicación de los siguientes releases: [`57f5887`](https://github.com/solareco86-ai/proyecto-integrador/commit/57f588778c39ac5d3fb86186728bfbd91b99b6d9), [`030b4cb`](https://github.com/solareco86-ai/proyecto-integrador/commit/030b4cb3b16d25c7f9d01c865e48c605b6d196ff), [`52ce46d`](https://github.com/solareco86-ai/proyecto-integrador/commit/52ce46d69fe969bfcbd3b980a1d8d9159dc705ad), [`70b759c`](https://github.com/solareco86-ai/proyecto-integrador/commit/70b759c0632f98002544a5bc22869e891bc39472) y el [PR #85](https://github.com/solareco86-ai/proyecto-integrador/pull/85).

En el release identificado con `030b4cb` se integraron cambios de mi autoría. Mi participación en los demás releases estuvo principalmente vinculada a tareas de integración y publicación, sin atribuirme la autoría del código desarrollado por otros integrantes del equipo.

## 10. Evidencias

**Pull Requests:**
- [PR #2](https://github.com/solareco86-ai/proyecto-integrador/pull/2) — Desarrollo del panel de administración de contenidos institucionales.
- [PR #85](https://github.com/solareco86-ai/proyecto-integrador/pull/85) — Release develop → main.

**Commits principales:**
- Panel de administración: [`628b226`](https://github.com/solareco86-ai/proyecto-integrador/commit/628b2265eac86de0d621ef4061f4c0416b9ccaed), [`3f3a84e`](https://github.com/solareco86-ai/proyecto-integrador/commit/3f3a84e5015b69507098b17a2e8b57691d603885), [`7303a5f`](https://github.com/solareco86-ai/proyecto-integrador/commit/7303a5f3a15767e84c190f3fbaa897fa53c51f4e), [`fc320a3`](https://github.com/solareco86-ai/proyecto-integrador/commit/fc320a39574329ef9503abdb28b7a315ae94c1e9), [`4ecdbe4`](https://github.com/solareco86-ai/proyecto-integrador/commit/4ecdbe46891df05168b7dcfa43d01480f4e16cc3), [`e37d0cc`](https://github.com/solareco86-ai/proyecto-integrador/commit/e37d0cc0e1c7d19bb76fc9454290b87911e23149), [`d3386ea`](https://github.com/solareco86-ai/proyecto-integrador/commit/d3386ea89666ec638cc9be9bbe72766df6a17374), [`2b958b8`](https://github.com/solareco86-ai/proyecto-integrador/commit/2b958b8d9c02a1918fd48b53e73b239c1e1a1b9c), [`fdd7fba`](https://github.com/solareco86-ai/proyecto-integrador/commit/fdd7fba2acfb1075432bad9962216ecee8165ad1), [`9295433`](https://github.com/solareco86-ai/proyecto-integrador/commit/92954332c8669922698393d82777dd1eab9794e7), [`f7cc048`](https://github.com/solareco86-ai/proyecto-integrador/commit/f7cc048b746f13cf797cef9923a86d763c221dc8), [`c85e65b`](https://github.com/solareco86-ai/proyecto-integrador/commit/c85e65bff0fffe0d6025e24723658d8b3697e614), [`84ead55`](https://github.com/solareco86-ai/proyecto-integrador/commit/84ead55afad10de55f70fbc58b21073e2a8095a3), [`c6150b7`](https://github.com/solareco86-ai/proyecto-integrador/commit/c6150b7e2e72fbc07f20286940d91b91467753b0), [`eeaa143`](https://github.com/solareco86-ai/proyecto-integrador/commit/eeaa143a5c43ad490635be9b36798a9314ff2123).
- Validaciones de contacto: [`e780b24`](https://github.com/solareco86-ai/proyecto-integrador/commit/e780b246766f8f3d39e487740a258dcd35a4f1a9).
- Mejoras complementarias: [`95dad24`](https://github.com/solareco86-ai/proyecto-integrador/commit/95dad240290c33c8abba2bdd3a44138b698de5d6), [`a90289b`](https://github.com/solareco86-ai/proyecto-integrador/commit/a90289b83ea06eed577e9a0109b55fe605d034d5), [`0863873`](https://github.com/solareco86-ai/proyecto-integrador/commit/0863873427a309b7fbf18cb5fa2c8e7d64e9648c), [`f840670`](https://github.com/solareco86-ai/proyecto-integrador/commit/f8406707525d5fbea9d4902d6feef93e9a806938), [`80dc0ca`](https://github.com/solareco86-ai/proyecto-integrador/commit/80dc0ca9ba07c2d2033ba24449e1b7fed84bf83a), [`55c74e9`](https://github.com/solareco86-ai/proyecto-integrador/commit/55c74e960bdd2f577d653a01adefd807d488e6df), [`8fdcef4`](https://github.com/solareco86-ai/proyecto-integrador/commit/8fdcef45a643b001223ba7b47ea9902337d6c233).
- Releases: [`57f5887`](https://github.com/solareco86-ai/proyecto-integrador/commit/57f588778c39ac5d3fb86186728bfbd91b99b6d9), [`030b4cb`](https://github.com/solareco86-ai/proyecto-integrador/commit/030b4cb3b16d25c7f9d01c865e48c605b6d196ff), [`52ce46d`](https://github.com/solareco86-ai/proyecto-integrador/commit/52ce46d69fe969bfcbd3b980a1d8d9159dc705ad), [`70b759c`](https://github.com/solareco86-ai/proyecto-integrador/commit/70b759c0632f98002544a5bc22869e891bc39472).

## 11. Conclusión

El desarrollo del panel de administración de contenidos institucionales fue mi primer trabajo de diseño de un flujo CRUD completo de principio a fin, con autenticación, protección contra CSRF y gestión segura de archivos subidos por usuarios — decisiones técnicas que debí investigar y justificar, no solo implementar. Las validaciones del formulario de contacto me permitieron trabajar específicamente el problema de garantizar datos mínimos utilizables sin sobrecargar al usuario con campos innecesarios. Además, asumir la administración del repositorio me dio una perspectiva distinta del trabajo en equipo: coordinar la integración del trabajo de varios compañeros exige criterios de revisión y responsabilidad que complementan, pero no reemplazan, el trabajo de desarrollo individual documentado en este informe.
