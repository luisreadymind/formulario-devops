#!/usr/bin/env python3
"""
🌎 TROPICALIZADOR DE CUESTIONARIO DEVOPS
Actualiza las preguntas del cuestionario para que sean más claras,
explicativas y tropicalizadas al español latinoamericano
"""

import json
import re
from datetime import datetime

class CuestionarioTropicalizador:
    def __init__(self, archivo_entrada, archivo_salida):
        self.archivo_entrada = archivo_entrada
        self.archivo_salida = archivo_salida
        self.preguntas_mejoradas = {
            # SECCIÓN A: Planificación y Gestión Ágil
            "A1": {
                "texto_original": "¿Qué herramienta primaria utiliza para planificación, backlog y sprints?",
                "texto_mejorado": "¿Cuál es la herramienta principal que utiliza su equipo para organizar y planificar el trabajo, crear listas de tareas pendientes (backlog) y gestionar los ciclos de desarrollo (sprints)?"
            },
            "A2": {
                "texto_original": "¿Cómo prioriza y ordena su backlog de producto?",
                "texto_mejorado": "¿De qué manera su equipo decide qué tareas y características son más importantes y en qué orden deben desarrollarse en la lista de trabajo pendiente?"
            },
            "A3": {
                "texto_original": "¿Existe trazabilidad end-to-end Requisito→Commit→Build→Release→Incidente?",
                "texto_mejorado": "¿Pueden seguir el recorrido completo de una funcionalidad desde que se solicita hasta que se entrega, incluyendo los cambios de código, compilación, despliegue y posibles problemas?"
            },
            "A4": {
                "texto_original": "Cadencia de iteraciones/entregas a producción:",
                "texto_mejorado": "¿Con qué frecuencia su equipo entrega nuevas funcionalidades o actualizaciones a los usuarios finales en el ambiente de producción?"
            },
            "A5": {
                "texto_original": "¿Qué prácticas de refinamiento y calidad del backlog utiliza?",
                "texto_mejorado": "¿Qué técnicas utiliza su equipo para revisar, mejorar y mantener organizada la lista de trabajo pendiente (backlog) para asegurar que sea clara y útil?"
            },
            "A6": {
                "texto_original": "¿Qué estándar de gestión de requerimientos utiliza?",
                "texto_mejorado": "¿Qué metodología o framework utiliza su organización para documentar, organizar y gestionar las necesidades y solicitudes de los usuarios?"
            },
            "A7": {
                "texto_original": "¿Cómo gestiona la dependencia entre equipos/tribus?",
                "texto_mejorado": "¿Cómo coordina su equipo el trabajo cuando necesita colaborar con otros equipos o cuando una tarea depende del trabajo de otros grupos?"
            },
            "A8": {
                "texto_original": "¿Qué métricas de delivery revisa de forma periódica?",
                "texto_mejorado": "¿Qué indicadores o números revisa regularmente su equipo para medir qué tan bien está entregando el trabajo y cumpliendo objetivos?"
            },
            "A9": {
                "texto_original": "¿Cómo gestiona riesgos y cambios de alcance?",
                "texto_mejorado": "¿Cómo maneja su equipo los posibles problemas que pueden surgir y los cambios en los requisitos o expectativas del proyecto?"
            },
            "A10": {
                "texto_original": "¿Qué herramienta de documentación viva utiliza?",
                "texto_mejorado": "¿Qué herramienta utiliza para crear y mantener actualizada la documentación del proyecto que siempre refleje el estado actual del desarrollo?"
            },

            # SECCIÓN B: Desarrollo y Calidad del Código
            "B1": {
                "texto_original": "¿Repositorio principal?",
                "texto_mejorado": "¿En qué plataforma principal almacena y gestiona su equipo el código fuente del proyecto?"
            },
            "B2": {
                "texto_original": "¿Dónde se almacenan artefactos y paquetes?",
                "texto_mejorado": "¿Dónde guarda su equipo los archivos compilados, librerías y componentes reutilizables que genera durante el desarrollo?"
            },
            "B3": {
                "texto_original": "¿Qué se versiona?",
                "texto_mejorado": "¿Qué elementos de su proyecto tienen control de versiones para rastrear cambios y mantener un historial de modificaciones?"
            },
            "B4": {
                "texto_original": "¿Uso de IA para desarrollo seguro/productivo?",
                "texto_mejorado": "¿Utiliza su equipo herramientas de inteligencia artificial para ayudar a escribir código de manera más segura y eficiente?"
            },
            "B5": {
                "texto_original": "¿Evidencia de revisión entre pares (peer review) 100% de cambios críticos?",
                "texto_mejorado": "¿Todos los cambios importantes en el código son revisados por otros desarrolladores antes de ser incluidos en el proyecto principal?"
            },
            "B6": {
                "texto_original": "¿Gestión de dependencias y SBOM?",
                "texto_mejorado": "¿Cómo gestiona su equipo las librerías externas que utiliza el proyecto y mantiene un inventario de todos los componentes de software?"
            },

            # SECCIÓN C: CI/CD y Automatización
            "C1": {
                "texto_original": "¿Orquestador CI/CD primario?",
                "texto_mejorado": "¿Cuál es la herramienta principal que utiliza su equipo para automatizar la compilación, pruebas y despliegue de código?"
            },
            "C2": {
                "texto_original": "¿Lenguajes/herramientas IaC utilizados?",
                "texto_mejorado": "¿Qué herramientas utiliza su equipo para definir y gestionar la infraestructura de servidores y servicios mediante código?"
            },
            "C3": {
                "texto_original": "¿Controles de plataforma y gobierno?",
                "texto_mejorado": "¿Qué políticas y controles tiene implementados su organización para asegurar el cumplimiento de estándares y buenas prácticas?"
            },
            "C4": {
                "texto_original": "¿Gestión de secretos?",
                "texto_mejorado": "¿Cómo protege y gestiona su equipo las contraseñas, claves API y otra información sensible utilizada por las aplicaciones?"
            },
            "C5": {
                "texto_original": "¿Gestión de configuración de apps?",
                "texto_mejorado": "¿Cómo maneja su equipo las configuraciones específicas para cada ambiente (desarrollo, pruebas, producción) de las aplicaciones?"
            },
            "C6": {
                "texto_original": "¿Topologías y redes?",
                "texto_mejorado": "¿Cómo está organizada y conectada la infraestructura de red donde funcionan sus aplicaciones y servicios?"
            }
        }
        
        # Opciones también mejoradas con español latinoamericano
        self.opciones_mejoradas = {
            # Términos técnicos más explicativos
            "Stack rank con políticas definidas": "Ordenamiento por prioridad con reglas claras y documentadas",
            "MoSCoW/WSJF documentado": "Metodología de priorización MoSCoW (Must have, Should have, Could have, Won't have) o WSJF documentada",
            "Prioridad por comité ad-hoc": "Priorización decidida por un grupo de personas según la situación",
            "Por dependencia/urgencia sin criterio formal": "Se prioriza por urgencia o dependencias sin seguir un método específico",
            "Completa (automática)": "Seguimiento completo y automatizado",
            "Parcial (manual+automática)": "Seguimiento parcial con procesos manuales y automáticos",
            "Sólo manual": "Seguimiento únicamente manual",
            "Sin trazabilidad": "No hay seguimiento del recorrido de las funcionalidades",
            "Diaria": "Todos los días",
            "Semanal": "Una vez por semana",
            "Quincenal": "Cada dos semanas",
            "Mensual": "Una vez al mes",
            "Trimestral": "Cada tres meses",
            "Sin cadencia fija": "No hay una frecuencia establecida"
        }

    def cargar_cuestionario(self):
        """Carga el cuestionario desde el archivo JSON"""
        with open(self.archivo_entrada, 'r', encoding='utf-8') as file:
            return json.load(file)

    def mejorar_pregunta(self, pregunta):
        """Mejora el texto de una pregunta individual"""
        pregunta_id = pregunta.get('id')
        if pregunta_id in self.preguntas_mejoradas:
            pregunta['texto'] = self.preguntas_mejoradas[pregunta_id]['texto_mejorado']
            pregunta['texto_original'] = self.preguntas_mejoradas[pregunta_id]['texto_original']
        
        # Mejorar opciones
        if 'opciones' in pregunta:
            for opcion in pregunta['opciones']:
                texto_original = opcion['texto']
                if texto_original in self.opciones_mejoradas:
                    opcion['texto'] = self.opciones_mejoradas[texto_original]
                    opcion['texto_original'] = texto_original

        return pregunta

    def tropicalizar_cuestionario(self):
        """Tropicaliza todo el cuestionario"""
        print("🌎 Iniciando tropicalización del cuestionario DevOps...")
        
        # Cargar cuestionario
        cuestionario = self.cargar_cuestionario()
        
        # Actualizar metadata
        cuestionario['metadata']['idioma'] = 'es-LATAM'
        cuestionario['metadata']['version'] = '1.1-tropicalizado'
        cuestionario['metadata']['fechaActualizacion'] = datetime.now().strftime('%Y-%m-%d')
        cuestionario['metadata']['cambios'] = [
            'Preguntas tropicalizadas a español latinoamericano',
            'Lenguaje más claro y explicativo',
            'Reducción de tecnicismos',
            'Mayor claridad en las opciones de respuesta'
        ]
        
        # Mejorar instrucciones
        cuestionario['instrucciones'] = "Seleccione la opción que mejor describa la situación actual de su equipo u organización. Siempre puede elegir 'Otro (especificar)' para casos particulares o 'No implementado / No aplica' cuando no corresponda."
        
        total_preguntas_mejoradas = 0
        
        # Procesar cada área
        for area in cuestionario['areas']:
            print(f"📋 Procesando área: {area['nombre']}")
            
            # Mejorar objetivos de área con lenguaje más claro
            if area['id'] == 'A':
                area['objetivo'] = "Evalúa cómo su equipo planifica, organiza y gestiona el trabajo utilizando metodologías ágiles y herramientas de Azure/GitHub para optimizar el flujo de entrega de valor."
            elif area['id'] == 'B':
                area['objetivo'] = "Evalúa las prácticas de desarrollo de código, control de versiones, calidad y colaboración en equipo."
            elif area['id'] == 'C':
                area['objetivo'] = "Evalúa el nivel de automatización en los procesos de integración continua, despliegue continuo y gestión de infraestructura."
            elif area['id'] == 'D':
                area['objetivo'] = "Evalúa las prácticas de gestión de infraestructura como código y arquitectura en la nube."
            elif area['id'] == 'E':
                area['objetivo'] = "Evalúa las medidas de seguridad implementadas en todo el ciclo de desarrollo y despliegue."
            elif area['id'] == 'F':
                area['objetivo'] = "Evalúa las capacidades de monitoreo, observabilidad y respuesta a incidentes en producción."
            
            # Procesar preguntas del área
            for pregunta in area['preguntas']:
                pregunta_mejorada = self.mejorar_pregunta(pregunta)
                if 'texto_original' in pregunta_mejorada:
                    total_preguntas_mejoradas += 1
                    print(f"  ✅ Mejorada: {pregunta['id']}")

        print(f"\n📊 Resumen de mejoras:")
        print(f"  • Total de preguntas mejoradas: {total_preguntas_mejoradas}")
        print(f"  • Idioma actualizado: {cuestionario['metadata']['idioma']}")
        print(f"  • Versión: {cuestionario['metadata']['version']}")
        
        return cuestionario

    def guardar_cuestionario(self, cuestionario):
        """Guarda el cuestionario tropicalizado"""
        with open(self.archivo_salida, 'w', encoding='utf-8') as file:
            json.dump(cuestionario, file, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Cuestionario tropicalizado guardado en: {self.archivo_salida}")

    def ejecutar_tropicalizacion(self):
        """Ejecuta el proceso completo de tropicalización"""
        print("🚀 Iniciando proceso de tropicalización...")
        
        cuestionario_mejorado = self.tropicalizar_cuestionario()
        self.guardar_cuestionario(cuestionario_mejorado)
        
        print("\n🎉 ¡Tropicalización completada exitosamente!")
        print("\n📋 Los cambios incluyen:")
        print("  ✅ Preguntas más claras y explicativas")
        print("  ✅ Español latinoamericano")
        print("  ✅ Menos tecnicismos")
        print("  ✅ Mejor comprensión para usuarios no técnicos")
        
        return True

if __name__ == "__main__":
    # Configurar archivos
    archivo_entrada = "cuestionario_devops_azure.json"
    archivo_salida = "cuestionario_devops_azure_tropicalizado.json"
    
    # Ejecutar tropicalización
    tropicalizador = CuestionarioTropicalizador(archivo_entrada, archivo_salida)
    tropicalizador.ejecutar_tropicalizacion()
    
    print(f"\n🔄 Para aplicar los cambios, ejecute:")
    print(f"   mv {archivo_salida} {archivo_entrada}")
    print(f"   # O copie el contenido manualmente")