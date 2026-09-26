# Horus Space Lab — Sistema de Telemetría

Este proyecto contiene el software del orquestador y la interfaz de usuario (Dashboard) para la recolección, visualización y análisis de telemetría de banco de pruebas de motores de cohetes.

## Descripción
El **Horus Telemetry Dashboard** permite la adquisición de datos de empuje (thrust) provenientes de un banco de pruebas. Utiliza PyQt6 para proporcionar una visualización en tiempo real a través de gráficos integrados y tarjetas de indicadores de rendimiento (KPIs), junto con clasificación automática del motor probado según los estándares de la NAR.

## Estructura del Proyecto

```
InterfazBancoqueNoBanquea/
│
├── config/              # Configuraciones de estilos, constantes y clases de motor
├── core/                # Lógica central: Motores de telemetría y clasificadores
├── communication/       # Gestión de protocolos de comunicación Serial/LoRa
├── persistence/         # Exportación CSV y autoguardado de telemetría
├── ui/                  # Componentes de interfaz gráfica (widgets y ventanas)
├── utils/               # Utilidades misceláneas
├── tests/               # Pruebas automatizadas (pytest)
├── main.py              # Punto de entrada de la aplicación
└── requirements.txt     # Dependencias del sistema
```

## Requisitos y Configuración

El proyecto requiere Python 3.9 o superior. Puedes instalar las dependencias con:

```bash
pip install -r requirements.txt
```

## Uso

Para ejecutar la aplicación, corre el script principal:

```bash
python main.py
```

*Nota para compilación con PyInstaller: Utilizar `main.py` como el punto de entrada principal.*

## Modos de Conexión
La interfaz cuenta con dos métodos de conexión soportados:
- **CABLE/RS-485:** Comunicación de latencia ultrabaja para bancos adyacentes al equipo.
- **LoRa:** Transmisión a largo alcance, incorporando información extra sobre la intensidad de la señal y paquetes perdidos, además de funciones para iniciar/detener telemetría de forma inalámbrica de forma explícita.

## Características
- Visualización de Empuje e Impulso Total en tiempo real (PyQtGraph)
- Clasificación Automática según la Asociación Nacional de Cohetería (NAR)
- Autoguardado e historial en archivos CSV
- Conversión instantánea entre Newtons y Kilogramos-Fuerza
- Sistema seguro de ignición remota ("Armado" y "Fuego")
- Pruebas integradas de componentes

# BancoDePruebas2026
