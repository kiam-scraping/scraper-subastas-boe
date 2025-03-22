# scraper-subastas-boe
Scraper automatizado para extraer datos de subastas judiciales activas en el BOE (España)

# 🏛️ Scraper de Subastas Judiciales del BOE

Proyecto de scraping real usando Python para extraer datos del portal oficial de subastas del BOE (Boletín Oficial del Estado, España). Este script automatiza la recolección de datos de todas las subastas activas de bienes inmuebles, extrayendo detalles como valor de tasación, situación posesoria, ubicación, tipo de bien y más.

## 🚀 Tecnologías utilizadas

- `requests` para realizar peticiones HTTP
- `BeautifulSoup` para parsear el HTML
- `random` para rotación de User-Agents
- `csv` para guardar los datos estructurados

## ⚙️ Características del scraper

- Recorre automáticamente todas las páginas de subastas activas
- Extrae datos clave de cada subasta individual
- Evita bloqueos con rotación de headers
- Genera un CSV con columnas dinámicas
- Preparado para ser analizado fácilmente con `pandas`

## 📁 Archivos

- `scraper_boe.py` → script principal
- `13. subastas_basico.csv` → ejemplo de salida con subastas reales
- `README.md` → este archivo

## 🧠 Casos de uso

- Análisis de oportunidades de inversión
- Exploración del mercado judicial de inmuebles
- Filtrado por ocupación, valor, ubicación o tipo de subasta
- Proyecto de portfolio para scraping freelance

## 🧪 Próximos pasos

- Añadir limpieza de datos con `pandas`
- Visualización de datos: subastas por ciudad, valor medio, etc.
- Filtros avanzados (sin ocupantes, con mayor diferencia de valor vs puja mínima)

## ⚠️ Notas técnicas

Este scraper está optimizado para funcionar sin proxies, gracias a la rotación de `User-Agent`. En pruebas reales ha sido capaz de extraer más de 800 subastas sin bloqueos.

Sin embargo, si el portal del BOE implementa restricciones más agresivas (bloqueo por IP o frecuencia de peticiones), es posible que se requiera:

- Añadir pausas entre peticiones con `time.sleep()`
- Integrar proxies rotativos o servicios como ScraperAPI

El script está estructurado para facilitar estas mejoras en caso de ser necesarias.


## ✍️ Autor

Proyecto creado por **Kiam** [`@kiam-scraping`](https://github.com/kiam-scraping)

---

