#!/usr/bin/env python3
"""
Script de configuración inicial para el análisis de Google Maps
Ayuda a configurar el archivo .env con la API key
"""

import os
from pathlib import Path


def setup_env():
    """Configura el archivo .env con la API key de Google Maps"""
    
    print("=" * 80)
    print("🔧 CONFIGURACIÓN INICIAL - Google Maps API")
    print("=" * 80)
    print()
    
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  El archivo .env ya existe.")
        response = input("¿Deseas sobrescribirlo? (s/n): ").lower()
        if response != 's':
            print("❌ Configuración cancelada.")
            return
    
    print("\n📋 Para obtener tu API Key de Google Maps:")
    print("   1. Ve a: https://console.cloud.google.com/")
    print("   2. Crea o selecciona un proyecto")
    print("   3. Habilita 'Places API'")
    print("   4. Ve a Credenciales → Crear credenciales → Clave de API")
    print("   5. Copia tu API Key")
    print()
    
    api_key = input("🔑 Ingresa tu Google Maps API Key: ").strip()
    
    if not api_key:
        print("❌ No se ingresó ninguna API Key.")
        return
    
    # Crear archivo .env
    with open(env_file, "w") as f:
        f.write("# Google Maps API Configuration\n")
        f.write("# Generado por setup.py\n\n")
        f.write(f"GOOGLE_MAPS_API_KEY={api_key}\n")
    
    print()
    print("✅ Archivo .env creado exitosamente!")
    print()
    print("=" * 80)
    print("🎯 SIGUIENTE PASO:")
    print("=" * 80)
    print()
    print("Configura los parámetros de búsqueda en main.py:")
    print("   - QUERY: Tipo de negocio ('restaurante', 'hotel', etc.)")
    print("   - LOCATION: Coordenadas (lat, lng)")
    print("   - RADIUS: Radio de búsqueda en metros")
    print()
    print("Luego ejecuta:")
    print("   $ python3 main.py")
    print()


def test_api():
    """Prueba la configuración de la API"""
    from dotenv import load_dotenv
    import googlemaps
    
    load_dotenv()
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not api_key:
        print("❌ No se encontró GOOGLE_MAPS_API_KEY en .env")
        return False
    
    try:
        print("\n🔍 Probando conexión con Google Maps API...")
        gmaps = googlemaps.Client(key=api_key)
        
        # Hacer una búsqueda simple
        result = gmaps.geocode('Monterrey, Mexico')
        
        if result:
            print("✅ API Key válida y funcionando correctamente!")
            print(f"   Resultado de prueba: {result[0]['formatted_address']}")
            return True
        else:
            print("⚠️  La API responde pero no retornó resultados")
            return False
            
    except Exception as e:
        print(f"❌ Error al probar la API: {e}")
        print("\nPosibles causas:")
        print("   - API Key incorrecta")
        print("   - Places API no habilitada en Google Cloud Console")
        print("   - Sin créditos disponibles")
        return False


def main():
    """Función principal"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Modo de prueba
        test_api()
    else:
        # Modo de configuración
        setup_env()
        
        # Preguntar si desea probar
        print()
        test = input("¿Deseas probar la API ahora? (s/n): ").lower()
        if test == 's':
            test_api()


if __name__ == "__main__":
    main()
