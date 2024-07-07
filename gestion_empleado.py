import json
from datetime import datetime


class Persona:
    def __init__(self, nombre, apellido, edad, dni, fecha_vinculacion):
        self._nombre = nombre
        self._apellido = apellido
        self._edad = edad
        self._dni = dni
        self._fecha_vinculacion = fecha_vinculacion

    def obtener_nombre_completo(self):
        return f"{self._nombre} {self._apellido}"

    def __str__(self):
        return f"{self.obtener_nombre_completo()}, Edad: {self._edad}, DNI: {self._dni}, Fecha de Vinculación: {self._fecha_vinculacion}"

    def to_dict(self):
        return {
            "nombre": self._nombre,
            "apellido": self._apellido,
            "edad": self._edad,
            "dni": self._dni,
            "fecha_vinculacion": self._fecha_vinculacion
        }

    @staticmethod
    def from_dict(data):
        return Persona(data["nombre"], data["apellido"], data["edad"], data["dni"], data["fecha_vinculacion"])


class Empleado(Persona):
    def __init__(self, nombre, apellido, edad, salario, dni, fecha_vinculacion):
        super().__init__(nombre, apellido, edad, dni, fecha_vinculacion)
        self._salario = salario

    def actualizar_salario(self, nuevo_salario):
        self._salario = nuevo_salario

    def __str__(self):
        return f"Empleado: {super().__str__()}, Salario: {self._salario}"

    def to_dict(self):
        data = super().to_dict()
        data["salario"] = self._salario
        return data

    @staticmethod
    def from_dict(data):
        return Empleado(data["nombre"], data["apellido"], data["edad"], data["salario"], data["dni"], data["fecha_vinculacion"])

    @staticmethod
    def guardar_empleados(empleados, filename):
        try:
            with open(filename, "w") as file:
                json.dump([empleado.to_dict() for empleado in empleados], file, indent=4)
        except IOError as e:
            print(f"Error guardando empleados: {e}")

    @staticmethod
    def cargar_empleados(filename):
        try:
            with open(filename, "r") as file:
                empleados_data = json.load(file)
                return [Empleado.from_dict(empleado_data) for empleado_data in empleados_data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error cargando empleados: {e}")
            return []

    @staticmethod
    def buscar_por_dni(empleados, dni):
        return next((empleado for empleado in empleados if empleado._dni == dni), None)


class Jefe(Empleado):
    def __init__(self, nombre, apellido, edad, salario, dni, fecha_vinculacion):
        super().__init__(nombre, apellido, edad, salario, dni, fecha_vinculacion)
        self._empleados_a_cargo = []

    def agregar_empleado(self, empleado):
        self._empleados_a_cargo.append(empleado)

    def obtener_empleados_a_cargo(self):
        return self._empleados_a_cargo

    def __str__(self):
        return f"Jefe: {super().__str__()}, Empleados a Cargo: {len(self._empleados_a_cargo)}"

    def to_dict(self):
        data = super().to_dict()
        data["empleados_a_cargo"] = [empleado.to_dict() for empleado in self._empleados_a_cargo]
        return data

    @staticmethod
    def from_dict(data):
        jefe = Jefe(data["nombre"], data["apellido"], data["edad"], data["salario"], data["dni"], data["fecha_vinculacion"])
        jefe._empleados_a_cargo = [Empleado.from_dict(empleado_data) for empleado_data in data["empleados_a_cargo"]]
        return jefe

    @staticmethod
    def guardar_jefes(jefes, filename):
        try:
            with open(filename, "w") as file:
                json.dump([jefe.to_dict() for jefe in jefes], file, indent=4)
        except IOError as e:
            print(f"Error guardando jefes: {e}")

    @staticmethod
    def cargar_jefes(filename, empleados):
        try:
            with open(filename, "r") as file:
                jefes_data = json.load(file)
                jefes = []
                for jefe_data in jefes_data:
                    jefe = Jefe.from_dict(jefe_data)
                    jefe._empleados_a_cargo = [next((e for e in empleados if e._dni == emp["dni"]), None) for emp in jefe_data["empleados_a_cargo"]]
                    jefes.append(jefe)
                return jefes
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error cargando jefes: {e}")
            return []


class Area:
    def __init__(self, nombre, descripcion):
        self._nombre = nombre
        self._descripcion = descripcion
        self._empleados = []

    def agregar_empleado(self, empleado):
        self._empleados.append(empleado)

    def obtener_empleados(self):
        return self._empleados

    def __str__(self):
        return f"Área: {self._nombre}, Descripción: {self._descripcion}, Cantidad de Empleados: {len(self._empleados)}"

    def to_dict(self):
        return {
            "nombre": self._nombre,
            "descripcion": self._descripcion,
            "empleados": [empleado.to_dict() for empleado in self._empleados]
        }

    @staticmethod
    def from_dict(data):
        area = Area(data["nombre"], data["descripcion"])
        area._empleados = [Empleado.from_dict(empleado_data) for empleado_data in data["empleados"]]
        return area

    @staticmethod
    def guardar_areas(areas, filename):
        try:
            with open(filename, "w") as file:
                json.dump([area.to_dict() for area in areas], file, indent=4)
        except IOError as e:
            print(f"Error guardando áreas: {e}")

    @staticmethod
    def cargar_areas(filename, empleados):
        try:
            with open(filename, "r") as file:
                areas_data = json.load(file)
                areas = []
                for area_data in areas_data:
                    area = Area.from_dict(area_data)
                    area._empleados = [next((e for e in empleados if e._dni == emp["dni"]), None) for emp in area_data["empleados"]]
                    areas.append(area)
                return areas
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error cargando áreas: {e}")
            return []


def menu_principal():
    print("Bienvenido al Sistema de Gestión de Empleados:")
    print("1. Gestionar Empleados")
    print("2. Gestionar Jefes")
    print("3. Gestionar Áreas")
    print("4. Salir")


def gestion_empleados(empleados):
    while True:
        print("\nGestión de Empleados:")
        print("1. Agregar Empleado")
        print("2. Buscar Empleado")
        print("3. Actualizar Salario de Empleado")
        print("4. Volver al Menú Principal")
        opcion = input("Ingrese el número de la opción que desea realizar: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del empleado: ")
            apellido = input("Ingrese el apellido del empleado: ")
            edad = int(input("Ingrese la edad del empleado: "))
            salario = float(input("Ingrese el salario del empleado: "))
            dni = input("Ingrese el DNI del empleado: ")
            fecha_vinculacion = input("Ingrese la fecha de vinculación (dd/mm/yyyy): ")
            try:
                datetime.strptime(fecha_vinculacion, "%d/%m/%Y")
            except ValueError:
                print("Fecha no válida. Debe tener el formato dd/mm/yyyy.")
                continue

            nuevo_empleado = Empleado(nombre, apellido, edad, salario, dni, fecha_vinculacion)
            empleados.append(nuevo_empleado)
            Empleado.guardar_empleados(empleados, "empleados.txt")
            print("Empleado agregado exitosamente.")

        elif opcion == "2":
            dni = input("Ingrese el DNI del empleado a buscar: ")
            empleado = Empleado.buscar_por_dni(empleados, dni)
            if empleado:
                print(empleado)
            else:
                print("No se encontró ningún empleado con ese DNI.")

        elif opcion == "3":
            dni = input("Ingrese el DNI del empleado cuyo salario desea actualizar: ")
            empleado = Empleado.buscar_por_dni(empleados, dni)
            if empleado:
                nuevo_salario = float(input(f"Ingrese el nuevo salario para {empleado.obtener_nombre_completo()}: "))
                empleado.actualizar_salario(nuevo_salario)
                Empleado.guardar_empleados(empleados, "empleados.txt")
                print("Salario actualizado exitosamente.")
            else:
                print("No se encontró ningún empleado con ese DNI.")

        elif opcion == "4":
            break

        else:
            print("Opción no válida. Intente nuevamente.")


def gestion_jefes(jefes, empleados):
    while True:
        print("\nGestión de Jefes:")
        print("1. Agregar Jefe")
        print("2. Ver Empleados a Cargo")
        print("3. Asignar Empleado a Cargo")
        print("4. Volver al Menú Principal")
        opcion = input("Ingrese el número de la opción que desea realizar: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del jefe: ")
            apellido = input("Ingrese el apellido del jefe: ")
            edad = int(input("Ingrese la edad del jefe: "))
            salario = float(input("Ingrese el salario del jefe: "))
            dni = input("Ingrese el DNI del jefe: ")
            fecha_vinculacion = input("Ingrese la fecha de vinculación (dd/mm/yyyy): ")
            try:
                datetime.strptime(fecha_vinculacion, "%d/%m/%Y")
            except ValueError:
                print("Fecha no válida. Debe tener el formato dd/mm/yyyy.")
                continue

            nuevo_jefe = Jefe(nombre, apellido, edad, salario, dni, fecha_vinculacion)
            jefes.append(nuevo_jefe)
            Jefe.guardar_jefes(jefes, "jefes.txt")
            print("Jefe agregado exitosamente.")

        elif opcion == "2":
            dni = input("Ingrese el DNI del jefe para ver sus empleados a cargo: ")
            jefe = next((j for j in jefes if j._dni == dni), None)
            if jefe:
                if jefe.obtener_empleados_a_cargo():
                    for empleado in jefe.obtener_empleados_a_cargo():
                        print(empleado)
                else:
                    print("Este jefe no tiene empleados a cargo.")
            else:
                print("No se encontró ningún jefe con ese DNI.")

        elif opcion == "3":
            dni_jefe = input("Ingrese el DNI del jefe al cual desea asignar un empleado: ")
            jefe = next((j for j in jefes if j._dni == dni_jefe), None)
            if jefe:
                dni_empleado = input("Ingrese el DNI del empleado que desea asignar a este jefe: ")
                empleado = next((e for e in empleados if e._dni == dni_empleado), None)
                if empleado:
                    jefe.agregar_empleado(empleado)
                    Jefe.guardar_jefes(jefes, "jefes.txt")
                    print(f"Empleado {empleado.obtener_nombre_completo()} asignado a cargo del jefe {jefe.obtener_nombre_completo()} exitosamente.")
                else:
                    print("No se encontró ningún empleado con ese DNI.")
            else:
                print("No se encontró ningún jefe con ese DNI.")

        elif opcion == "4":
            break

        else:
            print("Opción no válida. Intente nuevamente.")


def gestion_areas(areas, empleados):
    while True:
        print("\nGestión de Áreas:")
        print("1. Agregar Área")
        print("2. Asignar Empleado a Área")
        print("3. Ver Empleados de Área")
        print("4. Volver al Menú Principal")
        opcion = input("Ingrese el número de la opción que desea realizar: ")

        if opcion == "1":
            nombre = input("Ingrese el nombre del área: ")
            descripcion = input("Ingrese la descripción del área: ")
            nueva_area = Area(nombre, descripcion)
            areas.append(nueva_area)
            Area.guardar_areas(areas, "areas.txt")
            print("Área agregada exitosamente.")

        elif opcion == "2":
            nombre_area = input("Ingrese el nombre del área al cual desea asignar un empleado: ")
            area = next((a for a in areas if a._nombre == nombre_area), None)
            if area:
                dni_empleado = input("Ingrese el DNI del empleado que desea asignar a este área: ")
                empleado = next((e for e in empleados if e._dni == dni_empleado), None)
                if empleado:
                    area.agregar_empleado(empleado)
                    Area.guardar_areas(areas, "areas.txt")
                    print(f"Empleado {empleado.obtener_nombre_completo()} asignado al área {area._nombre} exitosamente.")
                else:
                    print("No se encontró ningún empleado con ese DNI.")
            else:
                print("No se encontró ningún área con ese nombre.")

        elif opcion == "3":
            nombre_area = input("Ingrese el nombre del área para ver sus empleados: ")
            area = next((a for a in areas if a._nombre == nombre_area), None)
            if area:
                if area.obtener_empleados():
                    for empleado in area.obtener_empleados():
                        print(empleado)
                else:
                    print("Este área no tiene empleados asignados.")
            else:
                print("No se encontró ningún área con ese nombre.")

        elif opcion == "4":
            break

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    empleados = Empleado.cargar_empleados("empleados.txt")
    jefes = Jefe.cargar_jefes("jefes.txt", empleados)
    areas = Area.cargar_areas("areas.txt", empleados)

    while True:
        menu_principal()
        opcion_principal = input("Ingrese el número de la opción que desea realizar: ")

        if opcion_principal == "1":
            gestion_empleados(empleados)

        elif opcion_principal == "2":
            gestion_jefes(jefes, empleados)

        elif opcion_principal == "3":
            gestion_areas(areas, empleados)

        elif opcion_principal == "4":
            print("Gracias por utilizar el Sistema de Gestión de Empleados.")
            break

        else:
            print("Opción no válida. Intente nuevamente.")