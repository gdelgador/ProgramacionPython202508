"""
Realizar una función que permita la carga de n alumnos. 
Por cada alumno se deberá preguntar el nombre completo 
y permitir el ingreso de 3 notas. 
Las notas deben estar comprendidas entre 0 y 10. Devolver el listado de alumnos.
"""

from pprint import pprint


def registrar_nota_alumno():

    try:
        nota = int(input('Ingrese una nota entre 0 y 10: '))

        # me aseguro que nota estre en el rango de 0 a 10
        assert nota>=0 and nota<=10, 'Valor de nota invalido'

        # retorno nota en el rango especificado
        return nota
    except:
        print('Valor invalido, nota debe ser entero entre 0 y 10')
        return registrar_nota_alumno()

def registrar_alumno():

    alumno = dict()

    # 1. Solicitar nombre completo
    nombre = input("Ingrese el nombre del alumno a registrar: ")

    # 2. Solicitar notas
    notas =[]
    for i in range(3):
        print(f'Ingrese la nota {i+1} ....')
        nota = registrar_nota_alumno()
        notas.append(nota)

    # agrego al diciconario
    alumno['nombre']=nombre
    alumno['notas']=notas

    print('Se registro al alumno!')
    return alumno


listado_alumnos =[]
# 1. permite carga de alumnos hasta que usuario diga que ya no quiere ingresar mas alumnos
while True:

    respuesta =input("Desea registrar un alumno?(s/n) ").lower()

    if respuesta!='s':
        print('Salgo del bucle ...')
        break

    # 1.1 registro alumnos .....
    alumno =registrar_alumno()
    listado_alumnos.append(alumno)


pprint(listado_alumnos)












