import os

# Archivos
ARCHIVO_ESTUDIANTES = "estudiantes.txt"
ARCHIVO_ASIGNACIONES = "asignaciones.txt"
ARCHIVO_NOTAS = "notas.txt"

# Lista de materias
MATERIAS = [
    "Elementos de álgebra y geometría",
    "Fundamentos de informática",
    "Pensamiento crítico y comunicación",
    "Sistemas de información 1",
    "Teoría de sistemas",
    "Arquitectura de computadores",
    "Fundamentos de química",
    "Matemática discreta",
    "Programación 1",
    "Sistemas de representación",
    "Álgebra",
    "Cálculo 1",
    "Física 1",
    "Programación 2",
    "Sistemas de información 2",
    "Sistemas operativos",
    "Cálculo 2",
    "Fundamentos de telecomunicaciones",
    "Ingeniería de datos 1",
    "Paradigma orientado a objetos",
    "Programación 3",
    "Ingeniería de datos 2",
    "Probabilidad y estadística",
    "Proceso de desarrollo de software",
    "Teleinformática y redes",
    "Aplicaciones interactivas",
    "Estadística avanzada",
    "Física 2",
    "Ingeniería de software",
    "Teoría de la computación",
    "Ciencia de datos",
    "Desarrollo de aplicaciones 1",
    "Dirección de proyectos informáticos",
    "Modelado y simulación",
    "Desarrollo de aplicaciones 2",
    "Inteligencia artificial",
    "Evolución de proyectos informáticos",
    "Tecnología y medio ambiente",
    "Arquitectura de aplicaciones",
    "Calidad de software",
    "Tendencias tecnológicas",
    "Derecho informático",
    "Negocios tecnológicos",
    "Tecnología e innovación",
    "Proyecto final ingeniería informática",
]

# Validacion del DNI
def validar_dni(dni):
    return dni.isdigit() and len(dni) == 8 and 10000000 <= int(dni) <= 99999999

# Validación del nombre y apellido
def validar_nombre_apellido(valor):
    return valor.isalpha() and len(valor.strip()) > 0

# Ingreso de DNI recursivo
def ingresar_dni():
    dni = input("Ingrese el DNI del estudiante (o presione Enter para salir): ").strip()
    if dni == "":
        return None  # Indica que el usuario desea salir
    if not validar_dni(dni):
        print("DNI inválido. Debe tener 8 dígitos y estar entre 10000000 y 99999999.")
        return ingresar_dni()  # Reintentar
    return dni


# Validacion de notas
def validar_nota(nota):
    try:
        nota = int(nota)
        return 1 <= nota <= 10
    except ValueError:
        return False


# Función para abrir archivos
def abrir_archivo(nombre, modo):
    try:
        return open(nombre, modo)
    except FileNotFoundError:
        print(f"Error: El archivo {nombre} no existe.")
        return None
    except OSError as mensaje:
        print(f"Error al abrir el archivo {nombre}: {mensaje}")
        return None


# Carga del archivo de estudiantes
def cargar_estudiantes():
    if not os.path.exists(ARCHIVO_ESTUDIANTES):
        return []
    with open(ARCHIVO_ESTUDIANTES, "r") as archivo:
        return [linea.strip().split(";") for linea in archivo if linea.strip()]

