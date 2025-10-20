# 🗺️ Análisis de Google Maps Reviews

Sistema completo de análisis de unidades económicas usando la API de Google Maps. Identifica los mejores y peores negocios basándose en ratings, genera mapas de calor interactivos y crea análisis de texto mediante word clouds.

## 📋 Características

- ✅ Búsqueda de negocios usando Google Places API
- ⭐ Identificación de las 10-15 mejores unidades económicas por rating
- ⚠️ Identificación de las 10-15 peores unidades económicas por rating
- 📊 Análisis del número de reviews/votaciones
- 🗺️ Mapas de calor interactivos con Folium
- ☁️ Word clouds de comentarios positivos y negativos
- 📈 Reportes estadísticos visuales
- 💾 Exportación de datos a CSV

## 🚀 Instalación

### 1. Clonar o acceder al proyecto

```bash
cd /Users/enriquepablos/Documents/escuela/ultima/maps_review
```

### 2. Activar el entorno virtual

```bash
source .venv/bin/activate
```

### 3. Verificar dependencias instaladas

Las dependencias ya están instaladas. Si necesitas reinstalarlas:

```bash
uv pip install -r requirements.txt
```

## 🔑 Configuración de Google Maps API

### Paso 1: Obtener API Key

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente
3. Habilita las siguientes APIs:
   - **Places API** (necesaria)
   - **Maps JavaScript API** (necesaria)
   - **Geocoding API** (opcional)

4. Ve a **Credenciales** → **Crear credenciales** → **Clave de API**
5. Copia tu API Key

### Paso 2: Configurar archivo .env

1. Copia el archivo de ejemplo:
```bash
cp .env.example .env
```

