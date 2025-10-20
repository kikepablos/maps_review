#!/usr/bin/env python3
"""
Ejemplos de configuración para diferentes tipos de análisis
Copia y pega el ejemplo que necesites en main.py
"""

# ============================================================================
# EJEMPLO 1: Restaurantes en Monterrey
# ============================================================================
EJEMPLO_RESTAURANTES_MTY = """
QUERY = "restaurante"
LOCATION = (25.6866142, -100.3161126)  # Monterrey, México
RADIUS = 5000  # 5km
"""

# ============================================================================
# EJEMPLO 2: Hoteles en Cancún
# ============================================================================
EJEMPLO_HOTELES_CANCUN = """
QUERY = "hotel"
LOCATION = (21.1619, -86.8515)  # Cancún, México
RADIUS = 10000  # 10km
"""

# ============================================================================
# EJEMPLO 3: Cafeterías en Ciudad de México
# ============================================================================
EJEMPLO_CAFETERIAS_CDMX = """
QUERY = "cafetería"
LOCATION = (19.4326, -99.1332)  # CDMX, México
RADIUS = 3000  # 3km - Área más pequeña para mayor densidad
"""

# ============================================================================
# EJEMPLO 4: Gimnasios en Guadalajara
# ============================================================================
EJEMPLO_GIMNASIOS_GDL = """
QUERY = "gimnasio"
LOCATION = (20.6597, -103.3496)  # Guadalajara, México
RADIUS = 7000  # 7km
"""

# ============================================================================
# EJEMPLO 5: Farmacias en tu ubicación
# ============================================================================
EJEMPLO_FARMACIAS = """
QUERY = "farmacia"
LOCATION = (TU_LATITUD, TU_LONGITUD)  # Reemplaza con tus coordenadas
RADIUS = 2000  # 2km - Búsqueda local
"""

# ============================================================================
# EJEMPLO 6: Centros comerciales en Querétaro
# ============================================================================
EJEMPLO_MALLS_QRO = """
QUERY = "centro comercial"
LOCATION = (20.5888, -100.3899)  # Querétaro, México
RADIUS = 15000  # 15km - Área más amplia
"""

# ============================================================================
# EJEMPLO 7: Bancos en San Pedro Garza García
# ============================================================================
EJEMPLO_BANCOS_SPGG = """
QUERY = "banco"
LOCATION = (25.6515, -100.3606)  # San Pedro Garza García
RADIUS = 3000  # 3km
"""

# ============================================================================
# EJEMPLO 8: Supermercados en Puebla
# ============================================================================
EJEMPLO_SUPERMERCADOS_PUEBLA = """
QUERY = "supermercado"
LOCATION = (19.0414, -98.2063)  # Puebla, México
RADIUS = 8000  # 8km
"""

# ============================================================================
# EJEMPLO 9: Clínicas en Tijuana
# ============================================================================
EJEMPLO_CLINICAS_TJ = """
QUERY = "clínica"
LOCATION = (32.5149, -117.0382)  # Tijuana, México
RADIUS = 6000  # 6km
"""

# ============================================================================
# EJEMPLO 10: Gasolineras en León
# ============================================================================
EJEMPLO_GASOLINERAS_LEON = """
QUERY = "gasolinera"
LOCATION = (21.1236, -101.6830)  # León, Guanajuato
RADIUS = 10000  # 10km
"""