# Función para agregar estudiantes
def agregar_estudiante():
    estudiantes = cargar_estudiantes()  # Cargar estudiantes existentes
    archivo = abrir_archivo(ARCHIVO_ESTUDIANTES, "a")
    if not archivo:
        return
    try:
        while True:
            dni = ingresar_dni()
            if dni is None:  # Usuario presionó Enter para salir
                print("Finalizando ingreso de estudiantes.")
                break

            # Verificar duplicados solo por DNI
            if any(estudiante[0] == dni for estudiante in estudiantes):
                print("Este DNI ya está registrado. Intente con otro.")
                continue

            nombre = input("Ingrese el nombre: ").strip()
            while not validar_nombre_apellido(nombre):
                print("Nombre inválido. Debe contener solo letras y no estar vacío.")
                nombre = input("Ingrese el nombre: ").strip()

            apellido = input("Ingrese el apellido: ").strip()
            while not validar_nombre_apellido(apellido):
                print("Apellido inválido. Debe contener solo letras y no estar vacío.")
                apellido = input("Ingrese el apellido: ").strip()

            # Agregar estudiante al archivo y a la lista en memoria
            archivo.write(f"{dni};{nombre};{apellido}\n")
            estudiantes.append([dni, nombre, apellido])
            print("Estudiante agregado.")
    finally:
        try:
            archivo.close()
        except NameError:
            pass

# Funcion para mostrar estudinates 
def mostrar_estudiantes():
    archivo = abrir_archivo(ARCHIVO_ESTUDIANTES, "r")
    if not archivo:
        return
    try:
        print("Estudiantes registrados:")
        for linea in archivo:
            dni, nombre, apellido = linea.strip().split(";")
            print(f"DNI: {dni}, Nombre: {nombre}, Apellido: {apellido}")
    finally:
        try:
            archivo.close()
        except NameError:
            pass

# Funcion para mostrar materias
def mostrar_materias():
    print("Lista de materias disponibles:")
    i = 1  
    for materia in MATERIAS:
        print(f"{i}. {materia}")
        i += 1  

