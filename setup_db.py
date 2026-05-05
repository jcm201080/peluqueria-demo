from app import app, bcrypt
from database.models import db, Usuario, Peluquero, Servicio, HorarioPeluquero

def setup_inicial():
    with app.app_context():
        # ¡IMPORTANTE! Borramos y creamos para aplicar los cambios de estructura
        db.drop_all() 
        db.create_all()
        print("✅ Base de datos reseteada y tablas creadas.")

        # 1. Crear Peluqueros y sus 7 días de horario
        if not Peluquero.query.first():
            p1 = Peluquero(nombre="Peluquero A", activo=True)
            p2 = Peluquero(nombre="Peluquero B", activo=True)
            db.session.add_all([p1, p2])
            db.session.flush() # Para obtener los IDs de los peluqueros

            for p in [p1, p2]:
                for dia in range(7): # 0 a 6
                    nuevo_dia = HorarioPeluquero(
                        peluquero_id=p.id,
                        dia_semana=dia,
                        trabaja=True if dia < 5 else (True if dia == 5 else False), # L-V trabaja, S trabaja, D cerrado
                        h_inicio_m="10:00", h_fin_m="14:00",
                        h_inicio_t="17:00", h_fin_t="21:30"
                    )
                    db.session.add(nuevo_dia)
            print("✅ Peluqueros y horarios base (7 días) añadidos.")

        # 2. Servicios (Precios y servicios reales para la demo)
        servicios_base = [
            Servicio(nombre="Corte de pelo", precio=12.0, duracion=30),
            Servicio(nombre="Arreglo de barba", precio=8.0, duracion=20),
            Servicio(nombre="Corte de pelo y arreglo barba", precio=18.0, duracion=45),
            Servicio(nombre="Corte niño", precio=10.0, duracion=30)
        ]
        db.session.add_all(servicios_base)
        print("✅ Servicios de peluquería añadidos.")

        # 3. Usuarios (Admin y Demo usando SOLO teléfono como identificador)
        telf_admin = '614398084'
        hashed_pw_admin = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = Usuario(nombre='Admin', telefono=telf_admin, password=hashed_pw_admin, es_admin=True)
        
        # Usuario Demo para los clientes
        telf_demo = '699888777'
        hashed_pw_demo = bcrypt.generate_password_hash('demo123').decode('utf-8')
        demo_user = Usuario(nombre='Cliente Demo', telefono=telf_demo, password=hashed_pw_demo, es_admin=True)

        db.session.add_all([admin, demo_user])

        db.session.commit()
        print("\n🚀 Configuración profesional completada. ¡Lista para vender!")

if __name__ == '__main__':
    setup_inicial()