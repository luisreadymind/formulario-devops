#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para corregir las inconsistencias entre preguntas tropicalizadas y opciones de respuesta
en el cuestionario DevOps
"""

import json
import sys
from typing import Dict, Any

def corregir_inconsistencias(cuestionario: Dict[str, Any]) -> Dict[str, Any]:
    """
    Corrige las inconsistencias encontradas en el cuestionario tropicalizado
    """
    
    # Correcciones específicas por pregunta
    correcciones = {
        # Área A - Planificación y Gestión Ágil
        "A2": {
            "texto": "¿De qué manera su equipo decide qué tareas y características son más importantes y en qué orden deben desarrollarse en la lista de trabajo pendiente?",
            "opciones": [
                {"id": "A2O1", "texto": "Ordenamiento por prioridad con reglas claras y documentadas"},
                {"id": "A2O2", "texto": "Metodología de priorización como MoSCoW (Must/Should/Could/Won't) o WSJF bien documentada"},
                {"id": "A2O3", "texto": "Priorización decidida por un grupo de personas según cada situación"},
                {"id": "A2O4", "texto": "Se prioriza por urgencia o dependencias sin seguir un método específico"},
                {"id": "A2OTRO", "texto": "Otro (especificar)", "otroCampoId": "A2OTRO_TEXTO"},
                {"id": "A2NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        # Área B - Código y Control de Versiones
        "B2": {
            "texto": "¿Qué estrategia utiliza su equipo para organizar y gestionar las ramas (branches) del código en el repositorio?",
            "opciones": [
                {"id": "B2O1", "texto": "Trunk-Based Development con feature flags"},
                {"id": "B2O2", "texto": "GitFlow adaptado a las necesidades del equipo"},
                {"id": "B2O3", "texto": "GitHub Flow (rama principal + ramas de características)"},
                {"id": "B2O4", "texto": "Release branches (ramas específicas para cada versión)"},
                {"id": "B2OTRO", "texto": "Otro (especificar)", "otroCampoId": "B2OTRO_TEXTO"},
                {"id": "B2NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B3": {
            "texto": "¿Qué políticas de protección tiene implementadas su equipo para controlar los cambios en las ramas principales del código?",
            "opciones": [
                {"id": "B3O1", "texto": "Aprobaciones mínimas requeridas para cambios"},
                {"id": "B3O2", "texto": "Protección de ramas principales (branch protection)"},
                {"id": "B3O3", "texto": "Verificaciones de estado obligatorias (status checks)"},
                {"id": "B3O4", "texto": "Fusión automática con colas de integración (auto-merge/merge queues)"},
                {"id": "B3OTRO", "texto": "Otro (especificar)", "otroCampoId": "B3OTRO_TEXTO"},
                {"id": "B3NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B4": {
            "texto": "¿Qué herramientas utiliza su equipo para analizar automáticamente la calidad y seguridad del código?",
            "opciones": [
                {"id": "B4O1", "texto": "SonarQube o SonarCloud para análisis de calidad"},
                {"id": "B4O2", "texto": "CodeQL para análisis de seguridad"},
                {"id": "B4O3", "texto": "Semgrep para detección de vulnerabilidades"},
                {"id": "B4O4", "texto": "Análisis de cobertura de pruebas (Cobertura/JaCoCo)"},
                {"id": "B4OTRO", "texto": "Otro (especificar)", "otroCampoId": "B4OTRO_TEXTO"},
                {"id": "B4NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B5": {
            "texto": "¿Qué estándares de codificación y herramientas de formateo utiliza su equipo para mantener la consistencia del código?",
            "opciones": [
                {"id": "B5O1", "texto": "Herramientas de linting (ESLint, flake8, etc.)"},
                {"id": "B5O2", "texto": "Pre-commit hooks para validación automática"},
                {"id": "B5O3", "texto": "Estándares de codificación definidos por lenguaje"},
                {"id": "B5O4", "texto": "No hay estándares definidos"},
                {"id": "B5OTRO", "texto": "Otro (especificar)", "otroCampoId": "B5OTRO_TEXTO"},
                {"id": "B5NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B6": {
            "texto": "¿Dónde guarda su equipo los archivos compilados, librerías y componentes reutilizables que genera durante el desarrollo?",
            "opciones": [
                {"id": "B6O1", "texto": "Azure Artifacts"},
                {"id": "B6O2", "texto": "GitHub Packages"},
                {"id": "B6O3", "texto": "JFrog Artifactory"},
                {"id": "B6O4", "texto": "Nexus Repository"},
                {"id": "B6OTRO", "texto": "Otro (especificar)", "otroCampoId": "B6OTRO_TEXTO"},
                {"id": "B6NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B7": {
            "texto": "¿Qué elementos de su proyecto tienen control de versiones para rastrear cambios y mantener un historial de modificaciones?",
            "opciones": [
                {"id": "B7O1", "texto": "Código de la aplicación"},
                {"id": "B7O2", "texto": "Infraestructura como código (Bicep/Terraform/ARM)"},
                {"id": "B7O3", "texto": "Pipelines de CI/CD (archivos YAML)"},
                {"id": "B7O4", "texto": "Configuración como código"},
                {"id": "B7OTRO", "texto": "Otro (especificar)", "otroCampoId": "B7OTRO_TEXTO"},
                {"id": "B7NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B8": {
            "texto": "¿Utiliza su equipo herramientas de inteligencia artificial para ayudar a escribir código de manera más segura y eficiente?",
            "opciones": [
                {"id": "B8O1", "texto": "GitHub Copilot"},
                {"id": "B8O2", "texto": "Azure AI Studio integrado en el flujo de desarrollo"},
                {"id": "B8O3", "texto": "Modelos de IA internos o personalizados"},
                {"id": "B8O4", "texto": "No utilizamos IA para desarrollo"},
                {"id": "B8OTRO", "texto": "Otro (especificar)", "otroCampoId": "B8OTRO_TEXTO"},
                {"id": "B8NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B9": {
            "texto": "¿Todos los cambios importantes en el código son revisados por otros desarrolladores antes de ser incluidos en el proyecto principal?",
            "opciones": [
                {"id": "B9O1", "texto": "Sí, es una política obligatoria"},
                {"id": "B9O2", "texto": "Parcialmente, solo algunos cambios"},
                {"id": "B9O3", "texto": "Manual, a discreción del desarrollador"},
                {"id": "B9O4", "texto": "No se hacen revisiones de código"},
                {"id": "B9OTRO", "texto": "Otro (especificar)", "otroCampoId": "B9OTRO_TEXTO"},
                {"id": "B9NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "B10": {
            "texto": "¿Cómo gestiona su equipo las librerías externas que utiliza el proyecto y mantiene un inventario de todos los componentes de software?",
            "opciones": [
                {"id": "B10O1", "texto": "Dependabot/Renovate con generación de SBOM (Software Bill of Materials)"},
                {"id": "B10O2", "texto": "Solo actualizaciones manuales de dependencias"},
                {"id": "B10O3", "texto": "Auditoría esporádica de componentes"},
                {"id": "B10O4", "texto": "No se gestiona activamente"},
                {"id": "B10OTRO", "texto": "Otro (especificar)", "otroCampoId": "B10OTRO_TEXTO"},
                {"id": "B10NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        # Área C - CI/CD
        "C2": {
            "texto": "¿Qué tipo de agentes o servidores utiliza para ejecutar sus pipelines de CI/CD?",
            "opciones": [
                {"id": "C2O1", "texto": "Agentes hospedados por Microsoft"},
                {"id": "C2O2", "texto": "Agentes propios con Windows"},
                {"id": "C2O3", "texto": "Agentes propios con Linux"},
                {"id": "C2O4", "texto": "Escalado automático en AKS/VMSS"},
                {"id": "C2OTRO", "texto": "Otro (especificar)", "otroCampoId": "C2OTRO_TEXTO"},
                {"id": "C2NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "C3": {
            "texto": "¿Qué estrategias utiliza su equipo para desplegar nuevas versiones de manera segura y controlada?",
            "opciones": [
                {"id": "C3O1", "texto": "Blue/Green (dos ambientes idénticos)"},
                {"id": "C3O2", "texto": "Canary/Anillos (despliegue gradual)"},
                {"id": "C3O3", "texto": "A/B Testing (pruebas con usuarios)"},
                {"id": "C3O4", "texto": "Rings por región/tenant (despliegue por zonas)"},
                {"id": "C3OTRO", "texto": "Otro (especificar)", "otroCampoId": "C3OTRO_TEXTO"},
                {"id": "C3NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "C4": {
            "texto": "¿Qué controles y aprobaciones tiene implementados en sus pipelines para garantizar la calidad antes del despliegue?",
            "opciones": [
                {"id": "C4O1", "texto": "Gates automáticos de calidad"},
                {"id": "C4O2", "texto": "Aprobaciones manuales por entorno"},
                {"id": "C4O3", "texto": "Verificaciones de calidad previas"},
                {"id": "C4O4", "texto": "Integración con sistemas de gestión de cambios (ServiceNow)"},
                {"id": "C4OTRO", "texto": "Otro (especificar)", "otroCampoId": "C4OTRO_TEXTO"},
                {"id": "C4NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "C5": {
            "texto": "¿En qué tipo de servicios de Azure despliega principalmente sus aplicaciones?",
            "opciones": [
                {"id": "C5O1", "texto": "Azure App Service"},
                {"id": "C5O2", "texto": "AKS (Azure Kubernetes Service)"},
                {"id": "C5O3", "texto": "Azure Functions (Flex/Consumo)"},
                {"id": "C5O4", "texto": "VM Scale Sets/Máquinas Virtuales"},
                {"id": "C5OTRO", "texto": "Otro (especificar)", "otroCampoId": "C5OTRO_TEXTO"},
                {"id": "C5NO", "texto": "No implementado / No aplica"}
            ]
        },
        
        "C6": {
            "texto": "¿Cómo protege y gestiona su equipo las contraseñas, claves API y otra información sensible utilizada por las aplicaciones?",
            "opciones": [
                {"id": "C6O1", "texto": "Azure Key Vault"},
                {"id": "C6O2", "texto": "Variables protegidas en pipelines"},
                {"id": "C6O3", "texto": "Environments con permisos específicos"},
                {"id": "C6O4", "texto": "Federated Credentials (OIDC)"},
                {"id": "C6OTRO", "texto": "Otro (especificar)", "otroCampoId": "C6OTRO_TEXTO"},
                {"id": "C6NO", "texto": "No implementado / No aplica"}
            ]
        }
    }
    
    # Aplicar correcciones
    for area in cuestionario["areas"]:
        for pregunta in area["preguntas"]:
            if pregunta["id"] in correcciones:
                correccion = correcciones[pregunta["id"]]
                pregunta["texto"] = correccion["texto"]
                pregunta["opciones"] = correccion["opciones"]
                print(f"✅ Corregida pregunta {pregunta['id']}: {correccion['texto'][:60]}...")
    
    # Actualizar metadata
    cuestionario["metadata"]["version"] = "1.2-corregido"
    cuestionario["metadata"]["fechaActualizacion"] = "2025-11-08"
    cuestionario["metadata"]["cambios"].append("Corrección de inconsistencias entre preguntas y opciones")
    
    return cuestionario

def main():
    """Función principal"""
    try:
        # Cargar cuestionario actual
        with open("cuestionario_devops_azure.json", "r", encoding="utf-8") as f:
            cuestionario = json.load(f)
        
        print("🔍 Analizando inconsistencias en el cuestionario...")
        
        # Corregir inconsistencias
        cuestionario_corregido = corregir_inconsistencias(cuestionario)
        
        # Guardar versión corregida
        with open("cuestionario_devops_azure_corregido.json", "w", encoding="utf-8") as f:
            json.dump(cuestionario_corregido, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Correcciones completadas!")
        print(f"📝 Archivo generado: cuestionario_devops_azure_corregido.json")
        print(f"📊 Versión: {cuestionario_corregido['metadata']['version']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())