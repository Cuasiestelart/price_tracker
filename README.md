# 📉 Automated Price Tracker & Alert System

![Python](https://img.shields.io/badge/Python-3.11+-blue?logo=python&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?logo=supabase&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-CI%2FCD-2088FF?logo=github-actions&logoColor=white)

Pipeline automatizado en Python para el monitoreo periódico de precios en línea, almacenamiento histórico en base de datos en la nube (Supabase) y envío automático de alertas por correo electrónico cuando se detectan caídas de precio o condiciones objetivo.

---

## Características Principales

* **Extracción y Monitoreo Automatizado:** Scraping y consulta periódica de precios y disponibilidad de productos configurados.
* **Persistencia en la Nube (Supabase / PostgreSQL):** Almacenamiento histórico de precios y catálogo de productos gestionado mediante cliente dedicado (`supabase_client.py`).
* **Sistema de Alertas Inteligentes:** Evaluación automática de umbrales de precio y envío de notificaciones por correo electrónico (`notifier.py`).
* **Ejecución Serverless Programada (CI/CD):** Flujo automatizado mediante **GitHub Actions** ejecutándose cada **6 horas** sin necesidad de servidores dedicados encendidos.
* **Gestión de Catálogo:** Script auxiliar (`add.product.py`) para dar de alta nuevos productos y precios objetivo de forma sencilla.

---

## Stack Tecnológico

* **Lenguaje:** Python
* **Base de Datos & Backend Cloud:** Supabase (PostgreSQL)
* **Automatización & CI/CD:** GitHub Actions (Cron jobs cada 6h)
* **Notificaciones:** SMTP / Email Automation

---

## Arquitectura del Proyecto

    price_tracker/
    ├── .github/workflows/    # Pipelines de automatización (ejecución cada 6 horas)
    ├── config/               # Configuraciones y parámetros de monitoreo
    ├── src/                  # Módulos principales de extracción y lógica de negocio
    ├── add.product.py        # Script para registrar nuevos productos a monitorear
    ├── database.py           # Operaciones y consultas hacia la base de datos
    ├── supabase_client.py    # Conexión y cliente de Supabase
    ├── notifier.py           # Módulo de envío de alertas por correo
    ├── main.py               # Orquestador principal del pipeline
    └── requirements.txt      # Dependencias del proyecto

---

## Instalación y Uso Local

1. **Clonar el repositorio e instalar dependencias:**

       git clone https://github.com/Cuasiestelart/price_tracker.git
       cd price_tracker
       pip install -r requirements.txt

2. **Configurar variables de entorno:**  
   Definir las credenciales de conexión a Supabase (`SUPABASE_URL`, `SUPABASE_KEY`) y credenciales SMTP para las alertas en el entorno local o en los *Secrets* de GitHub Actions.

3. **Ejecutar el rastreador manualmente:**

       python main.py