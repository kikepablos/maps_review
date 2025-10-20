# ⚡ Guía Rápida de Inicio

## 🚀 Inicio Rápido (5 minutos)

### 1️⃣ Obtener API Key de Google Maps

1. Ve a: https://console.cloud.google.com/
2. Crea un proyecto nuevo
3. Habilita **Places API**
4. Crea una **API Key** en Credenciales

### 2️⃣ Configurar el proyecto

```bash
# Activar entorno virtual
source .venv/bin/activate

# Configurar API Key (opción 1: script interactivo)
python3 setup.py

# O configurar manualmente (opción 2)
cp .env.example .env
# Edita .env y agrega tu API Key
```

### 3️⃣ Probar la API

```bash
python3 setup.py test
```

### 4️⃣ Ejecutar análisis

```bash
python3 main.py
```

## 📊 Resultados

El análisis genera automáticamente:

- `mapa_mejores_negocios.html` - Mapa interactivo
- `mapa_peores_negocios.html` - Mapa interactivo  
- `wordcloud_mejores.png` - Nube de palabras
- `wordcloud_peores.png` - Nube de palabras
- `analisis_estadistico.png` - Gráficos
- `datos_negocios.csv` - Datos completos

## ⚙️ Personalizar Búsqueda

Edita `main.py` líneas 302-304:

```python
QUERY = "restaurante"                    # ← Cambia el tipo
LOCATION = (25.6866, -100.3161)         # ← Cambia ubicación
RADIUS = 5000                            # ← Cambia radio (metros)
```

## 💡 Ver Ejemplos

```bash
# Ver ejemplos predefinidos
python3 ejemplos.py

# Ver coordenadas de ciudades
python3 ejemplos.py coords
```

## 🆘 Problemas Comunes

### Error: "API key not found"
```bash
cat .env  # Verifica que existe y tiene la key
```

### Error: "REQUEST_DENIED"
- Verifica que Places API está habilitada
- Revisa restricciones de la API Key

### No aparecen resultados
- Aumenta el RADIUS
- Cambia el QUERY a algo más general
- Verifica las coordenadas de LOCATION

## 📚 Más Información

- README completo: `README.md`
- Ejemplos detallados: `ejemplos.py`
- Configuración: `setup.py`

---

**¿Listo?** Ejecuta `python3 main.py` y obtén tu análisis completo. 🎉