# Funcion para asignar materias
def asignar_materia():
    archivo_asignaciones = abrir_archivo(ARCHIVO_ASIGNACIONES, "a")
    archivo_estudiantes = abrir_archivo(ARCHIVO_ESTUDIANTES, "r")
    if not archivo_asignaciones or not archivo_estudiantes:
        return
    try:
        estudiantes = {linea.split(";")[0]: linea.strip() for linea in archivo_estudiantes}
        if not estudiantes:
            print("No hay estudiantes registrados.")
            return

        dni = input("Ingrese el DNI del estudiante: ").strip()
        if not validar_dni(dni) or dni not in estudiantes:
            print("Estudiante no encontrado o DNI inválido.")
            return

        mostrar_materias()
        while True:
            try:
                seleccion = int(input("Seleccione el número de la materia: "))
                if 1 <= seleccion <= len(MATERIAS):
                    materia = MATERIAS[seleccion - 1]
                    break
                else:
                    print("Número inválido. Intente nuevamente.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

        archivo_asignaciones.write(f"{dni};{materia}\n")
        print(f"Materia '{materia}' asignada al estudiante con DNI {dni}.")
    finally:
        try:
            archivo_asignaciones.close()
            archivo_estudiantes.close()
        except NameError:
            pass

# Funcion para mostrar asignaciones
def mostrar_asignaciones():
    archivo_asignaciones = abrir_archivo(ARCHIVO_ASIGNACIONES, "r")
    archivo_estudiantes = abrir_archivo(ARCHIVO_ESTUDIANTES, "r")
    if not archivo_asignaciones or not archivo_estudiantes:
        return
    try:
        estudiantes = {linea.split(";")[0]: linea.strip().split(";")[1:] for linea in archivo_estudiantes}
        print("Asignaciones de materias:")
        for linea in archivo_asignaciones:
            dni, materia = linea.strip().split(";")
            if dni in estudiantes:
                nombre, apellido = estudiantes[dni]
                print(f"DNI: {dni}, Nombre: {nombre}, Apellido: {apellido}, Materia: {materia}")
            else:
                print(f"DNI: {dni}, Materia: {materia} (Estudiante no encontrado)")
    finally:
        try:
            archivo_asignaciones.close()
            archivo_estudiantes.close()
        except NameError:
            pass

# Nueva funcion para cargar o modificar notas
def cargar_notas():
    archivo_notas = abrir_archivo(ARCHIVO_NOTAS, "r+")
    archivo_asignaciones = abrir_archivo(ARCHIVO_ASIGNACIONES, "r")
    if not archivo_notas or not archivo_asignaciones:
        return

    try:
        asignaciones = {}
        for linea in archivo_asignaciones:
            dni, materia = linea.strip().split(";")
            if dni in asignaciones:
                asignaciones[dni].append(materia)
            else:
                asignaciones[dni] = [materia]

        dni = input("Ingrese el DNI del estudiante: ").strip()
        if not validar_dni(dni) or dni not in asignaciones:
            print("Estudiante no encontrado o no tiene materias asignadas.")
            return

        print("Materias asignadas:")
        index = 1  # Contador manual
        for materia in asignaciones[dni]:
            print(f"{index}. {materia}")
            index += 1  # Incrementar el índice

        while True:
            try:
                seleccion = int(input("Seleccione el número de la materia para cargar notas: "))
                if 1 <= seleccion <= len(asignaciones[dni]):
                    materia = asignaciones[dni][seleccion - 1]
                    break
                else:
                    print("Número inválido. Intente nuevamente.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

        # Leer las notas existentes de la materia, si las hay
        archivo_notas.seek(0)  # Regresar al inicio del archivo
        notas_existentes = {}
        for linea in archivo_notas:
            linea = linea.strip().split(";")
            if len(linea) >= 7:
                dni_nota, materia_nota = linea[0], linea[1]
                if dni_nota == dni and materia_nota == materia:
                    notas_existentes[materia] = linea[2:]  # Guardamos las notas

        # Verificar si ya existen notas
        if materia in notas_existentes:
            print("Notas actuales para esta materia:")
            print(f"Notas: {notas_existentes[materia][:2]}")  # Mostrar solo las primeras dos notas

            modificar = input("¿Desea modificar las notas? (s/n): ").strip().lower()
            if modificar != 's':
                print("Se mantendrán las notas actuales.")
                return  # Si no se modifican, salimos

        # Si no existen notas o se desea modificarlas, pedir las nuevas
        print(f"Materia seleccionada: {materia}")
        notas = []
        for i in range(1, 3):
            while True:
                nota = input(f"Ingrese la Nota {i} (entre 1 y 10): ").strip()
                if validar_nota(nota):
                    notas.append(int(nota))
                    break
                print("Nota inválida. Intente nuevamente.")

        recuperatorio = ""
        if any(nota < 4 for nota in notas):
            while True:
                nota = input("Ingrese el Recuperatorio (entre 1 y 10): ").strip()
                if validar_nota(nota):
                    recuperatorio = int(nota)
                    break
                print("Nota inválida. Intente nuevamente.")

        notas_validas = notas + ([recuperatorio] if recuperatorio else [])
        aprobadas = sum(1 for nota in notas_validas if nota >= 4)

        if aprobadas >= 2:
            cursada = "Aprobado"
            while True:
                nota_final = input("Ingrese la Nota final (entre 1 y 10): ").strip()
                if validar_nota(nota_final):
                    notas.append(int(nota_final))
                    break
                print("Nota inválida. Intente nuevamente.")
        else:
            cursada = "Recursa"
            nota_final = ""

        # Reabrir archivo de notas para actualizar
        archivo_notas.seek(0)
        lineas = archivo_notas.readlines()
        archivo_notas.close()

        # Filtrar la materia actualizada
        with open(ARCHIVO_NOTAS, "w") as archivo:
            for linea in lineas:
                if linea.strip().split(";")[0] != dni or linea.strip().split(";")[1] != materia:
                    archivo.write(linea)

            # Guardar las nuevas notas
            archivo.write(f"{dni};{materia};{notas[0]};{notas[1]};{recuperatorio};{cursada};{nota_final}\n")

        print("Notas cargadas/modificadas exitosamente.")
    finally:
        try:
            archivo_asignaciones.close()
        except NameError:
            pass

# Función para mostrar notas
def mostrar_notas():
    archivo_notas = abrir_archivo(ARCHIVO_NOTAS, "r")
    archivo_estudiantes = abrir_archivo(ARCHIVO_ESTUDIANTES, "r")
    archivo_asignaciones = abrir_archivo(ARCHIVO_ASIGNACIONES, "r")
    if not archivo_notas or not archivo_estudiantes or not archivo_asignaciones:
        return

    try:
        # Crear diccionarios de estudiantes y asignaciones
        estudiantes = {linea.split(";")[0]: linea.strip().split(";")[1:] for linea in archivo_estudiantes}
        asignaciones = {}
        for linea in archivo_asignaciones:
            dni, materia = linea.strip().split(";")
            if dni in asignaciones:
                asignaciones[dni].append(materia)
            else:
                asignaciones[dni] = [materia]

        # Solicitar DNI del estudiante
        dni = input("Ingrese el DNI del estudiante para ver sus notas: ").strip()
        if not validar_dni(dni) or dni not in estudiantes:
            print("Estudiante no encontrado o no tiene materias asignadas.")
            return

        nombre, apellido = estudiantes[dni]
        if dni not in asignaciones:
            print(f"El estudiante {nombre} {apellido} no tiene materias asignadas.")
            return

        # Mostrar materias asignadas al estudiante
        print(f"Materias asignadas al estudiante {nombre} {apellido}:")
        contador = 1
        for materia in asignaciones[dni]:
            print(f"{contador}. {materia}")
            contador += 1

        # Seleccionar una materia
        while True:
            try:
                seleccion = int(input("Seleccione el número de la materia para ver las notas: "))
                if 1 <= seleccion <= len(asignaciones[dni]):
                    materia_seleccionada = asignaciones[dni][seleccion - 1]
                    break
                else:
                    print("Número inválido. Intente nuevamente.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

        # Buscar y mostrar las notas de la materia seleccionada
        encontrado = False
        for linea in archivo_notas:
            datos = linea.strip().split(";")
            if datos[0] == dni and datos[1] == materia_seleccionada:
                print(f"\nNotas para {nombre} {apellido} en '{materia_seleccionada}':")
                print(f"Nota 1: {datos[2]}")
                print(f"Nota 2: {datos[3]}")
                print(f"Recuperatorio: {datos[4]}" if datos[4] else "Recuperatorio: No requerido")
                print(f"Estado de cursada: {datos[5]}")
                print(f"Nota final: {datos[6]}" if datos[6] else "Nota final: No cargada")
                encontrado = True
                break

        if not encontrado:
            print(f"No se encontraron notas para la materia '{materia_seleccionada}' del estudiante {nombre} {apellido}.")
    finally:
        # Cerrar archivos
        try:
            archivo_notas.close()
            archivo_estudiantes.close()
            archivo_asignaciones.close()
        except NameError:
            pass

# Menú principal
def menu_principal():
    opciones = {
        "1": agregar_estudiante,
        "2": mostrar_estudiantes,
        "3": mostrar_materias,
        "4": asignar_materia,
        "5": mostrar_asignaciones,
        "6": cargar_notas,
        "7": mostrar_notas,
        "8": salir_del_sistema
    }

    while True:
        print("\n=== Menú Principal ===")
        print("1. Agregar estudiante")
        print("2. Mostrar estudiantes")
        print("3. Mostrar materias")
        print("4. Asignar materia a estudiante")
        print("5. Mostrar asignaciones")
        print("6. Cargar notas")
        print("7. Mostrar notas")
        print("8. Salir")

        opcion = input("Seleccione una opción: ").strip()
        if opcion in opciones:
            opciones[opcion]()
        else:
            print("Opción no válida. Por favor, intente nuevamente.")

def salir_del_sistema():
    print("Saliendo del sistema. ¡Hasta luego!")
    exit()

# Llamada a la función para ejecutar el menú
if __name__ == "__main__":
    menu_principal()
