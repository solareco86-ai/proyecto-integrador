#!/bin/bash
# Pruebas de regresión para los bloques de scripts/deploy-server.sh marcados
# con BEGIN_PERM_CHECK/END_PERM_CHECK y BEGIN_ROLLBACK/END_ROLLBACK.
#
# Extrae esos bloques TEXTUALMENTE del script real (no una copia mantenida a
# mano) y los ejecuta contra un repositorio git temporal y descartable, para
# detectar si algún cambio futuro vuelve a romper estos dos casos.
#
# Requiere semántica POSIX real de permisos (chmod sobre bits de usuario): está
# pensado para correr en Linux (CI o VPS), no en Windows. No toca el VPS real
# ni ningún repositorio del proyecto: todo ocurre en un directorio temporal
# bajo mktemp, eliminado al finalizar.
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_SCRIPT="$SCRIPT_DIR/deploy-server.sh"
FALLOS=0

extraer_bloque() {
    # extraer_bloque INICIO FIN ARCHIVO
    # Normaliza CRLF por si el archivo fue checkeado con core.autocrlf=true en
    # Windows: el blob de git es LF, pero el working tree local puede no serlo.
    sed -n "/$1/,/$2/p" "$3" | sed '1d;$d' | sed 's/\r$//'
}

assert_igual() {
    local descripcion="$1" esperado="$2" obtenido="$3"
    if [ "$esperado" = "$obtenido" ]; then
        echo "  OK: $descripcion"
    else
        echo "  FALLO: $descripcion (esperado='$esperado' obtenido='$obtenido')"
        FALLOS=$((FALLOS + 1))
    fi
}

assert_rc() {
    local descripcion="$1" esperado="$2" obtenido="$3"
    if [ "$esperado" -eq "$obtenido" ]; then
        echo "  OK: $descripcion (exit=$obtenido)"
    else
        echo "  FALLO: $descripcion (esperado exit=$esperado, obtenido=$obtenido)"
        FALLOS=$((FALLOS + 1))
    fi
}

preparar_repo() {
    local dir="$1"
    rm -rf "$dir"
    mkdir -p "$dir"
    (
        cd "$dir"
        git init -q -b main
        git config user.email test@test.com
        git config user.name Test
        echo "v1" > existente.py
        mkdir sub_existente
        echo "v1" > sub_existente/archivo.py
        git add -A
        git commit -q -m "v1"
    )
}

echo "=== Caso 1: todo escribible -> el chequeo no debe detectar nada ==="
TMP1="$(mktemp -d)"
preparar_repo "$TMP1"
(
    cd "$TMP1"
    PERM_CHECK="$(extraer_bloque BEGIN_PERM_CHECK END_PERM_CHECK "$DEPLOY_SCRIPT")"
    eval "$PERM_CHECK"
    echo "NOT_WRITABLE='$NOT_WRITABLE'"
)
RESULTADO="$(cd "$TMP1" && PERM_CHECK="$(extraer_bloque BEGIN_PERM_CHECK END_PERM_CHECK "$DEPLOY_SCRIPT")"; eval "$PERM_CHECK"; echo "$NOT_WRITABLE")"
assert_igual "caso base sin bloqueos" "" "$RESULTADO"
rm -rf "$TMP1"

echo
echo "=== Caso 2 (Problema 1): directorio EXISTENTE sin permiso de escritura ==="
echo "    (sus archivos internos SI son escribibles; solo el directorio no lo es)"
TMP2="$(mktemp -d)"
preparar_repo "$TMP2"
chmod a-w "$TMP2/sub_existente"
RESULTADO="$(cd "$TMP2" && PERM_CHECK="$(extraer_bloque BEGIN_PERM_CHECK END_PERM_CHECK "$DEPLOY_SCRIPT")"; eval "$PERM_CHECK"; echo "$NOT_WRITABLE")"
assert_igual "detecta el directorio no escribible" "sub_existente/" "$RESULTADO"
chmod u+w "$TMP2/sub_existente"
rm -rf "$TMP2"

echo
echo "=== Caso 2b: confirmar que, SIN el fix, este caso pasaba desapercibido ==="
echo "    (chequeo viejo: solo find .git + archivos + raiz + .build_commit)"
TMP2B="$(mktemp -d)"
preparar_repo "$TMP2B"
chmod a-w "$TMP2B/sub_existente"
RESULTADO_VIEJO="$(cd "$TMP2B" && {
    NOT_WRITABLE=$({
        find .git -maxdepth 2 ! -writable 2>/dev/null
        git ls-files | while IFS= read -r f; do [ -e "$f" ] && [ ! -w "$f" ] && echo "$f"; done
        [ -w . ] || echo "."
        [ -e .build_commit ] && [ ! -w .build_commit ] && echo ".build_commit"
    } | head -1)
    echo "$NOT_WRITABLE"
})"
assert_igual "logica ANTERIOR no detectaba este caso (regresion que motiva este fix)" "" "$RESULTADO_VIEJO"
chmod u+w "$TMP2B/sub_existente"
rm -rf "$TMP2B"

