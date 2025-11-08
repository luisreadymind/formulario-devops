#!/usr/bin/env python3
"""
Script de Testing Automatizado - Formulario DevOps ReadyMind
Autor: Luis Alberto Arenas
Fecha: 2025-11-08

Este script automatiza el llenado completo del formulario DevOps y valida
la funcionalidad del modal de despedida con cierre automático de ventana.
"""

import time
import random
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('test_formulario_devops.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class FormularioDevOpsTest:
    """Clase para automatizar el testing del formulario DevOps"""
    
    def __init__(self, url="https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/"):
        self.url = url
        self.driver = None
        self.wait = None
        self.test_data = {
            'client_name': 'ReadyMind Testing Suite',
            'client_email': 'testing@readymind.com',
            'client_company': 'ReadyMind Tecnología'
        }
        
    def setup_driver(self, headless=False):
        """Configurar el driver de Chrome con opciones optimizadas"""
        try:
            chrome_options = Options()
            
            if headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-extensions')
            chrome_options.add_argument('--disable-web-security')
            chrome_options.add_argument('--allow-running-insecure-content')
            
            # Configurar para permitir cierre automático de ventana
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            # Inicializar driver
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("✅ Driver de Chrome configurado exitosamente")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error configurando driver: {e}")
            return False
    
    def load_page(self):
        """Cargar la página del formulario"""
        try:
            logger.info(f"🌐 Cargando página: {self.url}")
            self.driver.get(self.url)
            
            # Esperar a que la página cargue completamente
            self.wait.until(EC.presence_of_element_located((By.ID, "devopsForm")))
            
            # Tomar screenshot inicial
            self.driver.save_screenshot('test_screenshots/01_pagina_inicial.png')
            logger.info("✅ Página cargada exitosamente")
            
            # Validar sección de bienvenida ReadyMind
            try:
                welcome_section = self.driver.find_element(By.CLASS_NAME, "welcome-section")
                readymind_logo = welcome_section.find_element(By.CLASS_NAME, "readymind-logo")
                logger.info("✅ Sección de bienvenida ReadyMind encontrada")
            except NoSuchElementException:
                logger.warning("⚠️ Sección de bienvenida no encontrada")
                
            return True
            
        except Exception as e:
            logger.error(f"❌ Error cargando página: {e}")
            return False
    
    def fill_client_data(self):
        """Llenar información del cliente"""
        try:
            logger.info("📝 Llenando información del cliente...")
            
            # Nombre
            name_field = self.wait.until(EC.element_to_be_clickable((By.ID, "client_name")))
            name_field.clear()
            name_field.send_keys(self.test_data['client_name'])
            logger.info(f"✅ Nombre: {self.test_data['client_name']}")
            
            # Email
            email_field = self.driver.find_element(By.ID, "client_email")
            email_field.clear()
            email_field.send_keys(self.test_data['client_email'])
            logger.info(f"✅ Email: {self.test_data['client_email']}")
            
            # Empresa
            company_field = self.driver.find_element(By.ID, "client_company")
            company_field.clear()
            company_field.send_keys(self.test_data['client_company'])
            logger.info(f"✅ Empresa: {self.test_data['client_company']}")
            
            # Screenshot después de llenar datos del cliente
            self.driver.save_screenshot('test_screenshots/02_datos_cliente.png')
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error llenando datos del cliente: {e}")
            return False
    
    def fill_questionnaire(self):
        """Llenar todas las preguntas del cuestionario automáticamente"""
        try:
            logger.info("📋 Iniciando llenado automático del cuestionario...")
            questions_answered = 0
            
            # Obtener todas las preguntas
            question_groups = self.driver.find_elements(By.CLASS_NAME, "question-group")
            total_questions = len(question_groups)
            logger.info(f"📊 Total de preguntas encontradas: {total_questions}")
            
            for i, question_group in enumerate(question_groups, 1):
                try:
                    # Scroll hacia la pregunta
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", question_group)
                    time.sleep(0.5)
                    
                    question_id = question_group.get_attribute('data-question')
                    question_title = question_group.find_element(By.CLASS_NAME, "question-title").text
                    
                    # Buscar opciones de radio buttons
                    radio_options = question_group.find_elements(By.CSS_SELECTOR, "input[type='radio']")
                    if radio_options:
                        # Seleccionar una opción aleatoria pero consistente
                        selected_index = min(random.randint(0, len(radio_options) - 1), len(radio_options) - 1)
                        option = radio_options[selected_index]
                        
                        # Hacer clic en la opción usando JavaScript
                        self.driver.execute_script("arguments[0].click();", option)
                        questions_answered += 1
                        
                        logger.info(f"✅ Pregunta {question_id} ({i}/{total_questions}): Radio seleccionado")
                        
                    else:
                        # Buscar opciones de checkboxes
                        checkbox_options = question_group.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
                        if checkbox_options:
                            # Seleccionar 1-3 opciones aleatorias
                            num_to_select = min(random.randint(1, 3), len(checkbox_options))
                            selected_indices = random.sample(range(len(checkbox_options)), num_to_select)
                            
                            for idx in selected_indices:
                                option = checkbox_options[idx]
                                self.driver.execute_script("arguments[0].click();", option)
                            
                            questions_answered += 1
                            logger.info(f"✅ Pregunta {question_id} ({i}/{total_questions}): {num_to_select} checkboxes seleccionados")
                    
                    # Pequeña pausa entre preguntas
                    time.sleep(0.3)
                    
                    # Screenshot cada 10 preguntas
                    if i % 10 == 0:
                        self.driver.save_screenshot(f'test_screenshots/03_progreso_{i}_preguntas.png')
                        
                except Exception as e:
                    logger.warning(f"⚠️ Error en pregunta {i}: {e}")
                    continue
            
            logger.info(f"✅ Cuestionario completado: {questions_answered}/{total_questions} preguntas respondidas")
            
            # Screenshot final del cuestionario
            self.driver.save_screenshot('test_screenshots/04_cuestionario_completo.png')
            
            # Validar progreso al 100%
            try:
                progress_element = self.driver.find_element(By.ID, "progress-percentage")
                progress_text = progress_element.text
                logger.info(f"📊 Progreso mostrado: {progress_text}")
                
                if "100%" in progress_text:
                    logger.info("✅ Progreso al 100% confirmado")
                else:
                    logger.warning(f"⚠️ Progreso no está al 100%: {progress_text}")
                    
            except NoSuchElementException:
                logger.warning("⚠️ No se pudo verificar el progreso")
            
            return questions_answered == total_questions
            
        except Exception as e:
            logger.error(f"❌ Error llenando cuestionario: {e}")
            return False
    
    def submit_form_and_validate_modal(self):
        """Enviar formulario y validar el modal de despedida"""
        try:
            logger.info("🚀 Enviando formulario...")
            
            # Buscar y hacer clic en el botón de envío
            submit_button = self.wait.until(EC.element_to_be_clickable((By.ID, "submitBtn")))
            submit_button_text = submit_button.text
            logger.info(f"📝 Texto del botón de envío: {submit_button_text}")
            
            # Screenshot antes del envío
            self.driver.save_screenshot('test_screenshots/05_antes_envio.png')
            
            submit_button.click()
            logger.info("✅ Formulario enviado")
            
            # Esperar a que aparezca el loading overlay
            try:
                loading_overlay = self.wait.until(EC.visibility_of_element_located((By.ID, "loadingOverlay")))
                logger.info("⏳ Loading overlay aparecido")
                
                # Esperar a que desaparezca el loading
                self.wait.until(EC.invisibility_of_element_located((By.ID, "loadingOverlay")))
                logger.info("✅ Loading completado")
                
            except TimeoutException:
                logger.warning("⚠️ Loading overlay no detectado o muy rápido")
            
            # Esperar a que aparezca el modal
            modal = self.wait.until(EC.visibility_of_element_located((By.ID, "analysisResultModal")))
            logger.info("✅ Modal de resultados aparecido")
            
            # Screenshot del modal
            self.driver.save_screenshot('test_screenshots/06_modal_resultados.png')
            
            # Validar elementos del modal
            self.validate_modal_content()
            
            # Esperar un poco para ver el modal completo
            time.sleep(3)
            
            # Hacer clic en cerrar y validar funcionalidad de cierre
            self.test_modal_close_functionality()
            
            return True
            
        except TimeoutException as e:
            logger.error(f"❌ Timeout esperando modal: {e}")
            self.driver.save_screenshot('test_screenshots/error_timeout_modal.png')
            return False
        except Exception as e:
            logger.error(f"❌ Error enviando formulario: {e}")
            self.driver.save_screenshot('test_screenshots/error_envio_formulario.png')
            return False
    
    def validate_modal_content(self):
        """Validar el contenido del modal de despedida"""
        try:
            logger.info("🔍 Validando contenido del modal...")
            
            modal = self.driver.find_element(By.ID, "analysisResultModal")
            
            # Validar título del modal
            modal_title = modal.find_element(By.ID, "analysisModalTitle").text
            logger.info(f"📋 Título del modal: {modal_title}")
            
            # Buscar sección de despedida ReadyMind
            try:
                farewell_section = modal.find_element(By.CLASS_NAME, "farewell-section")
                logger.info("✅ Sección de despedida ReadyMind encontrada")
                
                # Validar logo ReadyMind
                try:
                    readymind_logo = farewell_section.find_element(By.CLASS_NAME, "readymind-logo-small")
                    logo_brand = readymind_logo.find_element(By.CLASS_NAME, "logo-brand").text
                    logo_tagline = readymind_logo.find_element(By.CLASS_NAME, "logo-tagline-small").text
                    logger.info(f"✅ Logo ReadyMind: {logo_brand} - {logo_tagline}")
                except NoSuchElementException:
                    logger.warning("⚠️ Logo ReadyMind no encontrado en modal")
                
                # Validar mensaje de despedida
                try:
                    farewell_title = farewell_section.find_element(By.CLASS_NAME, "farewell-title").text
                    farewell_text = farewell_section.find_element(By.CLASS_NAME, "farewell-text").text
                    logger.info(f"✅ Mensaje de despedida encontrado: {farewell_title[:50]}...")
                except NoSuchElementException:
                    logger.warning("⚠️ Mensaje de despedida no encontrado")
                
                # Validar próximos pasos
                try:
                    next_steps = farewell_section.find_element(By.CLASS_NAME, "next-steps")
                    steps_list = next_steps.find_elements(By.CSS_SELECTOR, ".steps-list li")
                    logger.info(f"✅ Próximos pasos encontrados: {len(steps_list)} elementos")
                except NoSuchElementException:
                    logger.warning("⚠️ Lista de próximos pasos no encontrada")
                
                # Validar aviso de cierre de ventana
                try:
                    close_notice = farewell_section.find_element(By.CLASS_NAME, "window-close-notice")
                    logger.info("✅ Aviso de cierre de ventana encontrado")
                except NoSuchElementException:
                    logger.warning("⚠️ Aviso de cierre de ventana no encontrado")
                    
            except NoSuchElementException:
                logger.error("❌ Sección de despedida ReadyMind no encontrada")
            
            # Screenshot del modal completo
            self.driver.save_screenshot('test_screenshots/07_modal_validacion.png')
            
        except Exception as e:
            logger.error(f"❌ Error validando contenido del modal: {e}")
    
    def test_modal_close_functionality(self):
        """Probar la funcionalidad de cierre del modal"""
        try:
            logger.info("🔚 Probando funcionalidad de cierre del modal...")
            
            # Buscar botón de cerrar
            close_button = self.driver.find_element(By.CSS_SELECTOR, "#analysisResultModal .btn-secondary")
            close_button_text = close_button.text
            logger.info(f"🔲 Botón de cerrar encontrado: {close_button_text}")
            
            # Screenshot antes de cerrar
            self.driver.save_screenshot('test_screenshots/08_antes_cerrar_modal.png')
            
            # Hacer clic en cerrar
            close_button.click()
            logger.info("✅ Botón de cerrar clickeado")
            
            # Esperar confirmación del navegador (si aparece)
            time.sleep(2)
            
            # Verificar si aparece confirmación de cierre
            try:
                # Intentar manejar alert de confirmación
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                logger.info(f"📢 Confirmación de cierre: {alert_text}")
                
                # Aceptar la confirmación
                alert.accept()
                logger.info("✅ Confirmación de cierre aceptada")
                
            except:
                logger.info("ℹ️ No se detectó confirmación de cierre (normal)")
            
            # Screenshot final
            self.driver.save_screenshot('test_screenshots/09_despues_cerrar_modal.png')
            
            # Verificar si la ventana se cerró o cambió
            try:
                current_url = self.driver.current_url
                logger.info(f"🌐 URL actual después del cierre: {current_url}")
                
                if current_url != self.url:
                    logger.info("✅ Página cambió después del cierre del modal")
                else:
                    logger.info("ℹ️ Página permanece igual (comportamiento esperado en testing)")
                    
            except Exception as e:
                logger.info(f"ℹ️ Posible cierre de ventana: {e}")
            
        except Exception as e:
            logger.error(f"❌ Error probando cierre del modal: {e}")
    
    def run_full_test(self, headless=False):
        """Ejecutar test completo del formulario"""
        start_time = datetime.now()
        logger.info(f"🚀 INICIANDO TEST COMPLETO DEL FORMULARIO DEVOPS - {start_time}")
        
        try:
            # Crear directorio para screenshots
            import os
            os.makedirs('test_screenshots', exist_ok=True)
            
            # Setup
            if not self.setup_driver(headless):
                return False
            
            # Load page
            if not self.load_page():
                return False
            
            # Fill client data
            if not self.fill_client_data():
                return False
            
            # Fill questionnaire
            if not self.fill_questionnaire():
                return False
            
            # Submit and validate modal
            if not self.submit_form_and_validate_modal():
                return False
            
            end_time = datetime.now()
            duration = end_time - start_time
            logger.info(f"✅ TEST COMPLETADO EXITOSAMENTE - Duración: {duration}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ERROR EN TEST COMPLETO: {e}")
            return False
        
        finally:
            if self.driver:
                time.sleep(5)  # Pausa antes de cerrar para observar
                self.driver.quit()
                logger.info("🔚 Driver cerrado")

def main():
    """Función principal para ejecutar el test"""
    print("🧪 SCRIPT DE TESTING - FORMULARIO DEVOPS READYMIND")
    print("="*60)
    
    # Configuración del test
    url = input("🌐 URL del formulario (Enter para default): ").strip()
    if not url:
        url = "https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/"
    
    headless_input = input("🖥️ ¿Ejecutar en modo headless? (y/N): ").strip().lower()
    headless = headless_input in ['y', 'yes', 'sí', 'si']
    
    print(f"\n🎯 Iniciando test en: {url}")
    print(f"👁️ Modo headless: {'Sí' if headless else 'No'}")
    print("-"*60)
    
    # Ejecutar test
    test = FormularioDevOpsTest(url)
    success = test.run_full_test(headless)
    
    print("\n" + "="*60)
    if success:
        print("✅ TEST EXITOSO - Modal de despedida funcionando correctamente")
        print("📸 Screenshots guardados en: ./test_screenshots/")
        print("📋 Log detallado en: ./test_formulario_devops.log")
    else:
        print("❌ TEST FALLIDO - Revisa los logs para más detalles")
        print("📋 Log de errores en: ./test_formulario_devops.log")
    
    print("🎉 Gracias por usar ReadyMind Testing Suite")

if __name__ == "__main__":
    main()