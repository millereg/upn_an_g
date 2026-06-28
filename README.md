# Inventario UPN G

Sistema de gestión de inventario desarrollado con Django 6.0.3.

## Tecnologías

- **Backend:** Django 6.0.3 / Python
- **Base de datos:** SQLite
- **Frontend:** SB Admin 2, Bootstrap, jQuery, FontAwesome, DataTables
- **Autenticación:** Django Auth con sistema de permisos personalizado

## Estructura del Proyecto

```
upn_an_g/
├── apps/
│   ├── acceso/        # Login, logout, sistema de permisos
│   ├── compras/       # Proveedores, compras, detalles
│   ├── dashboard/     # Panel principal
│   ├── inventario/    # Inventario, movimientos, detalles
│   ├── productos/     # Categorías, productos, lotes
│   ├── sucursales/    # Sucursales, almacenes
│   ├── ubicacion/     # Países, departamentos, provincias, ciudades
│   ├── usuarios/      # Perfiles de usuario
│   └── ventas/        # Ventas, detalles
├── inventario_upn_g/ # Configuración del proyecto Django
├── static/            # Archivos estáticos (CSS, JS, img)
├── templates/         # Plantillas HTML base
├── db.sqlite3         # Base de datos
└── manage.py
```

## Aplicaciones

### 1. Acceso (`apps.acceso`)
Sistema de autenticación y permisos.

**Modelos:**
- `Modulo` - Módulos del sistema con estructura jerárquica (padre/hijo)
- `TipoPermiso` - Tipos de permisos (ver, crear, editar, eliminar, ver_reportes, exportar, imprimir, aprobar, anular)
- `PermisoModulo` - Relación entre grupos, módulos y permisos

**Vistas:** Login, Logout

### 2. Ubicación (`apps.ubicacion`)
Geografía jerárquica.

**Modelos:**
- `Pais`
- `Departamento` → Pais
- `Provincia` → Departamento
- `Ciudad` → Provincia

### 3. Sucursales (`apps.sucursales`)
**Modelos:**
- `Sucursal` - Datos de sucursal (nombre, código, dirección, contacto)
- `Almacen` - Almacenes por sucursal (tipos: principal, secundario, tránsito, cuarentena)

### 4. Productos (`apps.productos`)
**Modelos:**
- `Categoria` - Categorías de productos
- `Producto` - Productos (referencia, nombre, categoría, código de barras, precio, requiere receta)
- `Lote` - Lotes de productos (número, fecha vencimiento, registro sanitario, estado)

### 5. Compras (`apps.compras`)
**Modelos:**
- `Proveedor` - Proveedores con datos de ubicación
- `Compra` - Encabezado de compra (proveedor, almacén, tipo/número documento, estado)
- `DetalleCompra` - Líneas de compra (producto, lote, cantidad, precio)

### 6. Ventas (`apps.ventas`)
**Modelos:**
- `Venta` - Encabezado de venta (sucursal, tipo/número documento, estado)
- `DetalleVenta` - Líneas de venta (lote, cantidad, precio)

### 7. Inventario (`apps.inventario`)
**Modelos:**
- `Inventario` - Stock por almacén y lote
- `Movimiento` - Movimientos de inventario (entrada, salida, ajuste, transferencia)
- `DetalleMovimiento` - Detalles del movimiento

### 8. Usuarios (`apps.usuarios`)
**Modelos:**
- `Perfil` - Extiende Django User (sucursal asignada, teléfono, foto)

## Algoritmos y Técnicas de Optimización

Este proyecto implementa técnicas algorítmicas para demostrar competencias en el curso.

### 1. Reorder Point (Punto de Reorden)
**Técnicas:** Algoritmo Voraz + Programación Dinámica

**Ubicación:** `apps/inventario/models.py`

**Lógica:**
- Si `stock <= punto_reorden` → marcar para reorden
- Calcular cantidad óptima a pedir usando demanda histórica

**Código pendiente:**
```python
class Inventario(models.Model):
    cantidad = models.IntegerField()
    punto_reorden = models.IntegerField(default=10)
    demanda_historica = models.JSONField(default=list)

    def needs_reorder(self):
        """Algoritmo Voraz: si stock <= mínimo, pedir más"""
        return self.cantidad <= self.punto_reorden

    def calcular_lote_optimo(self):
        """Programación Dinámica: Cantidad económica de pedido (EOQ)
        EOQ = √(2DS/H) donde D=demanda, S=costo orden, H=costo hold
        """
        demanda = sum(self.demanda_historica[-12:])  # último año
        costo_orden = 10  # costo fijo por orden
        costo_hold = 0.5  # costo de almacenar por unidad

        if demanda == 0:
            return 0
        eoq = int((2 * demanda * costo_orden / costo_hold) ** 0.5)
        return eoq
```

