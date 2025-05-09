from nicegui import ui
from alumno import Alumno, AdministradorAlumnos, generar_alumnos
from algoritmos import alumnos_mas_cercanos, Grafo
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import base64
import io
import csv
import pprint

alumnos: list[Alumno] = []

def generar_alumnos_ui(n: int):
    global alumnos
    alumnos.clear()
    alumnos = generar_alumnos(n)
    actualizar_tabla()

# Función para actualizar la tabla de alumnos
def actualizar_tabla():
    tabla.rows.clear()
    for a in alumnos:
        tabla.add_row({'codigo': a.codigo, 'semestre': a.semestre, 'promedio': f'{a.promedio:.2f}'})
    mostrar_estadisticas()

# Función para ordenar los alumnos por un atributo
def ordenar_por(attr: str, descendente=False):
    alumnos.sort(key=lambda x: getattr(x, attr), reverse=descendente)
    actualizar_tabla()

# Función para exportar los alumnos a CSV
def exportar_csv():
    contenido = 'Código,Semestre,Promedio\n'
    for a in alumnos:
        contenido += f'{a.codigo},{a.semestre},{a.promedio}\n'
    with open('alumnos.csv', 'w', encoding='utf-8') as f:
        f.write(contenido)
    ui.download('alumnos.csv')

# Función para cargar alumnos desde un archivo CSV
def cargar_csv(file):
    alumnos.clear()
    content = file.content.read().decode()
    reader = csv.reader(io.StringIO(content))
    next(reader)  # Saltar el encabezado
    for row in reader:
        codigo, semestre, promedio = int(row[0]), int(row[1]), float(row[2])
        alumnos.append(Alumno(codigo, semestre, promedio))
    actualizar_tabla()

def limpiar():
    alumnos.clear()              
    tabla.update_rows([])        
    promedio_grupo.set_text('')  
    maximo.set_text('')
    minimo.set_text('')
    resumen.set_text('')
    with grafica:
        grafica.clear()          

# Función para mostrar estadísticas
def mostrar_estadisticas():
    if not alumnos:
        promedio_grupo.set_text('Promedio general: N/A')
        return

    promedios = [a.promedio for a in alumnos]
    promedio_grupo.set_text(f'Promedio general: {sum(promedios)/len(promedios):.2f}')
    maximo.set_text(f'Promedio más alto: {max(promedios):.2f}')
    minimo.set_text(f'Promedio más bajo: {min(promedios):.2f}')

    alta = len([a for a in alumnos if a.promedio > 80])
    media = len([a for a in alumnos if 60 <= a.promedio <= 80])
    baja = len([a for a in alumnos if a.promedio < 60])
    resumen.set_text(f'Alta (>80): {alta} | Media (60–80): {media} | Baja (<60): {baja}')

    mostrar_grafica()

# Función para mostrar el gráfico de barras
def mostrar_grafica():
    conteo = [0] * 12
    for a in alumnos:
        conteo[a.semestre - 1] += 1

    fig, ax = plt.subplots()
    ax.bar(range(1, 13), conteo)
    ax.set_xlabel('Semestre')
    ax.set_ylabel('Número de Alumnos')
    ax.set_title('Alumnos por Semestre')

    buf = io.BytesIO()
    FigureCanvasAgg(fig).print_png(buf)
    encoded = base64.b64encode(buf.getvalue()).decode()
    grafica.set_source(f'data:image/png;base64,{encoded}')
    plt.close(fig)

def tab_cambiada(tab):
    #print(f"Tab cambiado a: {tab.value}")
    if tab.value == "Vecino Cercano":
        actualizar_lista()

#Interfaz gráfica compartida.
with ui.header().classes('bg-[#E6E6E6] justify-center'):
    ui.label('Administrador de Alumnos').style('color: #39393A; font-size: 36px; font-weight: bold;')

with ui.tabs(on_change=tab_cambiada).classes('fixed-bottom bg-[#297373]') as tabs:
    agregar_alumnos_tab = ui.tab('Agregar Alumnos', icon="add").classes('bg-[#297373] text-white')
    exportar_importar_tab = ui.tab('Exportar / Importar', icon="upload_download").classes('bg-[#297373] text-white')
    grafo_tab = ui.tab('Grafo', icon="show_chart").classes('bg-[#297373] text-white')
    vecino_cercano_tab = ui.tab('Vecino Cercano', icon="search").classes('bg-[#297373] text-white')

