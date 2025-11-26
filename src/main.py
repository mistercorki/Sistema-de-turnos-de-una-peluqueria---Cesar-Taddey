import os
from servicios.gestor_turnos import GestorTurnos

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