**Reporte:** `apps/inventario/views.py` → `reporte_reorder_point()`
```
Reporte: Productos que necesitan reorden
| Producto | Stock Actual | Punto Reorden | Estado |
| Paracetamol 500mg | 15 | 20 | ⚠️ REORDENAR |
```

---

### 2. Asignación de Productos a Almacenes
**Técnicas:** Algoritmo Voraz + Backtracking

**Ubicación:** `apps/inventario/views.py`

**Lógica:**
- Algoritmo Voraz: buscar primer almacén con espacio y más cercano
- Backtracking: si ninguno tiene espacio, redistribuir stock

**Código pendiente:**
```python
def asignar_producto_almacen(producto_id, cantidad):
    """Algoritmo Voraz: buscar el más cercano con espacio"""
    almacenes = Almacen.objects.filter(
        estado='activo',
        capacidad_disponible__gte=cantidad
    ).order_by('distancia')

    if almacenes.exists():
        return almacenes.first()  # Primer almacén (más cercano)

    # Backtracking: redistribuir si ninguno tiene espacio
    return redistribuir_stock(producto_id, cantidad)

def redistribuir_stock(producto_id, cantidad_necesaria):
    """Backtracking: explorar redistribuciones válidas"""
    # Implementar lógica de backtracking
    pass
```

**Reporte:** `apps/inventario/views.py` → `reporte_asignacion()`
```
Reporte: Asignación de productos a almacenes
| Producto | Cantidad | Almacén Asignado | Criterio |
| Paracetamol | 500 | Almacén Lima | Más cercano con espacio |
```

---

### 3. Planificación de Compras (Optimización de Proveedores)
**Técnica:** Programación Dinámica

**Ubicación:** `apps/compras/views.py`

**Lógica:**
- Encontrar combinación óptima de proveedores para minimizar costo total
- DP[producto][presupuesto] = máximo valor

**Código pendiente:**
```python
def sugerir_compras():
    """Programación Dinámica: minimizar costo total de compras"""
    productos_bajos = Inventario.objects.filter(
        cantidad__lte=F('punto_reorden')
    )

    sugerencias = []
    for inv in productos_bajos:
        mejor_costo = float('inf')
        mejor_combinacion = []

        # Programación Dinámica: probar combinaciones
        combinaciones = generar_combinaciones_proveedores(inv.producto)
        for combo in combinaciones:
            costo = calcular_costo_total(combo)
            if costo < mejor_costo:
                mejor_costo = costo
                mejor_combinacion = combo

        sugerencias.append({
            'producto': inv.producto,
            'cantidad_necesaria': inv.cantidad_necesaria(),
            'mejor_opcion': mejor_combinacion,
            'costo_total': mejor_costo
        })

    return sugerencias
```

**Reporte:** `apps/compras/views.py` → `reporte_planificacion()`
```
Reporte: Órdenes de compra sugeridas
| Producto | Cantidad | Proveedor | Costo Total |
| Paracetamol | 1000 | Proveedor A+B | $4,750 |
```

---

### 4. Forecasting (Predicción de Demanda)
**Técnica:** Programación Dinámica (Suavizado Exponencial)

**Ubicación:** `apps/productos/models.py`

**Lógica:**
- Basado en historial de ventas, predecir demanda futura
- Fórmula: forecast = α × real + (1-α) × forecast_anterior

**Código pendiente:**
```python
class Producto(models.Model):

    def predecir_demanda(self, meses=3):
        """Programación Dinámica: Suavizado exponencial"""
        ventas = self.ventas.order_by('-fecha')[:12]  # último año

        if len(ventas) < 3:
            return 0

        # Suavizado exponencial
        alpha = 0.3  # peso del dato reciente
        forecast = ventas[0].cantidad

        for venta in ventas[1:]:
            forecast = alpha * venta.cantidad + (1 - alpha) * forecast

        return int(forecast * meses)
```

**Reporte:** `apps/productos/views.py` → `reporte_forecasting()`
```
Reporte: Predicción de demanda
| Mes | Demanda Real | Demanda Predicha |
| Marzo | 120 | 115 |
| Abril | 130 | 128 |
| Mayo | - | 125 |
```

---

### 5. Redistribución de Stock
**Técnica:** Backtracking

**Ubicación:** `apps/inventario/views.py`

