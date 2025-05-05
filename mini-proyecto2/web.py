from nicegui import ui
from alumno import Alumno, AdministradorAlumnos

#Interfaz gráfica compartida.
with ui.header().classes('bg-[#E6E6E6] justify-center'):
    ui.label('Administrador de Alumnos').style('color: #39393A; font-size: 36px; font-weight: bold;')

with ui.tabs().classes('fixed-bottom bg-[#297373]') as tabs:
    agregar_alumnos_tab = ui.tab('Agregar Alumnos', icon="add").classes('bg-[#297373] text-white')

with ui.tab_panels(tabs).classes('fixed-center'):
    with ui.tab_panel(agregar_alumnos_tab).classes('bg-gray-100'):
        with ui.card(): 
            # Interfaz de la pestaña Agregar Alumnos.
            pass


# Lógica Parte 3.

# Lógica Parte 4.

# Lógica Parte 5.


ui.run(title='Administrador de Alumnos', port=8081, reload=True)