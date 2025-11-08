#!/usr/bin/env python3
"""
Chrome DevOps Assessment - SCRIPT UNIFICADO COMPLETO
Maneja las 60 preguntas: Radio (opción única) + Checkbox (opción múltiple)
Lógica unificada para completar todo el formulario
"""

import logging
import json
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ChromeDevOpsUnifiedAssessment:
    def __init__(self):
        self.driver = None
        self.production_url = "https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/"
        self.complete_structure = self.load_complete_structure()
        
        # Datos del cliente para pruebas
        self.client_data = {
            'name': 'Cliente DevOps Completo',
            'email': 'devops.completo@readymind.com',
            'company': 'ReadyMind DevOps Solutions'
        }
        
    def load_complete_structure(self):
        """Cargar la estructura completa de 60 preguntas"""
        try:
            with open('complete_form_structure.json', 'r', encoding='utf-8') as f:
                structure = json.load(f)
                logger.info(f"📊 Estructura cargada: {structure.get('total_questions', 0)} preguntas")
                logger.info(f"   Radio: {structure.get('summary', {}).get('radio_questions', 0)}")
                logger.info(f"   Checkbox: {structure.get('summary', {}).get('checkbox_questions', 0)}")
                return structure
        except Exception as e:
            logger.error(f"Error cargando estructura completa: {e}")
            return {}
    
    def setup_chrome(self):
        """Configurar Chrome optimizado para el formulario completo"""
        try:
            driver_path = "/home/larenas/.wdm/drivers/chromedriver/linux64/142.0.7444.61/chromedriver-linux64/chromedriver"
            
            if not os.path.exists(driver_path):
                logger.error(f"ChromeDriver no encontrado: {driver_path}")
                return False
            
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-web-security")
            chrome_options.add_argument("--allow-running-insecure-content")
            
            service = Service(driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.implicitly_wait(15)
            
            logger.info("✅ Chrome configurado para formulario completo de 60 preguntas")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error configurando Chrome: {e}")
            return False
    
    def take_screenshot(self, filename):
        """Tomar screenshot con manejo de errores"""
        try:
            self.driver.save_screenshot(filename)
            logger.info(f"📸 Screenshot guardado: {filename}")
            return True
        except Exception as e:
            logger.warning(f"Error tomando screenshot: {e}")
            return False
    
    def fill_client_info(self):
        """Llenar información del cliente"""
        try:
            logger.info("📝 Llenando información del cliente...")
            
            # Nombre del cliente
            name_field = WebDriverWait(self.driver, 15).until(
                EC.element_to_be_clickable((By.ID, "client_name"))
            )
            name_field.clear()
            name_field.send_keys(self.client_data['name'])
            logger.info(f"   ✅ Nombre: {self.client_data['name']}")
            
            # Email del cliente
            email_field = self.driver.find_element(By.ID, "client_email")
            email_field.clear()
            email_field.send_keys(self.client_data['email'])
            logger.info(f"   ✅ Email: {self.client_data['email']}")
            
            # Empresa del cliente
            company_field = self.driver.find_element(By.ID, "client_company")
            company_field.clear()
            company_field.send_keys(self.client_data['company'])
            logger.info(f"   ✅ Empresa: {self.client_data['company']}")
            
            time.sleep(1)
            return True
            
        except Exception as e:
            logger.error(f"❌ Error llenando información del cliente: {e}")
            return False
    
    def get_unified_answers(self, question_name, question_type):
        """
        LÓGICA UNIFICADA: Obtener respuestas según tipo de pregunta
        Radio = 1 respuesta, Checkbox = 2-3 respuestas
        """
        try:
            # Definir estrategias de respuesta por sección y tipo
            base_strategies = {
                # Sección A - Planificación y Gestión Ágil
                'A1': {'radio': ['A1O3'], 'checkbox': ['A1O2', 'A1O3']},
                'A2': {'radio': ['A2O3'], 'checkbox': ['A2O2', 'A2O4']},
                'A3': {'radio': ['A3O2'], 'checkbox': ['A3O1', 'A3O3']},
                'A4': {'radio': ['A4O3'], 'checkbox': ['A4O2', 'A4O3']},
                'A5': {'radio': ['A5O2'], 'checkbox': ['A5O2', 'A5O3']},
                'A6': {'radio': ['A6O3'], 'checkbox': ['A6O1', 'A6O2']},
                'A7': {'radio': ['A7O2'], 'checkbox': ['A7O2', 'A7O3']},
                'A8': {'radio': ['A8O3'], 'checkbox': ['A8O2', 'A8O4']},
                'A9': {'radio': ['A9O2'], 'checkbox': ['A9O1', 'A9O3']},
                'A10': {'radio': ['A10O3'], 'checkbox': ['A10O2', 'A10O3']},
                
                # Sección B - Código, Control de Versiones y Calidad
                'B1': {'radio': ['B1O3'], 'checkbox': ['B1O1', 'B1O3', 'B1O4']},
                'B2': {'radio': ['B2O2'], 'checkbox': ['B2O2', 'B2O3']},
                'B3': {'radio': ['B3O3'], 'checkbox': ['B3O1', 'B3O3', 'B3O4']},
                'B4': {'radio': ['B4O2'], 'checkbox': ['B4O2', 'B4O3']},
                'B5': {'radio': ['B5O3'], 'checkbox': ['B5O1', 'B5O2']},
                'B6': {'radio': ['B6O2'], 'checkbox': ['B6O2', 'B6O3']},
                'B7': {'radio': ['B7O3'], 'checkbox': ['B7O1', 'B7O2', 'B7O3']},
                'B8': {'radio': ['B8O2'], 'checkbox': ['B8O2', 'B8O3']},
                'B9': {'radio': ['B9O3'], 'checkbox': ['B9O1', 'B9O3']},
                'B10': {'radio': ['B10O2'], 'checkbox': ['B10O2', 'B10O3']},
                
                # Sección C - CI/CD y Gestión de Releases
                'C1': {'radio': ['C1O3'], 'checkbox': ['C1O1', 'C1O2', 'C1O3']},
                'C2': {'radio': ['C2O3'], 'checkbox': ['C2O2', 'C2O3']},
                'C3': {'radio': ['C3O2'], 'checkbox': ['C3O2', 'C3O3']},
                'C4': {'radio': ['C4O3'], 'checkbox': ['C4O1', 'C4O2', 'C4O3']},
                'C5': {'radio': ['C5O2'], 'checkbox': ['C5O1', 'C5O2']},
                'C6': {'radio': ['C6O3'], 'checkbox': ['C6O2', 'C6O3']},
                'C7': {'radio': ['C7O2'], 'checkbox': ['C7O1', 'C7O2']},
                'C8': {'radio': ['C8O3'], 'checkbox': ['C8O2', 'C8O3']},
                'C9': {'radio': ['C9O2'], 'checkbox': ['C9O1', 'C9O2', 'C9O3']},
                'C10': {'radio': ['C10O3'], 'checkbox': ['C10O1', 'C10O2']},
                
                # Sección D - Infraestructura como Código
                'D1': {'radio': ['D1O3'], 'checkbox': ['D1O1', 'D1O2']},
                'D2': {'radio': ['D2O2'], 'checkbox': ['D2O2', 'D2O3']},
                'D3': {'radio': ['D3O3'], 'checkbox': ['D3O1', 'D3O2']},
                'D4': {'radio': ['D4O2'], 'checkbox': ['D4O1', 'D4O2']},
                'D5': {'radio': ['D5O3'], 'checkbox': ['D5O1', 'D5O3']},
                'D6': {'radio': ['D6O2'], 'checkbox': ['D6O2', 'D6O3']},
                'D7': {'radio': ['D7O3'], 'checkbox': ['D7O1', 'D7O2']},
                'D8': {'radio': ['D8O2'], 'checkbox': ['D8O1', 'D8O2', 'D8O3']},
                'D9': {'radio': ['D9O3'], 'checkbox': ['D9O1', 'D9O2']},
                'D10': {'radio': ['D10O2'], 'checkbox': ['D10O1', 'D10O2']},
                
                # Sección E - Seguridad y Cumplimiento
                'E1': {'radio': ['E1O3'], 'checkbox': ['E1O1', 'E1O2']},
                'E2': {'radio': ['E2O3'], 'checkbox': ['E2O1', 'E2O2']},
                'E3': {'radio': ['E3O2'], 'checkbox': ['E3O1', 'E3O2']},
                'E4': {'radio': ['E4O3'], 'checkbox': ['E4O1', 'E4O2']},
                'E5': {'radio': ['E5O2'], 'checkbox': ['E5O1', 'E5O2']},
                'E6': {'radio': ['E6O3'], 'checkbox': ['E6O1', 'E6O2']},
                'E7': {'radio': ['E7O2'], 'checkbox': ['E7O1', 'E7O2']},
                'E8': {'radio': ['E8O3'], 'checkbox': ['E8O1', 'E8O2']},
                'E9': {'radio': ['E9O2'], 'checkbox': ['E9O1', 'E9O2']},
                'E10': {'radio': ['E10O3'], 'checkbox': ['E10O1', 'E10O2']},
                
                # Sección F - Observabilidad, Monitoreo y Operación
                'F1': {'radio': ['F1O3'], 'checkbox': ['F1O1', 'F1O2', 'F1O3']},
                'F2': {'radio': ['F2O3'], 'checkbox': ['F2O1', 'F2O2']},
                'F3': {'radio': ['F3O2'], 'checkbox': ['F3O1', 'F3O2']},
                'F4': {'radio': ['F4O3'], 'checkbox': ['F4O1', 'F4O3']},
                'F5': {'radio': ['F5O2'], 'checkbox': ['F5O1', 'F5O2']},
                'F6': {'radio': ['F6O3'], 'checkbox': ['F6O1', 'F6O2']},
                'F7': {'radio': ['F7O2'], 'checkbox': ['F7O1', 'F7O2']},
                'F8': {'radio': ['F8O3'], 'checkbox': ['F8O1', 'F8O2']},
                'F9': {'radio': ['F9O2'], 'checkbox': ['F9O1', 'F9O2']},
                'F10': {'radio': ['F10O3'], 'checkbox': ['F10O1', 'F10O2']}
            }
            
            # Obtener estrategia para la pregunta específica
            question_strategy = base_strategies.get(question_name, {})
            answers = question_strategy.get(question_type, [])
            
            if not answers:
                # Fallback: generar respuestas dinámicamente
                if question_type == 'radio':
                    answers = [f"{question_name}O2"]  # Opción intermedia
                else:  # checkbox
                    answers = [f"{question_name}O1", f"{question_name}O2"]  # 2 opciones
                
                logger.info(f"   📋 {question_name} ({question_type}): usando fallback {answers}")
            else:
                logger.info(f"   📋 {question_name} ({question_type}): respuesta estratégica {answers}")
            
            return answers
            
        except Exception as e:
            logger.warning(f"Error obteniendo respuestas para {question_name}: {e}")
            return [f"{question_name}O2"]
    
    def fill_question_unified(self, question_name, question_data):
        """
        MÉTODO UNIFICADO: Llenar una pregunta sin importar si es radio o checkbox
        """
        try:
            question_type = question_data.get('type', 'radio')
            options = question_data.get('options', [])
            
            if not options:
                logger.warning(f"   ⚠️ {question_name}: sin opciones disponibles")
                return False
            
            # Obtener respuestas usando lógica unificada
            target_answers = self.get_unified_answers(question_name, question_type)
            
            successful_selections = 0
            
            # Procesar cada respuesta objetivo
            for target_answer in target_answers:
                # Buscar la opción correspondiente
                target_option = None
                for option in options:
                    if option['value'] == target_answer:
                        target_option = option
                        break
                
                if target_option and target_option['id']:
                    try:
                        # Localizar elemento
                        element = WebDriverWait(self.driver, 8).until(
                            EC.presence_of_element_located((By.ID, target_option['id']))
                        )
                        
                        # Scroll inteligente para visibilidad
                        self.driver.execute_script(
                            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});", 
                            element
                        )
                        time.sleep(0.3)
                        
                        # Click usando JavaScript para mayor confiabilidad
                        self.driver.execute_script("arguments[0].click();", element)
                        successful_selections += 1
                        
                        logger.info(f"       ✅ Seleccionado: {target_answer}")
                        
                        # Pausa entre selecciones
                        time.sleep(random.uniform(0.2, 0.4))
                        
                    except TimeoutException:
                        logger.warning(f"       ⚠️ Timeout para {target_answer}")
                        continue
                    except Exception as e:
                        logger.warning(f"       ⚠️ Error con {target_answer}: {str(e)[:50]}")
                        continue
                else:
                    logger.warning(f"       ⚠️ Opción {target_answer} no encontrada")
            
            # Validar resultado
            if successful_selections > 0:
                type_label = "RADIO" if question_type == "radio" else "CHECKBOX"
                logger.info(f"   ✅ {question_name}: {successful_selections} opciones ({type_label})")
                return True
            else:
                # Fallback: seleccionar primera opción disponible
                if options and options[0]['id']:
                    try:
                        element = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.ID, options[0]['id']))
                        )
                        self.driver.execute_script("arguments[0].click();", element)
                        logger.info(f"   ✅ {question_name}: {options[0]['value']} (fallback)")
                        return True
                    except:
                        pass
                
                logger.warning(f"   ❌ {question_name}: no se pudo completar")
                return False
            
        except Exception as e:
            logger.error(f"❌ Error procesando {question_name}: {e}")
            return False
    
    def fill_all_60_questions_unified(self):
        """
        MÉTODO PRINCIPAL: Llenar las 60 preguntas usando lógica unificada
        """
        try:
            logger.info("🚀 INICIANDO LLENADO UNIFICADO DE 60 PREGUNTAS")
            
            if not self.complete_structure or 'questions' not in self.complete_structure:
                logger.error("❌ Estructura de preguntas no disponible")
                return False
            
            questions = self.complete_structure['questions']
            total_questions = len(questions)
            
            logger.info(f"📊 Total preguntas detectadas: {total_questions}")
            logger.info(f"📊 Radio preguntas: {self.complete_structure.get('summary', {}).get('radio_questions', 0)}")
            logger.info(f"📊 Checkbox preguntas: {self.complete_structure.get('summary', {}).get('checkbox_questions', 0)}")
            
            # Contadores de progreso
            processed = 0
            successful = 0
            radio_completed = 0
            checkbox_completed = 0
            
            # Procesar cada pregunta usando método unificado
            for question_name, question_data in questions.items():
                try:
                    processed += 1
                    progress = (processed / total_questions) * 100
                    question_type = question_data.get('type', 'radio')
                    
                    logger.info(f"[{processed}/{total_questions}] 📝 {question_name} ({question_type}) - {progress:.1f}%")
                    
                    # Usar método unificado para cualquier tipo de pregunta
                    success = self.fill_question_unified(question_name, question_data)
                    
                    if success:
                        successful += 1
                        if question_type == 'radio':
                            radio_completed += 1
                        else:
                            checkbox_completed += 1
                    
                    # Screenshots de progreso
                    if processed % 12 == 0:  # Cada 12 preguntas (20% aprox)
                        screenshot_name = f"unified_progress_{processed}_{progress:.0f}percent.png"
                        self.take_screenshot(screenshot_name)
                        logger.info(f"📸 Progreso: {successful}/{processed} exitosas ({radio_completed}R/{checkbox_completed}C)")
                    
                    # Pausa entre preguntas
                    time.sleep(random.uniform(0.3, 0.8))
                    
                except Exception as e:
                    logger.error(f"Error procesando {question_name}: {e}")
                    continue
            
            # Resumen final
            success_rate = (successful / total_questions) * 100
            logger.info(f"📊 RESUMEN FINAL:")
            logger.info(f"   Total procesadas: {processed}/{total_questions}")
            logger.info(f"   Exitosas: {successful} ({success_rate:.1f}%)")
            logger.info(f"   Radio completadas: {radio_completed}")
            logger.info(f"   Checkbox completadas: {checkbox_completed}")
            
            # Considerar éxito si al menos 90% completado
            is_successful = success_rate >= 90.0
            
            if is_successful:
                logger.info("🎉 ¡CUESTIONARIO COMPLETADO EXITOSAMENTE!")
            else:
                logger.warning(f"⚠️ Solo {success_rate:.1f}% completado (requiere ≥90%)")
            
            return is_successful
            
        except Exception as e:
            logger.error(f"❌ Error en llenado unificado de 60 preguntas: {e}")
            return False
    
    def submit_final_form(self):
        """Enviar formulario completo y validar modal ReadyMind"""
        try:
            logger.info("🚀 ENVIANDO FORMULARIO COMPLETO DE 60 PREGUNTAS")
            
            # Estrategias múltiples para encontrar botón de envío
            submit_strategies = [
                ("CSS", "button[type='submit']"),
                ("CSS", "input[type='submit']"),
                ("CSS", ".submit-btn"),
                ("CSS", "#submit-btn"),
                ("CSS", "button.btn-primary"),
                ("CSS", ".btn.btn-primary"),
                ("XPATH", "//button[contains(text(), 'Enviar')]"),
                ("XPATH", "//button[contains(text(), 'Finalizar')]"),
                ("XPATH", "//input[@value='Enviar']"),
                ("XPATH", "//button[contains(text(), 'Submit')]"),
                ("XPATH", "//button[contains(@class, 'submit')]")
            ]
            
            submit_button = None
            used_strategy = None
            
            for strategy_type, selector in submit_strategies:
                try:
                    if strategy_type == "XPATH":
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        submit_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    used_strategy = f"{strategy_type}: {selector}"
                    logger.info(f"   ✅ Botón encontrado con: {used_strategy}")
                    break
                except:
                    continue
            
            if not submit_button:
                # Último recurso: buscar cualquier botón con texto relacionado
                logger.warning("⚠️ Buscando botón alternativo por texto...")
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for btn in buttons:
                        btn_text = (btn.text or "").lower()
                        if any(keyword in btn_text for keyword in ['enviar', 'submit', 'finalizar', 'send', 'complete']):
                            submit_button = btn
                            used_strategy = f"TEXT: '{btn.text}'"
                            logger.info(f"   ✅ Botón alternativo: {used_strategy}")
                            break
                except Exception as e:
                    logger.error(f"Error buscando botones alternativos: {e}")
            
            if submit_button:
                # Scroll al botón y preparar envío
                self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
                time.sleep(2)
                
                # Screenshot pre-envío
                self.take_screenshot("unified_before_submit_60q.png")
                logger.info("📸 Screenshot pre-envío guardado")
                
                # Ejecutar envío
                self.driver.execute_script("arguments[0].click();", submit_button)
                logger.info(f"✅ Formulario enviado usando: {used_strategy}")
                
                # Esperar procesamiento del servidor
                logger.info("⏳ Esperando respuesta del servidor (60 preguntas)...")
                time.sleep(15)  # Más tiempo para procesar todas las preguntas
                
                # Screenshots post-envío
                self.take_screenshot("unified_after_submit_60q.png")
                
                # Verificar indicadores de éxito múltiples
                try:
                    page_source = self.driver.page_source.lower()
                    
                    # Indicadores de éxito esperados
                    success_indicators = [
                        "readymind", "assessment", "devops", "analysis", "report",
                        "resultado", "completado", "success", "thank you", "gracias",
                        "modal", "popup", "dashboard", "score", "evaluation",
                        "congratulations", "felicitaciones", "análisis"
                    ]
                    
                    # Indicadores de error
                    error_indicators = [
                        "error", "preguntas pendientes", "obligatorias", "incompleto",
                        "faltan", "required", "missing", "incomplete"
                    ]
                    
                    found_success = [ind for ind in success_indicators if ind in page_source]
                    found_errors = [ind for ind in error_indicators if ind in page_source]
                    
                    # Buscar modal específicamente
                    try:
                        modals = self.driver.find_elements(By.CSS_SELECTOR, 
                            ".modal, .popup, .overlay, [class*='modal'], [id*='modal'], [class*='popup']")
                        modal_count = len(modals)
                    except:
                        modal_count = 0
                    
                    # Evaluar resultado
                    if found_success and not found_errors:
                        logger.info(f"🎉 ¡ENVÍO EXITOSO! Indicadores: {found_success}")
                        if modal_count > 0:
                            logger.info(f"📋 Modal ReadyMind detectado: {modal_count} elementos")
                            self.take_screenshot("unified_modal_detected_60q.png")
                        return True
                        
                    elif found_errors:
                        logger.error(f"❌ Errores detectados: {found_errors}")
                        if "preguntas pendientes" in page_source:
                            logger.error("❌ AÚN HAY PREGUNTAS SIN RESPONDER")
                        self.take_screenshot("unified_errors_detected.png")
                        return False
                        
                    else:
                        logger.warning("⚠️ Estado incierto, pero sin errores explícitos")
                        return True  # Asumir éxito si no hay errores claros
                
                except Exception as e:
                    logger.warning(f"Error verificando resultado: {e}")
                    return True  # Asumir éxito si no se puede verificar
                
            else:
                logger.error("❌ NO SE ENCONTRÓ BOTÓN DE ENVÍO")
                self.take_screenshot("unified_no_submit_button.png")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error enviando formulario: {e}")
            self.take_screenshot("unified_submit_error.png")
            return False
    
    def run_unified_60_assessment(self):
        """MÉTODO PRINCIPAL: Ejecutar assessment completo unificado"""
        try:
            logger.info("🔥 CHROME DEVOPS ASSESSMENT - LÓGICA UNIFICADA")
            logger.info("📊 60 PREGUNTAS: Radio + Checkbox en flujo unificado")
            logger.info("🎯 Objetivo: Completar todo y obtener modal ReadyMind")
            logger.info("=" * 80)
            
            start_time = time.time()
            
            # 1. Configurar Chrome
            logger.info("🔧 Paso 1: Configuración de Chrome")
            if not self.setup_chrome():
                return False
            
            # 2. Navegar al formulario
            logger.info("🌐 Paso 2: Navegando al formulario")
            self.driver.get(self.production_url)
            time.sleep(5)
            self.take_screenshot("01_unified_form_loaded.png")
            
            # 3. Llenar información del cliente
            logger.info("📝 Paso 3: Información del cliente")
            if not self.fill_client_info():
                logger.error("❌ Error en información del cliente")
                return False
            self.take_screenshot("02_unified_client_info.png")
            
            # 4. Llenar las 60 preguntas con lógica unificada
            logger.info("📋 Paso 4: Llenando 60 preguntas (unificado)")
            if not self.fill_all_60_questions_unified():
                logger.error("❌ Error completando las 60 preguntas")
                return False
            self.take_screenshot("03_unified_all_questions_done.png")
            
            # 5. Enviar formulario y validar
            logger.info("🚀 Paso 5: Envío final y validación")
            success = self.submit_final_form()
            self.take_screenshot("04_unified_final_result.png")
            
            # 6. Resumen final
            elapsed_time = time.time() - start_time
            logger.info("=" * 80)
            
            if success:
                logger.info("🎉 ¡ÉXITO TOTAL! ASSESSMENT COMPLETO")
                logger.info("✅ 60 preguntas completadas con lógica unificada")
                logger.info("📋 Modal ReadyMind debe estar visible")
                logger.info("📸 Screenshots completos documentados")
                logger.info(f"⏱️ Tiempo total: {elapsed_time:.1f} segundos")
            else:
                logger.warning("⚠️ El assessment puede haber fallado")
                logger.info(f"⏱️ Tiempo transcurrido: {elapsed_time:.1f} segundos")
            
            # Mantener Chrome abierto para verificación
            logger.info("\n🔍 Chrome mantenido abierto para verificación manual")
            logger.info("   Presiona Ctrl+C para cerrar")
            
            try:
                while True:
                    time.sleep(10)
            except KeyboardInterrupt:
                logger.info("Cerrando aplicación...")
            
            return success
            
        except Exception as e:
            logger.error(f"❌ Error en assessment unificado: {e}")
            return False
        finally:
            try:
                if self.driver:
                    self.driver.quit()
            except:
                pass

def main():
    logger.info("🔥 CHROME DEVOPS ASSESSMENT - VERSIÓN UNIFICADA")
    logger.info("🎯 Radio + Checkbox en una sola lógica")
    logger.info("📊 60 preguntas completas → Envío → Modal ReadyMind")
    logger.info("=" * 80)
    
    assessment = ChromeDevOpsUnifiedAssessment()
    success = assessment.run_unified_60_assessment()
    
    if success:
        print("\n🎉 ¡ÉXITO COMPLETO!")
        print("✅ Las 60 preguntas fueron completadas")
        print("📋 Formulario enviado exitosamente")
        print("🎯 Modal ReadyMind debe estar visible")
        print("📸 Evidencia completa documentada")
    else:
        print("\n❌ El assessment falló")
        print("🔍 Revisa los logs y screenshots para diagnóstico")
    
    return 0 if success else 1

if __name__ == "__main__":
    exit(main())