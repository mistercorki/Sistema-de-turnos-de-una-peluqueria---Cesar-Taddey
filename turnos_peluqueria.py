import csv
import os
import json
from datetime import datetime

class Cliente:
    def __init__(self, nombre, telefono, dni, email):
        self.nombre = nombre
        self.telefono = telefono
        self.dni = dni
        self.email = email

class Turno:
    def __init__(self, id_turno, cliente_dni, fecha_hora, servicio, estado):
        self.id_turno = int(id_turno)
        self.cliente_dni = cliente_dni
        self.fecha_hora = fecha_hora
        self.servicio = servicio
        self.estado = estado

    def to_dict(self):
        return {
            'id_turno': self.id_turno,
            'cliente_dni': self.cliente_dni,
            'fecha_hora': self.fecha_hora.strftime('%H:%M %d/%m/%Y'),
            'servicio': self.servicio,
            'estado': self.estado
        }

class GestorTurnos:
    def __init__(self, csv_file='turnos.csv', json_file='turnos.json'):
        self.csv_file = csv_file
        self.json_file = json_file
        self.clientes = {}
        self.turnos = []
        self.last_id = 0
        self._load_from_csv_if_exists()

    def _load_from_csv_if_exists(self):
        if not os.path.exists(self.csv_file):
            return
        with open(self.csv_file, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            i = 0
            if len(rows) == 0:
                return
            header = rows[0]
            i = 1
            while i < len(rows):
                row = rows[i]
                if len(row) >= 5:
                    id_turno = int(row[0])
                    cliente_dni = row[1]
                    fecha_hora = datetime.strptime(row[2], '%H:%M %d/%m/%Y')
                    servicio = row[3]
                    estado = row[4]
                    turno = Turno(id_turno, cliente_dni, fecha_hora, servicio, estado)
                    self.turnos.append(turno)
                    if id_turno > self.last_id:
                        self.last_id = id_turno
                i += 1

    def guardar_csv(self):
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id_turno', 'cliente_dni', 'fecha_hora', 'servicio', 'estado'])
            i = 0
            while i < len(self.turnos):
                t = self.turnos[i]
                writer.writerow([t.id_turno, t.cliente_dni, t.fecha_hora.strftime('%H:%M %d/%m/%Y'), t.servicio, t.estado])
                i += 1

    def guardar_json(self):
        data = {'turnos': {}, 'last_id': self.last_id}
        i = 0
        while i < len(self.turnos):
            t = self.turnos[i]
            data['turnos'][str(t.id_turno)] = t.to_dict()
            i += 1
        with open(self.json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def registrar_cliente(self, nombre, telefono, dni, email):
        if dni in self.clientes:
            return False
        self.clientes[dni] = Cliente(nombre, telefono, dni, email)
        return True

    def _parse_fecha(self, fecha_str):
        return datetime.strptime(fecha_str, '%H:%M %d/%m/%Y')

    def solicitar_turno(self, cliente_dni, fecha_str, servicio):
        try:
            fecha = self._parse_fecha(fecha_str)
        except Exception:
            return None, 'Formato de fecha inválido. Use HH:MM DD/MM/YYYY'
        if cliente_dni not in self.clientes:
            return None, 'Cliente no registrado'
        i = 0
        while i < len(self.turnos):
            t = self.turnos[i]
            if t.fecha_hora == fecha and t.estado != 'Cancelado':
                return None, 'Ya existe un turno en ese horario'
            i += 1
        self.last_id += 1
        nuevo = Turno(self.last_id, cliente_dni, fecha, servicio, 'Pendiente')
        self.turnos.append(nuevo)
        return nuevo, None

    def listar_turnos(self, filtro_dni=None, filtro_fecha=None):
        resultados = []
        i = 0
        while i < len(self.turnos):
            t = self.turnos[i]
            match = True
            if filtro_dni:
                if t.cliente_dni != filtro_dni:
                    match = False
            if filtro_fecha and match:
                try:
                    dia = datetime.strptime(filtro_fecha, '%d/%m/%Y').date()
                except Exception:
                    return None, 'Formato de fecha de filtro inválido. Use DD/MM/YYYY'
                if t.fecha_hora.date() != dia:
                    match = False
            if match:
                resultados.append(t)
            i += 1
        return resultados, None

    def _buscar_turno_por_id(self, id_turno):
        i = 0
        while i < len(self.turnos):
            if self.turnos[i].id_turno == int(id_turno):
                return self.turnos[i]
            i += 1
        return None

    def modificar_turno(self, id_turno, nueva_fecha=None, nuevo_servicio=None, nuevo_estado=None):
        t = self._buscar_turno_por_id(id_turno)
        if not t:
            return False, 'Turno no encontrado'
        if nueva_fecha:
            try:
                fecha = self._parse_fecha(nueva_fecha)
            except Exception:
                return False, 'Formato de fecha inválido. Use HH:MM DD/MM/YYYY'
            i = 0
            while i < len(self.turnos):
                other = self.turnos[i]
                if other.id_turno != t.id_turno and other.fecha_hora == fecha and other.estado != 'Cancelado':
                    return False, 'Conflicto con otro turno en ese horario'
                i += 1
            t.fecha_hora = fecha
        if nuevo_servicio:
            t.servicio = nuevo_servicio
        if nuevo_estado:
            t.estado = nuevo_estado
        return True, None

    def cancelar_turno(self, id_turno):
        t = self._buscar_turno_por_id(id_turno)
        if not t:
            return False
        t.estado = 'Cancelado'
        return True

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input('Presione Enter para continuar...')

def main():
    gestor = GestorTurnos()
    while True:
        limpiar_pantalla()
        print('Sistema de Turnos para Peluquería')
        print('1. Registrar cliente')
        print('2. Solicitar turno')
        print('3. Listar turnos')
        print('4. Modificar turno')
        print('5. Cancelar turno')
        print('6. Guardar CSV')
        print('7. Guardar JSON')
        print('8. Salir')
        opcion = input('Seleccione una opción: ').strip()
        if opcion == '1':
            nombre = input('Nombre: ').strip()
            telefono = input('Teléfono: ').strip()
            dni = input('DNI: ').strip()
            email = input('Email: ').strip()
            ok = gestor.registrar_cliente(nombre, telefono, dni, email)
            if ok:
                print('Cliente registrado correctamente')
            else:
                print('El DNI ya está registrado')
            pausa()
        elif opcion == '2':
            dni = input('DNI del cliente: ').strip()
            fecha = input('Fecha (HH:MM DD/MM/YYYY): ').strip()
            servicio = input('Servicio: ').strip()
            turno, err = gestor.solicitar_turno(dni, fecha, servicio)
            if turno:
                print('Turno solicitado. ID:', turno.id_turno)
            else:
                print('Error:', err)
            pausa()
        elif opcion == '3':
            filtro = input('Filtrar por DNI (enter sin filtro): ').strip()
            if filtro == '':
                filtro = None
            fecha_filtro = input('Filtrar por fecha DD/MM/YYYY (enter sin filtro): ').strip()
            if fecha_filtro == '':
                fecha_filtro = None
            resultados, err = gestor.listar_turnos(filtro, fecha_filtro)
            if resultados is None:
                print('Error:', err)
            else:
                i = 0
                if len(resultados) == 0:
                    print('No hay turnos que mostrar')
                while i < len(resultados):
                    t = resultados[i]
                    print('ID:', t.id_turno, '| DNI:', t.cliente_dni, '| Fecha:', t.fecha_hora.strftime('%H:%M %d/%m/%Y'), '| Servicio:', t.servicio, '| Estado:', t.estado)
                    i += 1
            pausa()
        elif opcion == '4':
            idm = input('ID del turno a modificar: ').strip()
            nuevo_fecha = input('Nueva fecha HH:MM DD/MM/YYYY (enter para mantener): ').strip()
            if nuevo_fecha == '':
                nuevo_fecha = None
            nuevo_servicio = input('Nuevo servicio (enter para mantener): ').strip()
            if nuevo_servicio == '':
                nuevo_servicio = None
            nuevo_estado = input('Nuevo estado (enter para mantener): ').strip()
            if nuevo_estado == '':
                nuevo_estado = None
            ok, err = gestor.modificar_turno(idm, nuevo_fecha, nuevo_servicio, nuevo_estado)
            if ok:
                print('Turno modificado correctamente')
            else:
                print('Error:', err)
            pausa()
        elif opcion == '5':
            idm = input('ID del turno a cancelar: ').strip()
            ok = gestor.cancelar_turno(idm)
            if ok:
                print('Turno cancelado')
            else:
                print('No se encontró el turno')
            pausa()
        elif opcion == '6':
            gestor.guardar_csv()
            print('CSV guardado en', gestor.csv_file)
            pausa()
        elif opcion == '7':
            gestor.guardar_json()
            print('JSON guardado en', gestor.json_file)
            pausa()
        elif opcion == '8':
            print('Saliendo...')
            break
        else:
            print('Opción inválida')
            pausa()

if __name__ == '__main__':
    main()
