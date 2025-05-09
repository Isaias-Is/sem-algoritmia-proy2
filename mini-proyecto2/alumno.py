from dataclasses import dataclass
from typing import List
import random

@dataclass
class Alumno:
    codigo: int
    semestre: int
    promedio: float

    def __str__(self):
        return f"{self.codigo}"
    
    def __repr__(self):
        return f"{self.codigo}"

    def __hash__(self):
        return hash(self.codigo)

def generar_alumnos(n: int):
    alumnos: List[Alumno] = []
    for _ in range(n):
        codigo = random.randint(10000, 99999)
        semestre = random.randint(1, 12)
        promedio = round(random.uniform(0, 100), 2)
        alumnos.append(Alumno(codigo, semestre, promedio))
    return alumnos

# Parte 1 y Parte 2.
class AdministradorAlumnos:
    pass


# Parte 3.
@dataclass
class AlumnosCercanos:
    alumno: Alumno
    vecinos: List[Alumno]