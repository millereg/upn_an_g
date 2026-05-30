def merge_sort(lista, key):
    if len(lista) <= 1:
        return lista

    mid = len(lista) // 2
    izquierda = merge_sort(lista[:mid], key)
    derecha = merge_sort(lista[mid:], key)

    return merge(izquierda, derecha, key)


def merge(izq, der, key):
    resultado = []
    i = j = 0

    while i < len(izq) and j < len(der):
        valor_izq = str(getattr(izq[i], key)).lower()
        valor_der = str(getattr(der[j], key)).lower()

        if valor_izq <= valor_der:
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1

    resultado.extend(izq[i:])
    resultado.extend(der[j:])

    return resultado


def busqueda_binaria(lista, key, valor):
    izq, der = 0, len(lista) - 1
    valor = str(valor).lower()

    while izq <= der:
        mid = (izq + der) // 2
        valor_mid = str(getattr(lista[mid], key)).lower()

        if valor_mid == valor:
            return lista[mid]
        elif valor_mid < valor:
            izq = mid + 1
        else:
            der = mid - 1

    return None
