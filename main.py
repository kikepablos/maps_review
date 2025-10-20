from dotenv import load_dotenv
import os
import googlemaps
import pandas as pd
import folium
from folium.plugins import HeatMap
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import time
import json

load_dotenv()


class GoogleMapsAnalyzer:
    def __init__(self, api_key):
        """Inicializa el analizador con la API key de Google Maps"""
        self.gmaps = googlemaps.Client(key=api_key)
        self.businesses = []
        
    def search_places(self, query, location, radius=5000, max_results=60):
        """
        Busca lugares usando Google Places API
        
        Args:
            query: Tipo de negocio (ej: 'restaurante', 'hotel', 'cafetería')
            location: Tupla (lat, lng) del centro de búsqueda
            radius: Radio de búsqueda en metros
            max_results: Número máximo de resultados
        """
        print(f"\n🔍 Buscando '{query}' en un radio de {radius}m...")
        
        places_result = self.gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=query
        )
        
        businesses = places_result.get('results', [])
        
        # Obtener más resultados si hay página siguiente
        while 'next_page_token' in places_result and len(businesses) < max_results:
            time.sleep(2)  # Esperar antes de la siguiente petición
            places_result = self.gmaps.places_nearby(
                page_token=places_result['next_page_token']
            )
            businesses.extend(places_result.get('results', []))
        
        self.businesses = businesses[:max_results]
        print(f"✅ Se encontraron {len(self.businesses)} negocios")
        
    def get_place_details(self, place_id):
        """Obtiene detalles completos de un lugar, incluyendo reviews"""
        try:
            place_details = self.gmaps.place(place_id, fields=[
                'name', 'rating', 'user_ratings_total', 'reviews',
                'formatted_address', 'geometry'
            ])
            return place_details.get('result', {})
        except Exception as e:
            print(f"Error obteniendo detalles: {e}")
            return {}
    
    def collect_detailed_data(self):
        """Recopila datos detallados de todos los negocios"""
        print("\n📊 Recopilando datos detallados...")
        detailed_businesses = []
        
        for i, business in enumerate(self.businesses, 1):
            print(f"  Procesando {i}/{len(self.businesses)}: {business.get('name', 'Sin nombre')}", end='\r')
            
            place_id = business.get('place_id')
            details = self.get_place_details(place_id)
            
            business_data = {
                'name': business.get('name', 'Sin nombre'),
                'rating': business.get('rating', 0),
                'total_ratings': business.get('user_ratings_total', 0),
                'address': details.get('formatted_address', 'Sin dirección'),
                'lat': business.get('geometry', {}).get('location', {}).get('lat', 0),
                'lng': business.get('geometry', {}).get('location', {}).get('lng', 0),
                'types': ', '.join(business.get('types', [])),
                'reviews': details.get('reviews', [])
            }
            
            detailed_businesses.append(business_data)
            time.sleep(0.1)  # Pequeña pausa para no exceder rate limits
        
        print("\n✅ Datos detallados recopilados")
        self.df = pd.DataFrame(detailed_businesses)
        return self.df
    
    def get_top_businesses(self, n=15):
        """Obtiene las mejores N unidades económicas"""
        # Filtrar negocios con rating > 0
        df_filtered = self.df[self.df['rating'] > 0].copy()
        
        # Ordenar por rating (descendente) y total_ratings (descendente)
        top = df_filtered.nlargest(n, ['rating', 'total_ratings'])
        
        print(f"\n⭐ Top {n} Mejores Negocios:")
        print("-" * 80)
        for idx, row in top.iterrows():
            print(f"{row['name'][:40]:40} | Rating: {row['rating']:.1f} | Reviews: {row['total_ratings']}")
        
        return top
    
    def get_worst_businesses(self, n=15):
        """Obtiene las peores N unidades económicas"""
        # Filtrar negocios con rating > 0
        df_filtered = self.df[self.df['rating'] > 0].copy()
        
        # Ordenar por rating (ascendente) pero con suficientes reviews
        # Para evitar negocios con pocas reviews que sesgan el resultado
        df_filtered = df_filtered[df_filtered['total_ratings'] >= 3]
        worst = df_filtered.nsmallest(n, ['rating'])
        
        print(f"\n⚠️ Top {n} Peores Negocios:")
        print("-" * 80)
        for idx, row in worst.iterrows():
            print(f"{row['name'][:40]:40} | Rating: {row['rating']:.1f} | Reviews: {row['total_ratings']}")
        
        return worst
    
    def create_heatmap(self, businesses_df, filename, title):
        """Crea un mapa de calor con las ubicaciones"""
        print(f"\n🗺️ Creando mapa de calor: {filename}")
        
        if businesses_df.empty:
            print("⚠️ No hay datos para crear el mapa")
            return
        
        # Centro del mapa
        center_lat = businesses_df['lat'].mean()
        center_lng = businesses_df['lng'].mean()
        
        # Crear mapa base
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=13,
            tiles='OpenStreetMap'
        )
        
        # Datos para el heatmap
        heat_data = [[row['lat'], row['lng'], row['total_ratings']] 
                     for idx, row in businesses_df.iterrows()]
        
        # Agregar capa de calor
        HeatMap(heat_data, radius=15, blur=25, max_zoom=13).add_to(m)
        
        # Guardar mapa
        m.save(filename)
        print(f"✅ Mapa guardado: {filename}")
    
    def extract_review_text(self, businesses_df):
        """Extrae todo el texto de las reviews"""
        all_text = []
        
        for reviews in businesses_df['reviews']:
            if isinstance(reviews, list):
                for review in reviews:
                    if isinstance(review, dict):
                        text = review.get('text', '')
                        if text:
                            all_text.append(text)
        
        return ' '.join(all_text)
    
    def create_wordcloud(self, text, filename, title):
        """Crea una nube de palabras"""
        print(f"\n☁️ Creando word cloud: {filename}")
        
        if not text or len(text.strip()) == 0:
            print("⚠️ No hay texto suficiente para crear word cloud")
            return
        
        # Palabras comunes a excluir (stopwords en español)
        stopwords = set([
            'el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'ser', 'se', 'no',
            'haber', 'por', 'con', 'su', 'para', 'como', 'estar', 'tener',
            'le', 'lo', 'todo', 'pero', 'más', 'hacer', 'o', 'poder', 'decir',
            'este', 'ir', 'otro', 'ese', 'si', 'me', 'ya', 'ver', 'porque',
            'dar', 'cuando', 'él', 'muy', 'sin', 'vez', 'mucho', 'saber',
            'qué', 'sobre', 'mi', 'alguno', 'mismo', 'yo', 'también', 'hasta',
            'año', 'dos', 'querer', 'entre', 'así', 'primero', 'desde', 'grande',
            'eso', 'ni', 'nos', 'llegar', 'pasar', 'tiempo', 'ella', 'sí',
            'día', 'uno', 'bien', 'poco', 'deber', 'entonces', 'poner', 'cosa',
            'tanto', 'hombre', 'parecer', 'nuestro', 'tan', 'donde', 'ahora',
            'parte', 'después', 'vida', 'quedar', 'siempre', 'creer', 'hablar',
            'llevar', 'dejar', 'nada', 'cada', 'seguir', 'menos', 'nuevo', 'encontrar',
            'algo', 'solo', 'decir', 'entonces', 'fue', 'the', 'and', 'is', 'it',
            'to', 'of', 'was', 'for', 'on', 'are', 'with', 'as', 'I', 'his', 'that',
            'he', 'this', 'at', 'but', 'from', 'had', 'they', 'which', 'she', 'or',
        ])
        
        # Crear wordcloud
        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            stopwords=stopwords,
            max_words=100,
            colormap='viridis' if 'top' in filename.lower() else 'Reds',
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)
        
        # Crear figura
        plt.figure(figsize=(20, 10))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title(title, fontsize=24, fontweight='bold', pad=20)
        plt.tight_layout(pad=0)
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"✅ Word cloud guardado: {filename}")
    
    def generate_report(self, top_businesses, worst_businesses):
        """Genera un reporte estadístico"""
        print("\n📈 Generando reporte estadístico...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análisis de Unidades Económicas - Google Maps', fontsize=16, fontweight='bold')
        
        # 1. Rating distribution
        axes[0, 0].hist(self.df[self.df['rating'] > 0]['rating'], bins=20, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Distribución de Ratings')
        axes[0, 0].set_xlabel('Rating')
        axes[0, 0].set_ylabel('Frecuencia')
        axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Top 15 mejores
        top_plot = top_businesses.head(15)[['name', 'rating']].sort_values('rating')
        axes[0, 1].barh(range(len(top_plot)), top_plot['rating'], color='green', alpha=0.7)
        axes[0, 1].set_yticks(range(len(top_plot)))
        axes[0, 1].set_yticklabels([n[:25] for n in top_plot['name']], fontsize=8)
        axes[0, 1].set_title('Top 15 Mejores Negocios')
        axes[0, 1].set_xlabel('Rating')
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # 3. Top 15 peores
        worst_plot = worst_businesses.head(15)[['name', 'rating']].sort_values('rating', ascending=False)
        axes[1, 0].barh(range(len(worst_plot)), worst_plot['rating'], color='red', alpha=0.7)
        axes[1, 0].set_yticks(range(len(worst_plot)))
        axes[1, 0].set_yticklabels([n[:25] for n in worst_plot['name']], fontsize=8)
        axes[1, 0].set_title('Top 15 Peores Negocios')
        axes[1, 0].set_xlabel('Rating')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # 4. Reviews distribution
        axes[1, 1].scatter(self.df['rating'], self.df['total_ratings'], alpha=0.5)
        axes[1, 1].set_title('Rating vs Número de Reviews')
        axes[1, 1].set_xlabel('Rating')
        axes[1, 1].set_ylabel('Número de Reviews')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('analisis_estadistico.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        print("✅ Reporte guardado: analisis_estadistico.png")
    
    def save_data(self, filename='datos_negocios.csv'):
        """Guarda los datos en un archivo CSV"""
        # Crear copia sin la columna reviews (es una lista)
        df_export = self.df.drop(columns=['reviews'])
        df_export.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 Datos guardados: {filename}")


def main():
    # Cargar API key desde .env
    API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    
    if not API_KEY:
        print("❌ ERROR: No se encontró GOOGLE_MAPS_API_KEY en el archivo .env")
        print("\nPor favor:")
        print("1. Ve a: https://console.cloud.google.com/")
        print("2. Crea un proyecto y habilita Google Places API")
        print("3. Genera una API Key")
        print("4. Agrega GOOGLE_MAPS_API_KEY=tu_api_key en el archivo .env")
        return
    
    print("=" * 80)
    print("🗺️  ANÁLISIS DE GOOGLE MAPS REVIEWS")
    print("=" * 80)
    
    # Solicitar configuración de búsqueda al usuario
    print("\n📝 Configuración de búsqueda:")
    print("-" * 80)
    
    # Solicitar tipo de negocio
    print("\n💼 Tipo de negocio a buscar")
    print("   Ejemplos: restaurante, hotel, cafetería, gimnasio, farmacia, banco, etc.")
    QUERY = input("   → Ingresa el tipo de negocio: ").strip()
    
    if not QUERY:
        print("⚠️  No se ingresó ningún tipo de negocio. Usando 'restaurante' por defecto.")
        QUERY = "restaurante"
    
    # Solicitar ubicación
    print("\n📍 Ubicación del centro de búsqueda")
    print("   Formato: latitud,longitud")
    print("   Ejemplo: 25.6866142,-100.3161126 (Monterrey)")
    print("   Tip: Busca coordenadas en Google Maps → Clic derecho → Primera opción")
    print("   💡 Presiona Enter para usar Monterrey por defecto")
    location_input = input("   → Ingresa las coordenadas (lat,lng) [Enter=Monterrey]: ").strip()
    
    if location_input:
        try:
            lat, lng = map(float, location_input.split(','))
            LOCATION = (lat, lng)
            print(f"   ✅ Ubicación configurada: {LOCATION}")
        except ValueError:
            print("   ⚠️  Formato inválido. Usando Monterrey por defecto.")
            LOCATION = (25.6866142, -100.3161126)
    else:
        LOCATION = (25.6866142, -100.3161126)
        print("   ✅ Usando Monterrey por defecto: (25.6866142, -100.3161126)")
    
    # Solicitar radio
    print("\n📏 Radio de búsqueda")
    print("   En metros (Ejemplo: 5000 = 5km, máximo recomendado: 50000 = 50km)")
    radius_input = input("   → Ingresa el radio en metros: ").strip()
    
    if radius_input:
        try:
            RADIUS = int(radius_input)
            if RADIUS > 50000:
                print("⚠️  Radio muy grande. Ajustando a 50000m (50km)")
                RADIUS = 50000
            elif RADIUS < 100:
                print("⚠️  Radio muy pequeño. Ajustando a 1000m (1km)")
                RADIUS = 1000
        except ValueError:
            print("⚠️  Valor inválido. Usando 5000m (5km) por defecto.")
            RADIUS = 5000
    else:
        print("⚠️  No se ingresó radio. Usando 5000m (5km) por defecto.")
        RADIUS = 5000
    
    print("\n" + "=" * 80)
    print("✅ Búsqueda configurada:")
    print("=" * 80)
    print(f"   📌 Tipo: {QUERY}")
    print(f"   📍 Ubicación: {LOCATION}")
    print(f"   📏 Radio: {RADIUS}m ({RADIUS/1000:.1f}km)")
    print("=" * 80)
    
    # Confirmación
    confirmar = input("\n¿Deseas continuar con esta búsqueda? (s/n): ").lower()
    if confirmar != 's':
        print("\n❌ Búsqueda cancelada.")
        return
    
    # Crear analizador
    analyzer = GoogleMapsAnalyzer(API_KEY)
    
    # Buscar lugares
    analyzer.search_places(QUERY, LOCATION, RADIUS)
    
    # Recopilar datos detallados
    analyzer.collect_detailed_data()
    
    # Obtener mejores y peores
    top_businesses = analyzer.get_top_businesses(15)
    worst_businesses = analyzer.get_worst_businesses(15)
    
    # Crear mapas de calor
    analyzer.create_heatmap(top_businesses, 'mapa_mejores_negocios.html', 'Mejores Negocios')
    analyzer.create_heatmap(worst_businesses, 'mapa_peores_negocios.html', 'Peores Negocios')
    
    # Extraer texto de reviews
    top_text = analyzer.extract_review_text(top_businesses)
    worst_text = analyzer.extract_review_text(worst_businesses)
    
    # Crear word clouds
    analyzer.create_wordcloud(
        top_text,
        'wordcloud_mejores.png',
        'Palabras Frecuentes en Reviews de Mejores Negocios'
    )
    analyzer.create_wordcloud(
        worst_text,
        'wordcloud_peores.png',
        'Palabras Frecuentes en Reviews de Peores Negocios'
    )
    
    # Generar reporte estadístico
    analyzer.generate_report(top_businesses, worst_businesses)
    
    # Guardar datos
    analyzer.save_data()
    
    print("\n" + "=" * 80)
    print("✅ ANÁLISIS COMPLETADO")
    print("=" * 80)
    print("\n📁 Archivos generados:")
    print("   - mapa_mejores_negocios.html")
    print("   - mapa_peores_negocios.html")
    print("   - wordcloud_mejores.png")
    print("   - wordcloud_peores.png")
    print("   - analisis_estadistico.png")
    print("   - datos_negocios.csv")
    print("\n🎉 ¡Listo! Abre los archivos HTML en tu navegador para ver los mapas.\n")


if __name__ == "__main__":
    main()
