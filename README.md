<div align="center">
  <img src="HorusSlogan.png" alt="Horus Space Lab" width="720">

  # Banco de Pruebas 2026

  ### Telemetría, visualización y análisis de ensayos de motores de cohete

  ![Versión BETA](https://img.shields.io/badge/versi%C3%B3n-BETA-e63946?style=for-the-badge)
  ![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)

  **Horus Space Lab**
</div>

> [!WARNING]
> **Versión BETA:** la aplicación todavía está en desarrollo y puede contener errores o cambiar. Verifica los datos y los procedimientos antes de cada ensayo.

Aplicación de escritorio para recibir telemetría de un banco de pruebas, visualizar empuje e impulso en tiempo real y guardar o comparar los resultados de cada ensayo.

## Contenido

- [Funciones](#funciones)
- [Requisitos e instalación](#requisitos-e-instalación)
- [Puesta en marcha](#puesta-en-marcha)
- [Flujo de operación](#flujo-de-operación)
- [Telemetría y archivos](#telemetría-y-archivos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Seguridad](#seguridad)

## Funciones

- **Conexión flexible:** recibe telemetría por cable, LoRa o WiFi/UDP.
- **Vista en vivo:** grafica el empuje y el impulso acumulado, con lectura de coordenadas sobre la curva.
- **Lecturas más claras:** aplica un filtro de mediana de 5 muestras y un umbral de empuje para reducir picos y ruido.
- **Indicadores del ensayo:** muestra empuje actual y máximo, impulso, clase NAR, señal y paquetes perdidos.
- **Unidades configurables:** alterna entre Newtons y kilogramos-fuerza.
- **Gestión de resultados:** tara la celda de carga, recorta intervalos, recalcula el impulso del intervalo y exporta CSV.
- **Guardado automático:** elige una carpeta para guardar los ensayos.
- **Comparación de ensayos:** carga dos CSV en `ANALIZAR`, superpone sus curvas y compara los cambios porcentuales de empuje máximo e impulso.
- **Protección de ignición:** exige armar el sistema y confirmar un código temporal de cuatro dígitos antes de enviar `FIRE`.

## Requisitos e instalación

- Python 3.9 o superior.
- Una fuente de telemetría y un sistema de adquisición compatibles.

Instala las dependencias desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
```

## Puesta en marcha

Inicia la aplicación:

```bash
python main.py
```

Ejecuta las pruebas automatizadas:

```bash
python -m pytest -q
```

## Flujo de operación

1. Inicia Horus y selecciona el modo de conexión: `Cable`, `LoRa` o `WiFi`.
2. Conecta la fuente de telemetría. En modo WiFi, la aplicación escucha por UDP en el puerto `8888`.
3. Con la celda de carga sin peso, pulsa `TARE` para establecer el cero.
4. Inicia la adquisición. El guardado automático creará un CSV en la carpeta configurada con `CARPETA CSV`.
5. Exporta el ensayo completo o selecciona un intervalo para guardar solo una parte.
6. Abre `ANALIZAR`, carga los archivos CSV como ensayo A y ensayo B y compara sus curvas y métricas.

## Telemetría y archivos

Los paquetes binarios contienen el empuje como un `float` de 4 bytes y un número de secuencia `uint32` de 4 bytes. La secuencia permite detectar paquetes perdidos; en modo LoRa se añade el RSSI.

Los CSV exportados incluyen tiempo, empuje en Newtons y kilogramos-fuerza. Los CSV recortados también incluyen el impulso acumulado, recalculado desde el inicio del intervalo seleccionado.

## Estructura del proyecto

```text
BancoDePruebas2026/
├── communication/  Lectores serie y UDP, protocolos de conexión
├── config/         Constantes, estilos, configuración y clases NAR
├── core/           Procesamiento, filtrado, integración y clasificación
├── persistence/    Autoguardado, carga y exportación CSV
├── ui/             Ventana principal, diálogos y widgets PyQt6
├── tests/          Pruebas automatizadas
├── main.py         Punto de entrada
└── requirements.txt
```

## Seguridad

La confirmación por código ayuda a reducir activaciones accidentales, pero **no sustituye los procedimientos físicos de seguridad**. Antes de armar el sistema, verifica el área de prueba, las conexiones y el relevador, y asegúrate de que no haya personas dentro de la zona de riesgo.

## Empaquetado

Para empaquetar con PyInstaller, usa `main.py` como punto de entrada e incluye los recursos gráficos necesarios, como `HSL_transparent.png`.
