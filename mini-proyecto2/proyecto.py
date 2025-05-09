from nicegui import ui
import random
import csv
import io
from dataclasses import dataclass, asdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import base64

@dataclass
class Alumno:
    codigo: int
    semestre: int
    promedio: float

alumnos: list[Alumno] = []

# Función para generar alumnos aleatorios
def generar_alumnos(n: int):
    alumnos.clear()
    for _ in range(n):
        codigo = random.randint(10000, 99999)
        semestre = random.randint(1, 12)
        promedio = round(random.uniform(0, 100), 2)
        alumnos.append(Alumno(codigo, semestre, promedio))
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

# Interfaz de la aplicación

with ui.header().classes('bg-[#E6E6E6] justify-center'):
    ui.label('Administrador de Alumnos').style('color: #39393A; font-size: 36px; font-weight: bold;')

with ui.tabs().classes('fixed-bottom bg-[#297373]') as tabs:
    agregar_alumnos_tab = ui.tab('Agregar Alumnos', icon="add").classes('bg-[#297373] text-white')
    exportar_importar_tab = ui.tab('Exportar / Importar', icon="upload_download").classes('bg-[#297373] text-white')

with ui.tab_panels(tabs).classes('w-full h-full'):
    with ui.tab_panel(agregar_alumnos_tab).classes('bg-gray-100'):
        with ui.card():
            cantidad = ui.input('Cantidad de alumnos').props('type=number')
            ui.button('Generar', on_click=lambda: generar_alumnos(int(cantidad.value or 0)))
            ui.button('Ordenar por Código', on_click=lambda: ordenar_por('codigo'))
            ui.button('Ordenar por Semestre (desc)', on_click=lambda: ordenar_por('semestre', descendente=True))
            ui.button('Ordenar por Promedio', on_click=lambda: ordenar_por('promedio'))
            ui.button('Limpiar', on_click=limpiar)
            
            # Tabla para mostrar los alumnos
            tabla = ui.table(columns=[
                {'name': 'codigo', 'label': 'Código', 'field': 'codigo'},
                {'name': 'semestre', 'label': 'Semestre', 'field': 'semestre'},
                {'name': 'promedio', 'label': 'Promedio', 'field': 'promedio'},
            ], rows=[]).props('wrap-cells')

            # Estadísticas y gráfico
            ui.label('Promedio general:').style('font-size: 16px; margin-top: 10px')
            promedio_grupo = ui.label().style('font-size: 16px; margin-top: 5px')
            ui.label('Promedio máximo:').style('font-size: 16px; margin-top: 10px')
            maximo = ui.label().style('font-size: 16px; margin-top: 5px')
            ui.label('Promedio mínimo:').style('font-size: 16px; margin-top: 10px')
            minimo = ui.label().style('font-size: 16px; margin-top: 5px')
            resumen = ui.label().style('font-size: 16px; margin-top: 5px')
            grafica = ui.image().style('margin-top: 20px')
        
    with ui.tab_panel(exportar_importar_tab).classes('bg-gray-100'):
        with ui.card():
            ui.button('Exportar CSV', on_click=exportar_csv)
            ui.upload(on_upload=cargar_csv)

ui.run(title='Administrador de Alumnos', port=8081, reload=True)