with ui.tab_panels(tabs).classes('fixed-center'):
    with ui.tab_panel(agregar_alumnos_tab).classes('bg-gray-100 w-1/2 h-full'):
        with ui.row().classes('items-center justify-center h-full w-full'):
            with ui.card().classes('justify-center'):
                ui.label('Generador de Alumnos').classes('text-center text-xl font-bold')
                cantidad = ui.input('# de alumnos a generar').classes('w-full').props('type=number')
                with ui.row().classes('justify-center').classes('w-full'):
                    ui.button('Generar', on_click=lambda: generar_alumnos_ui(int(cantidad.value or 0)))
                    ui.button('Limpiar', on_click=limpiar)
                ui.label('Tabla').classes('text-center text-xl font-bold')
                ui.button('Ordenar por Código', on_click=lambda: ordenar_por('codigo'))
                ui.button('Ordenar por Semestre (desc)', on_click=lambda: ordenar_por('semestre', descendente=True))
                ui.button('Ordenar por Promedio', on_click=lambda: ordenar_por('promedio'))
                
                # Tabla para mostrar los alumnos
                with ui.scroll_area().classes('w-full h-50 justify-center'):
                    tabla = ui.table(columns=[
                        {'name': 'codigo', 'label': 'Código', 'field': 'codigo'},
                        {'name': 'semestre', 'label': 'Semestre', 'field': 'semestre'},
                        {'name': 'promedio', 'label': 'Promedio', 'field': 'promedio'},
                    ], rows=[]).props('wrap-cells')
            with ui.card().classes('justify-center'):
                ui.label('Estadísticas de Alumnos').classes('text-center text-xl font-bold')
                # Estadísticas y gráfico
                promedio_grupo = ui.label().style('font-size: 16px; margin-top: 5px')
                maximo = ui.label().style('font-size: 16px; margin-top: 5px')
                minimo = ui.label().style('font-size: 16px; margin-top: 5px')
                resumen = ui.label().style('font-size: 16px; margin-top: 5px')
                grafica = ui.image().style('margin-top: 20px')
        
    with ui.tab_panel(exportar_importar_tab).classes('bg-gray-100'):
        with ui.card():
            ui.button('Exportar CSV', on_click=exportar_csv)
            ui.upload(on_upload=cargar_csv)
# Parte gráfica: Pestaña Grafo
    with ui.tab_panel(grafo_tab).classes('bg-gray-100 w-1/3'):
        with ui.card().classes('justify-center'):
            # Interfaz de la pestaña Grafo.
            with ui.card().classes('justify-center'):
                ui.label("Grafo").classes('text-xl font-bold')
                ui.button("Crear Grafo", on_click=lambda: grafo())
                grafo_label = ui.label("").classes('w-full')

# Parte gráfica: Pestaña Buscar Vecino Cercano. 
    with ui.tab_panel(vecino_cercano_tab).classes('bg-gray-100 w-1/3'):
        with ui.card().classes('justify-center'):
            # Interfaz de la pestaña Vecino Cercano.
            ui.label('Buscar Vecino Cercano').classes('text-xl font-bold')
            busqueda_alumnos_lista = ui.select({i : str(i) for i in alumnos}, label='Buscar Alumno').classes('w-full')
            ui.button('Buscar', on_click=lambda: buscar_alumno())
            ui.label('Alumno Cercano:').classes('font-bold')
            alumnos_cercanos_tabla = ui.table(columns=[
                {'name': 'codigo', 'label': 'Código', 'field': 'codigo'},
                {'name': 'semestre', 'label': 'Semestre', 'field': 'semestre'},
                {'name': 'promedio', 'label': 'Promedio', 'field': 'promedio'},
            ], rows=[])
        
# Parte gráfica: Pestaña Grafo. 


# Lógica Parte 4.
def grafo():
    if len(alumnos) == 0:
        ui.notify('No hay alumnos generados', color='red')
        return
    # Lógica para crear el grafo.
    grafo = Grafo(alumnos)
    grafo.encontrar_conexiones(alumnos)
    print("--------- Grafo creado: Alumnos que Comparten Semestre---------")
    pprint.pprint(grafo.grafo)
    ui.notify('Grafo creado en la termianl', color='green')

# Lógica Parte 5.
def buscar_alumno():
    codigo = int(busqueda_alumnos_lista.value.codigo)
    print(codigo)
    alumnos_cercanos = alumnos_mas_cercanos(alumnos)
    for a in alumnos_cercanos:
        if a.alumno.codigo == codigo:
            alumnos_cercanos_tabla.update_rows([{'codigo': a.vecinos.codigo, 'semestre': a.vecinos.semestre, 'promedio': f'{a.vecinos.promedio:.2f}'}])
            break
    else:
        ui.notify('Alumno no encontrado', color='red')

def actualizar_lista():
    busqueda_alumnos_lista.set_options({i : str(i) for i in sorted(alumnos, key=lambda x: x.codigo)})


tabs.set_value(agregar_alumnos_tab)
ui.run(title='Administrador de Alumnos', port=8081, reload=True)