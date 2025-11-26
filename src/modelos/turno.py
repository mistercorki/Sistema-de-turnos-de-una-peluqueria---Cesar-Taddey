from datetime import datetime

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
