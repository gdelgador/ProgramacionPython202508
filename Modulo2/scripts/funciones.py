"""
Encuentra la suma de divisores para los numeros [10-20]
"""

def suma_divisores_numero(numero):
    listado_divisores = []
    for i in range(1, numero+1):
        if numero%i==0:
            listado_divisores.append(i)

    suma_divisores = sum(listado_divisores)
    #print(f'Lis divisores del numero {numero}: {listado_divisores}\nSuma divisores: {suma_divisores}')
    return suma_divisores


for numero in range(10,21):
    
    # mi codigo para calcular la suma de divisores
    x = suma_divisores_numero(numero)
    print(f'Suma divisores del numero {numero}: {x}')