def mostrar_ejemplos():
    """Muestra todos los ejemplos disponibles"""
    print("=" * 80)
    print("📚 EJEMPLOS DE CONFIGURACIÓN")
    print("=" * 80)
    print()
    
    ejemplos = [
        ("Restaurantes en Monterrey", EJEMPLO_RESTAURANTES_MTY),
        ("Hoteles en Cancún", EJEMPLO_HOTELES_CANCUN),
        ("Cafeterías en CDMX", EJEMPLO_CAFETERIAS_CDMX),
        ("Gimnasios en Guadalajara", EJEMPLO_GIMNASIOS_GDL),
        ("Farmacias (ubicación personalizada)", EJEMPLO_FARMACIAS),
        ("Centros Comerciales en Querétaro", EJEMPLO_MALLS_QRO),
        ("Bancos en San Pedro", EJEMPLO_BANCOS_SPGG),
        ("Supermercados en Puebla", EJEMPLO_SUPERMERCADOS_PUEBLA),
        ("Clínicas en Tijuana", EJEMPLO_CLINICAS_TJ),
        ("Gasolineras en León", EJEMPLO_GASOLINERAS_LEON),
    ]
    
    for i, (nombre, codigo) in enumerate(ejemplos, 1):
        print(f"{i}. {nombre}")
    
    print()
    print("=" * 80)
    print("📝 CÓMO USAR:")
    print("=" * 80)
    print()
    print("1. Elige un ejemplo de la lista")
    print("2. Abre main.py y busca las líneas 302-304")
    print("3. Reemplaza QUERY, LOCATION y RADIUS con el ejemplo")
    print("4. Ejecuta: python3 main.py")
    print()
    
    try:
        seleccion = int(input("Selecciona un ejemplo (1-10) o 0 para salir: "))
        
        if seleccion == 0:
            print("👋 ¡Hasta luego!")
            return
        
        if 1 <= seleccion <= len(ejemplos):
            nombre, codigo = ejemplos[seleccion - 1]
            print()
            print("=" * 80)
            print(f"📋 EJEMPLO: {nombre}")
            print("=" * 80)
            print(codigo)
            print("=" * 80)
            print()
            print("Copia este código y reemplázalo en main.py (líneas 302-304)")
        else:
            print("❌ Opción inválida")
    
    except ValueError:
        print("❌ Por favor ingresa un número")
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego!")


# ============================================================================
# COORDENADAS DE CIUDADES PRINCIPALES DE MÉXICO
# ============================================================================
COORDENADAS_CIUDADES = {
    "Monterrey": (25.6866, -100.3161),
    "Ciudad de México": (19.4326, -99.1332),
    "Guadalajara": (20.6597, -103.3496),
    "Puebla": (19.0414, -98.2063),
    "Tijuana": (32.5149, -117.0382),
    "León": (21.1236, -101.6830),
    "Querétaro": (20.5888, -100.3899),
    "Cancún": (21.1619, -86.8515),
    "San Pedro Garza García": (25.6515, -100.3606),
    "Saltillo": (25.4232, -101.0053),
    "Mérida": (20.9674, -89.5926),
    "Toluca": (19.2827, -99.6557),
    "Aguascalientes": (21.8853, -102.2916),
    "Chihuahua": (28.6330, -106.0691),
    "Hermosillo": (29.0729, -110.9559),
    "Culiacán": (24.8091, -107.3940),
    "Morelia": (19.7060, -101.1949),
    "Veracruz": (19.1738, -96.1342),
    "Acapulco": (16.8531, -99.8237),
    "Oaxaca": (17.0732, -96.7266),
}


def buscar_coordenadas():
    """Ayuda a encontrar coordenadas de una ciudad"""
    print()
    print("=" * 80)
    print("📍 COORDENADAS DE CIUDADES PRINCIPALES")
    print("=" * 80)
    print()
    
    for ciudad, (lat, lng) in COORDENADAS_CIUDADES.items():
        print(f"{ciudad:30} → ({lat}, {lng})")
    
    print()
    print("=" * 80)
    print("💡 CÓMO OBTENER COORDENADAS PERSONALIZADAS:")
    print("=" * 80)
    print()
    print("Método 1 - Google Maps:")
    print("   • Haz clic derecho en el mapa")
    print("   • La primera opción muestra las coordenadas")
    print()
    print("Método 2 - Con la API:")
    print("   • Ejecuta: python3 -c \"")
    print("     from dotenv import load_dotenv; import os, googlemaps;")
    print("     load_dotenv();")
    print("     g = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'));")
    print("     r = g.geocode('Ciudad, País');")
    print("     print(r[0]['geometry']['location'])\"")
    print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'coords':
        buscar_coordenadas()
    else:
        mostrar_ejemplos()
