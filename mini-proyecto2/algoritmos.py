from alumno import  Alumno, AlumnosCercanos
from typing import List, Dict, Set

def alumnos_mas_cercanos(alumnos: List[Alumno]) -> List[AlumnosCercanos]:
    if len(alumnos) <= 1:
        print("Error: Se necesitan como mínimo 2 alumnos.")
        return
    resultados = []
    i = 0
    while i < len(alumnos):
        alumno1 = alumnos[i]
        distancia_min = float('inf')
        j = 0
        while j < len(alumnos):
            if i == j:
                j += 1
                continue
            alumno2 = alumnos[j]
            distancia = abs(alumno1.promedio - alumno2.promedio)
            if distancia < distancia_min:
                alumnos_mas_cercanos = AlumnosCercanos(alumno1, alumno2)
                distancia_min = distancia
            j += 1
        resultados.append(alumnos_mas_cercanos)
        i = i + 1
    return resultados

class Grafo:
    def __init__(self, alumnos: List[Alumno]):
        self.grafo: Dict[Alumno, Set[Alumno]] = {a: set() for a in alumnos}
    
    def agregar_conexion(self, alumno1: Alumno, alumno2: Alumno):
        self.grafo[alumno1].add(alumno2)
        self.grafo[alumno2].add(alumno1)

    def encontrar_conexiones(self, alumnos: List[Alumno]):
        i = 0
        while i < len(alumnos):
            j = 0
            while j < len(alumnos):
                if i == j:
                    j += 1
                    continue
                if alumnos[i].semestre == alumnos[j].semestre:
                    self.agregar_conexion(alumnos[i], alumnos[j])
                j += 1
            i = i + 1
    
    def __str__(self):
        return str(self.grafo)