echo
echo "=== Caso 3 (Problema 1): archivo nuevo del commit remoto, en directorio EXISTENTE y escribible ==="
TMP3="$(mktemp -d)"
preparar_repo "$TMP3"
(
    cd "$TMP3"
    echo "nuevo" > sub_existente/archivo_nuevo.py
    mkdir sub_nueva
    echo "nuevo" > sub_nueva/archivo.py
    git add -A
    git commit -q -m "v2: agrega archivo y directorio nuevos"
)
RESULTADO="$(cd "$TMP3" && PERM_CHECK="$(extraer_bloque BEGIN_PERM_CHECK END_PERM_CHECK "$DEPLOY_SCRIPT")"; eval "$PERM_CHECK"; echo "$NOT_WRITABLE")"
assert_igual "sin bloqueos, no detecta falsos positivos con archivos/directorios nuevos ya aplicados" "" "$RESULTADO"
(cd "$TMP3" && git reset --hard HEAD~1 -q >/dev/null 2>&1)
RC_RESET=$?
assert_rc "el reset --hard real tambien funciona sin bloqueos" 0 "$RC_RESET"
rm -rf "$TMP3"

echo
echo "=== Caso 4 (Problema 1, residual documentado): directorio NUEVO cuyo padre"
echo "    (tambien nuevo, sin archivos rastreados todavia) no es escribible."
echo "    Limitacion conocida: el chequeo NO puede detectar esto porque, antes"
echo "    del fetch, ese directorio ni existe ni esta rastreado localmente."
TMP4="$(mktemp -d)"
preparar_repo "$TMP4"
RESULTADO="$(cd "$TMP4" && PERM_CHECK="$(extraer_bloque BEGIN_PERM_CHECK END_PERM_CHECK "$DEPLOY_SCRIPT")"; eval "$PERM_CHECK"; echo "$NOT_WRITABLE")"
assert_igual "limitacion conocida: no detecta un directorio padre nuevo aun no existente" "" "$RESULTADO"
echo "  (documentado en el PR: este caso requeriria fetch-then-diff, fuera de alcance de este fix)"
rm -rf "$TMP4"

echo
echo "=== Caso 5 (Problema 2): rollback con .build_commit NO escribible debe seguir restaurando ==="
TMP5="$(mktemp -d)"
preparar_repo "$TMP5"
(
    cd "$TMP5"
    echo "v2" > existente.py
    git add -A
    git commit -q -m "v2 (version que se simula rota)"
    # shellcheck disable=SC2034  # usada por el bloque ROLLBACK extraido y eval'ado mas abajo
    PREVIOUS_COMMIT="$(git rev-parse HEAD~1)"
    PREVIOUS_SHORT="$(git rev-parse --short HEAD~1)"
    echo "roto" > .build_commit
    chmod a-w .build_commit
    ROLLBACK="$(extraer_bloque BEGIN_ROLLBACK END_ROLLBACK "$DEPLOY_SCRIPT")"
    set +e
    eval "$ROLLBACK"
    RC=$?
    set -e
    chmod u+w .build_commit 2>/dev/null || true
    echo "HEAD_FINAL=$(git rev-parse --short HEAD)"
    echo "RC_ROLLBACK=$RC"
)
CONTENIDO_FINAL="$(cat "$TMP5/existente.py")"
assert_igual "el rollback restaura el contenido anterior (v1) aunque .build_commit no sea escribible" "v1" "$CONTENIDO_FINAL"
rm -rf "$TMP5"

echo
echo "=== Caso 5b: confirmar que, SIN el fix, set -e abortaba antes del reset del rollback ==="
TMP5B="$(mktemp -d)"
preparar_repo "$TMP5B"
(
    cd "$TMP5B"
    echo "v2" > existente.py
    git add -A
    git commit -q -m "v2 (version rota)"
    PREVIOUS_SHORT="v1simulado"
    chmod a-w .build_commit 2>/dev/null || true
    echo "roto" > .build_commit 2>/dev/null
    chmod a-w .build_commit
    set -e
    echo "$PREVIOUS_SHORT" > .build_commit
    git reset --hard HEAD~1
    echo "ESTA LINEA NO DEBERIA EJECUTARSE (demuestra el bug anterior)"
) 2>&1
RC_SIN_FIX=$?
assert_rc "logica ANTERIOR (sin fix) aborta con set -e antes del reset del rollback" 1 "$RC_SIN_FIX"
CONTENIDO_SIN_FIX="$(cat "$TMP5B/existente.py")"
assert_igual "logica ANTERIOR deja el codigo roto sin rollback (regresion que motiva este fix)" "v2" "$CONTENIDO_SIN_FIX"
chmod u+w "$TMP5B/.build_commit" 2>/dev/null || true
rm -rf "$TMP5B"

echo
if [ "$FALLOS" -eq 0 ]; then
    echo "TODAS LAS PRUEBAS PASARON (0 fallos)."
    exit 0
else
    echo "$FALLOS PRUEBA(S) FALLARON."
    exit 1
fi