2. Edita `.env` y agrega tu API Key:
```bash
GOOGLE_MAPS_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

⚠️ **IMPORTANTE**: Nunca compartas tu API Key públicamente ni la subas a repositorios.

### Paso 3: Configurar restricciones de API Key (recomendado)

En Google Cloud Console:
- Restringe tu API Key a las APIs habilitadas
- Considera agregar restricciones por IP o dominio
- Establece cuotas de uso para evitar cargos inesperados

## ⚙️ Configuración del Análisis

Edita las variables en `main.py` (líneas 302-304) según tu necesidad:

```python
QUERY = "restaurante"  # Tipo de negocio: 'hotel', 'cafetería', 'gimnasio', etc.
LOCATION = (25.6866142, -100.3161126)  # Coordenadas (lat, lng)
RADIUS = 5000  # Radio de búsqueda en metros (máx: 50000)
```

### Cómo obtener coordenadas:

1. **Google Maps**: 
   - Haz clic derecho en el mapa → Primera opción muestra las coordenadas
   
2. **Terminal**:
   ```python
   # En Python:
   import googlemaps
   gmaps = googlemaps.Client(key='TU_API_KEY')
   result = gmaps.geocode('Monterrey, México')
   print(result[0]['geometry']['location'])
   ```

## 🏃‍♂️ Uso

### Ejecutar análisis completo

```bash
python3 main.py
```

El script realizará:

1. 🔍 Búsqueda de negocios en el área especificada
2. 📊 Recopilación de ratings y reviews
3. ⭐ Identificación de mejores y peores negocios
4. 🗺️ Generación de mapas de calor interactivos
5. ☁️ Creación de word clouds
6. 📈 Generación de reportes estadísticos
7. 💾 Exportación de datos

### Archivos generados

```
maps_review/
├── mapa_mejores_negocios.html    # Mapa interactivo de mejores negocios
├── mapa_peores_negocios.html     # Mapa interactivo de peores negocios
├── wordcloud_mejores.png         # Word cloud de reviews positivas
├── wordcloud_peores.png          # Word cloud de reviews negativas
├── analisis_estadistico.png      # Gráficos estadísticos
└── datos_negocios.csv            # Datos completos exportados
```

## 📊 Interpretación de Resultados

### Mapas de Calor

Los mapas HTML muestran:
- **Marcadores verdes**: Mejores negocios (rating alto)
- **Marcadores rojos**: Peores negocios (rating bajo)
- **Intensidad del calor**: Basada en número de reviews
- **Popup**: Información detallada al hacer clic

### Word Clouds

Las nubes de palabras muestran:
- **Tamaño de palabra**: Frecuencia de aparición
- **Color verde/viridis**: Reviews positivas
- **Color rojo**: Reviews negativas
- Palabras comunes (stopwords) están excluidas

### Análisis Estadístico

El reporte incluye:
1. **Distribución de ratings**: Histograma general
2. **Top 15 mejores**: Ranking de mejores negocios
3. **Top 15 peores**: Ranking de peores negocios
4. **Rating vs Reviews**: Correlación entre calificación y cantidad

## 🔧 Personalización Avanzada

### Modificar número de resultados

En `main.py`, línea 315:

```python
analyzer.search_places(QUERY, LOCATION, RADIUS, max_results=100)  # Default: 60
```

### Cambiar número de top/worst

En `main.py`, líneas 321-322:

```python
top_businesses = analyzer.get_top_businesses(20)  # Default: 15
worst_businesses = analyzer.get_worst_businesses(20)  # Default: 15
```

### Ajustar filtros de reviews

En `main.py`, línea 117 (método `get_worst_businesses`):

```python
df_filtered = df_filtered[df_filtered['total_ratings'] >= 5]  # Default: 3
```

### Personalizar word clouds

En `main.py`, líneas 208-217:

```python
wordcloud = WordCloud(
    width=2000,           # Ancho en píxeles
    height=1000,          # Alto en píxeles
    max_words=150,        # Número máximo de palabras
    colormap='Blues',     # Esquema de colores
    background_color='white'
)
```

## 📦 Dependencias Principales

- **googlemaps**: Cliente Python para Google Maps API
- **pandas**: Análisis y manipulación de datos
- **folium**: Mapas interactivos
- **wordcloud**: Generación de nubes de palabras
- **matplotlib**: Visualizaciones estadísticas
- **seaborn**: Gráficos estadísticos mejorados

## 🐛 Solución de Problemas

### Error: "API key not found"

```bash
# Verifica que el archivo .env existe y contiene la API key
cat .env
```

### Error: "REQUEST_DENIED"

- Verifica que Places API está habilitada en Google Cloud Console
- Revisa las restricciones de tu API Key
- Confirma que tienes créditos disponibles

### Error: "OVER_QUERY_LIMIT"

- Has excedido el límite de consultas
- Reduce `max_results` en la búsqueda
- Agrega `time.sleep()` más largo entre peticiones
- Considera activar facturación en Google Cloud

### No se generan word clouds

- Las reviews están en diferentes idiomas
- Ajusta `stopwords` en el código
- Verifica que hay suficientes reviews para analizar

### Mapas no se visualizan

- Abre los archivos `.html` en un navegador web
- No funcionarán correctamente abriendo el archivo local en algunos navegadores
- Considera usar un servidor local: `python3 -m http.server`

## 💡 Ejemplos de Uso

### Análisis de hoteles en Ciudad de México

```python
QUERY = "hotel"
LOCATION = (19.4326, -99.1332)  # CDMX
RADIUS = 10000  # 10km
```

### Análisis de cafeterías en Guadalajara

```python
QUERY = "cafetería"
LOCATION = (20.6597, -103.3496)  # GDL
RADIUS = 3000  # 3km
```

### Análisis de gimnasios en tu ubicación

```python
QUERY = "gimnasio"
LOCATION = (TU_LAT, TU_LNG)
RADIUS = 5000
```

## 📄 Licencia

Este proyecto es para uso educativo y análisis de datos.

## 🤝 Contribuciones

Para mejoras o sugerencias:
1. Analiza el código en `main.py`
2. Prueba tus cambios localmente
3. Documenta las modificaciones

## 📞 Soporte

Para problemas con:
- **Google Maps API**: [Documentación oficial](https://developers.google.com/maps/documentation)
- **Python/Dependencias**: Revisa la documentación de cada librería
- **Errores del código**: Revisa los mensajes de error en la consola

---

**Última actualización**: Octubre 2025

¡Feliz análisis! 🎉
