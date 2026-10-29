from cursos import curso_fundamentos_programacion

# Asegurate de incluirlo en la lista de cursos disponibles
LISTA_CURSOS = [
    # ... otros cursos existentes ...
    curso_fundamentos_programacion,
]

if __name__ == "__main__":
    print(f"Cursos disponibles ({len(LISTA_CURSOS)}):")
    for curso in LISTA_CURSOS:
        print(f"- {curso['titulo']} ({curso['nivel']}): {curso['duracion']}")