**Lógica:**
- Cuando un almacén se llena, buscar redistribuciones válidas
- Probar opciones y retroceder si no funcionan

**Código pendiente:**
```python
def redistribuir_stock(producto_id, cantidad_necesaria):
    """Backtracking: buscar solución probando opciones"""
    def backtrack(almacenes, objetivo, idx=0):
        if objetivo == 0:
            return True  # Solución encontrada
        if objetivo < 0 or idx >= len(almacenes):
            return False  # No hay solución, retroceder

        alm = almacenes[idx]
        if alm.cantidad_disponible >= objetivo:
            # Intentar usar este almacén
            alm.cantidad_disponible -= objetivo
            if backtrack(almacenes, 0, idx + 1):
                return True
            # Deshacer
            alm.cantidad_disponible += objetivo

        # Saltar este almacén
        return backtrack(almacenes, objetivo, idx + 1)

    almacenes = Almacen.objects.filter(estado='activo')
    return backtrack(list(almacenes), cantidad_necesaria)
```

**Reporte:** `apps/inventario/views.py` → `reporte_redistribucion()`
```
Reporte: Redistribución de stock
| Desde | Hacia | Cantidad | Motivo |
| Almacén A | Almacén B | 300 | Almacén A lleno |
```

---

## Resumen de Técnicas Algorítmicas

| Técnica | Algoritmo | Ubicación | Cuándo se ejecuta |
|---------|-----------|-----------|-------------------|
| Reorder Point | Voraz + DP | `inventario/models.py` | Al hacer venta |
| Asignación Almacenes | Voraz + Backtracking | `inventario/views.py` | Al recibir compra |
| Planificación Compras | Programación Dinámica | `compras/views.py` | Stock mínimo |
| Forecasting | Programación Dinámica | `productos/models.py` | Cada noche (cron) |
| Redistribución | Backtracking | `inventario/views.py` | Almacén lleno |

---

## Reportes a Implementar

1. **Reporte de Reorder Point** - `inventario/reporte-reorder/`
2. **Reporte de Asignación de Almacenes** - `inventario/reporte-asignacion/`
3. **Reporte de Planificación de Compras** - `compras/reporte-planificacion/`
4. **Reporte de Forecasting** - `productos/reporte-forecasting/`
5. **Reporte de Redistribución** - `inventario/reporte-redistribucion/`

---

## Estado del Desarrollo

| Módulo        | Models | Admin | Forms | Views | URLs |
|---------------|--------|-------|-------|-------|------|
| acceso        | ✅     | ✅    | ✅    | ⚠️    | ⚠️   |
| compras       | ✅     | ✅    | ✅    | ❌    | ❌    |
| dashboard     | ❌     | ❌    | ❌    | ⚠️    | ✅    |
| inventario    | ✅     | ✅    | ❌    | ❌    | ❌    |
| productos     | ✅     | ✅    | ✅    | ❌    | ❌    |
| sucursales    | ✅     | ❌    | ❌    | ❌    | ❌    |
| ubicacion     | ✅     | ❌    | ❌    | ❌    | ❌    |
| usuarios      | ✅     | ✅    | ✅    | ⚠️    | ⚠️    |
| ventas        | ✅     | ✅    | ❌    | ❌    | ❌    |

**Leyenda:** ✅ Completo | ⚠️ Parcial | ❌ No implementado

## Rutas Configuradas

- `/` - Login
- `/logout/` - Logout
- `/dashboard/` - Panel principal
- `/admin/` - Django Admin
- `/acceso/` - App de acceso
- `/usuarios/` - Gestión de usuarios (CRUD completo)

## Modelos Pendientes de Registrar en Admin

- `ubicacion`: Pais, Departamento, Provincia, Ciudad
- `sucursales`: Sucursal, Almacen

## Formularios Implementados

- `acceso`: LoginForm, ModuloForm, TipoPermisoForm, PermisoModuloForm
- `compras`: ProveedorForm, CompraForm, DetalleCompraForm
- `productos`: CategoriaForm, ProductoForm, LoteForm
- `usuarios`: UsuarioForm, UsuarioEditForm, PerfilForm

## Próximos Pasos Sugeridos

1. Completar vistas CRUD para compras, ventas, productos, inventario
2. Registrar modelos de ubicacion y sucursales en admin
3. Implementar Select2/Dropdown dinámico para ubicación (cascada país→departamento→provincia→ciudad)
4. **Implementar los 5 algoritmos y sus reportes**
5. Implementar sistema de inventario (entradas/salidas por compras/ventas)
6. Agregar validaciones y permisos por grupo
