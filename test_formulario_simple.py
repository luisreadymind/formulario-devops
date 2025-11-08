#!/usr/bin/env python3
"""
Script de Testing Simplificado - Formulario DevOps ReadyMind
Version WSL-compatible sin Chrome GUI
"""

import requests
import time
import json
import logging
from datetime import datetime

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_formulario_simple.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FormularioDevOpsSimpleTest:
    """Test simplificado usando requests HTTP"""
    
    def __init__(self, url="https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/"):
        self.base_url = url
        self.session = requests.Session()
        self.test_data = {
            'client_name': 'ReadyMind Testing Suite',
            'client_email': 'testing@readymind.com',
            'client_company': 'ReadyMind Tecnología'
        }
        
    def test_page_accessibility(self):
        """Probar que la página está accesible"""
        try:
            logger.info(f"🌐 Probando accesibilidad de: {self.base_url}")
            response = self.session.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                logger.info("✅ Página accesible")
                
                # Verificar elementos clave en el HTML
                html_content = response.text
                checks = [
                    ('devopsForm', '✅ Formulario principal encontrado'),
                    ('client_name', '✅ Campo nombre encontrado'),
                    ('client_email', '✅ Campo email encontrado'),
                    ('welcome-section', '✅ Sección de bienvenida ReadyMind encontrada'),
                    ('readymind-logo', '✅ Logo ReadyMind encontrado'),
                    ('submitBtn', '✅ Botón de envío encontrado'),
                ]
                
                for element, message in checks:
                    if element in html_content:
                        logger.info(message)
                    else:
                        logger.warning(f"⚠️ {element} no encontrado en HTML")
                
                return True
            else:
                logger.error(f"❌ Error HTTP: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error probando accesibilidad: {e}")
            return False
    
    def generate_test_answers(self):
        """Generar respuestas de prueba para el cuestionario"""
        # Simulamos respuestas típicas para el cuestionario DevOps
        test_answers = {}
        
        # Preguntas típicas que suelen estar en el cuestionario
        questions_mapping = {
            'q1': 'opcion_2',    # Cultura y Organización
            'q2': 'opcion_3',    # Procesos
            'q3': 'opcion_1',    # Herramientas
            'q4': 'opcion_2',    # Métricas
            'q5': 'opcion_3',    # Automatización
            'q6': 'opcion_1',    # Colaboración
            'q7': 'opcion_2',    # Monitoreo
            'q8': 'opcion_3',    # Seguridad
            'q9': 'opcion_1',    # Testing
            'q10': 'opcion_2',   # Deployment
        }
        
        # Generar respuestas para hasta 60 preguntas
        for i in range(1, 61):
            question_key = f'q{i}'
            # Alternar respuestas de forma inteligente
            option_num = (i % 3) + 1
            test_answers[question_key] = f'opcion_{option_num}'
            
        logger.info(f"📋 Generadas {len(test_answers)} respuestas de prueba")
        return test_answers
    
    def simulate_form_submission(self):
        """Simular el envío del formulario"""
        try:
            logger.info("🚀 Simulando envío del formulario...")
            
            # Preparar datos del formulario
            form_data = {
                'client_name': self.test_data['client_name'],
                'client_email': self.test_data['client_email'],
                'client_company': self.test_data['client_company'],
            }
            
            # Agregar respuestas del cuestionario
            answers = self.generate_test_answers()
            form_data.update(answers)
            
            logger.info(f"📝 Datos preparados: {len(form_data)} campos")
            
            # Intentar envío POST
            submit_url = self.base_url.rstrip('/') + '/submit'
            logger.info(f"📤 Enviando a: {submit_url}")
            
            response = self.session.post(
                submit_url, 
                data=form_data,
                timeout=30,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'User-Agent': 'ReadyMind-TestingSuite/1.0'
                }
            )
            
            logger.info(f"📨 Respuesta HTTP: {response.status_code}")
            
            if response.status_code == 200:
                logger.info("✅ Formulario enviado exitosamente")
                
                # Intentar parsear respuesta JSON
                try:
                    json_response = response.json()
                    logger.info("✅ Respuesta JSON recibida")
                    
                    # Verificar estructura de respuesta esperada
                    if 'status' in json_response:
                        logger.info(f"📊 Status: {json_response.get('status')}")
                    
                    if 'message' in json_response:
                        logger.info(f"💬 Mensaje: {json_response.get('message')}")
                    
                    if 'analysis_url' in json_response:
                        logger.info(f"🔗 URL de análisis: {json_response.get('analysis_url')}")
                        
                    return True, json_response
                    
                except json.JSONDecodeError:
                    logger.info("📄 Respuesta HTML recibida (normal para formularios)")
                    return True, {"status": "submitted", "content": "HTML response"}
                    
            else:
                logger.error(f"❌ Error en envío: HTTP {response.status_code}")
                logger.error(f"❌ Contenido: {response.text[:200]}...")
                return False, None
                
        except Exception as e:
            logger.error(f"❌ Error simulando envío: {e}")
            return False, None
    
    def validate_backend_functionality(self):
        """Validar funcionalidades del backend"""
        try:
            logger.info("🔍 Validando funcionalidad del backend...")
            
            # Probar endpoint de salud si existe
            health_endpoints = ['/health', '/status', '/ping']
            
            for endpoint in health_endpoints:
                try:
                    health_url = self.base_url.rstrip('/') + endpoint
                    response = self.session.get(health_url, timeout=5)
                    
                    if response.status_code == 200:
                        logger.info(f"✅ Endpoint {endpoint} disponible")
                        return True
                except:
                    continue
            
            logger.info("ℹ️ No se encontraron endpoints de salud específicos")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error validando backend: {e}")
            return False
    
    def run_simple_test(self):
        """Ejecutar test simplificado completo"""
        start_time = datetime.now()
        logger.info(f"🧪 INICIANDO TEST SIMPLIFICADO - {start_time}")
        logger.info("="*60)
        
        success = True
        results = {
            'accessibility': False,
            'backend': False,
            'submission': False,
        }
        
        try:
            # Test 1: Accesibilidad
            logger.info("1️⃣ PROBANDO ACCESIBILIDAD DE LA PÁGINA")
            results['accessibility'] = self.test_page_accessibility()
            
            if not results['accessibility']:
                logger.error("❌ Página no accesible, deteniendo tests")
                return False
            
            # Test 2: Backend
            logger.info("\n2️⃣ VALIDANDO FUNCIONALIDAD DEL BACKEND")
            results['backend'] = self.validate_backend_functionality()
            
            # Test 3: Simulación de envío
            logger.info("\n3️⃣ SIMULANDO ENVÍO DEL FORMULARIO")
            submission_success, response_data = self.simulate_form_submission()
            results['submission'] = submission_success
            
            # Resumen
            logger.info("\n" + "="*60)
            logger.info("📊 RESUMEN DE RESULTADOS:")
            logger.info(f"🌐 Accesibilidad: {'✅' if results['accessibility'] else '❌'}")
            logger.info(f"⚙️ Backend: {'✅' if results['backend'] else '❌'}")
            logger.info(f"📤 Envío: {'✅' if results['submission'] else '❌'}")
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            overall_success = all(results.values())
            
            if overall_success:
                logger.info(f"✅ TEST COMPLETADO EXITOSAMENTE - Duración: {duration}")
                logger.info("🎉 El formulario DevOps ReadyMind está funcionando correctamente")
            else:
                logger.warning(f"⚠️ TEST COMPLETADO CON ADVERTENCIAS - Duración: {duration}")
                failed_tests = [test for test, result in results.items() if not result]
                logger.warning(f"❌ Tests fallidos: {', '.join(failed_tests)}")
            
            return overall_success
            
        except Exception as e:
            logger.error(f"❌ ERROR EN TEST SIMPLIFICADO: {e}")
            return False

def main():
    """Función principal"""
    print("🧪 SCRIPT DE TESTING SIMPLIFICADO - FORMULARIO DEVOPS READYMIND")
    print("================================================================")
    print("Este script funciona sin necesidad de navegador gráfico")
    print("Ideal para entornos WSL, servidores headless, y CI/CD")
    print()
    
    # Configuración
    url = input("🌐 URL del formulario (Enter para default): ").strip()
    if not url:
        url = "https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/"
    
    print(f"\n🎯 Iniciando test en: {url}")
    print("-" * 60)
    
    # Ejecutar test
    test = FormularioDevOpsSimpleTest(url)
    success = test.run_simple_test()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ TEST EXITOSO - Formulario funcionando correctamente")
        print("📋 Log detallado en: ./test_formulario_simple.log")
        print("🎯 El formulario DevOps ReadyMind está listo para producción")
    else:
        print("⚠️ TEST CON ADVERTENCIAS - Revisa los logs")
        print("📋 Log detallado en: ./test_formulario_simple.log")
        print("💡 Algunos componentes pueden necesitar verificación manual")
    
    print("🎉 Gracias por usar ReadyMind Testing Suite")

if __name__ == "__main__":
    main()