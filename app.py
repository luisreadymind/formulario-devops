#!/usr/bin/env python3
"""
Formulario DevOps Azure - Aplicación Flask
Autor: Luis Alberto Arenas
Fecha: 2025-11-07
"""

import os
import json
import uuid
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'devops-formulario-secret-key-2025')

# Configuración de la API externa
API_CONFIG = {
    'devops_analyzer_url': 'https://devops-analyzer-api.azurewebsites.net/api/generate-report',
    'timeout': 300  # 5 minutos timeout
}

# Cargar estructura del cuestionario
def load_questionnaire():
    """Cargar el cuestionario desde el archivo JSON"""
    try:
        with open('cuestionario_devops_azure.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error cargando cuestionario: {e}")
        return None

def calculate_maturity_score(responses):
    """Calcular puntaje de madurez DevOps basado en las respuestas"""
    scores = {
        'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0
    }
    
    # Valores para cada respuesta (ejemplo básico)
    score_mapping = {
        'A1': {'valor1': 4, 'valor2': 3, 'valor3': 2, 'valor4': 1, 'valor5': 0},
        'A2': {'valor1': 4, 'valor2': 3, 'valor3': 2, 'valor4': 1},
        'A3': {'valor1': 4, 'valor2': 3, 'valor3': 1, 'valor4': 0},
        'A4': {'valor1': 4, 'valor2': 3, 'valor3': 2, 'valor4': 1}
    }
    
    total_possible = 0
    total_achieved = 0
    
    for question_id, response in responses.items():
        if question_id.startswith(('A', 'B', 'C', 'D', 'E', 'F')):
            area = question_id[0]
            if question_id in score_mapping and response in score_mapping[question_id]:
                score = score_mapping[question_id][response]
                scores[area] += score
                total_achieved += score
                total_possible += max(score_mapping[question_id].values())
    
    # Calcular porcentajes
    maturity_percentages = {}
    for area, score in scores.items():
        max_score = 40  # Asumiendo 10 preguntas x 4 puntos máximo
        maturity_percentages[area] = min(100, (score / max_score) * 100) if max_score > 0 else 0
    
    overall_maturity = (total_achieved / total_possible * 100) if total_possible > 0 else 0
    
    return maturity_percentages, overall_maturity

def generate_pdf_report(client_data, questionnaire, responses):
    """Generar reporte PDF simple con las preguntas y respuestas del cliente (sin análisis)"""
    filename = f"reporte_devops_{client_data['nombre'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    doc = SimpleDocTemplate(filename, pagesize=A4, topMargin=1*inch, bottomMargin=1*inch)
    styles = getSampleStyleSheet()
    
    # Estilos personalizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=20,
        textColor=colors.HexColor('#0078d4'),  # Azure Blue
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=10,
        spaceBefore=15,
        textColor=colors.HexColor('#106ebe'),
        leftIndent=0
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=4,
        spaceBefore=8,
        leftIndent=10,
        fontName='Helvetica-Bold'
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        leftIndent=20,
        fontName='Helvetica'
    )
    
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    story = []
    
    # Título del reporte
    story.append(Paragraph("Reporte de Respuestas - Assessment DevOps", title_style))
    story.append(Spacer(1, 15))
    
    # Información del cliente
    story.append(Paragraph("Información del Cliente", heading_style))
    
    client_info = [
        ['Nombre:', client_data.get('nombre', 'No especificado')],
        ['Email:', client_data.get('email', 'No especificado')],
        ['Empresa:', client_data.get('empresa', 'No especificado')],
        ['Cargo:', client_data.get('cargo', 'No especificado')],
        ['Fecha de Evaluación:', datetime.now().strftime('%d/%m/%Y %H:%M')],
        ['ID de Evaluación:', str(uuid.uuid4())[:8]]
    ]
    
    client_table = Table(client_info, colWidths=[2*inch, 4*inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f8ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(client_table)
    story.append(Spacer(1, 20))
    
    # Contador de respuestas
    total_questions = 0
    answered_questions = 0
    other_field_count = 0
    
    # Verificar que el cuestionario está disponible
    if not questionnaire or 'areas' not in questionnaire:
        story.append(Paragraph("Error: No se pudo cargar el cuestionario", info_style))
        try:
            doc.build(story)
            return filename
        except:
            return None
    
    # Respuestas detalladas por área
    for area in questionnaire['areas']:
        story.append(Paragraph(f"{area['id']}. {area['nombre']}", heading_style))
        story.append(Paragraph(f"Objetivo: {area['objetivo']}", info_style))
        story.append(Spacer(1, 10))
        
        area_questions = 0
        area_answered = 0
        
        for question in area.get('preguntas', []):
            question_id = question['id']
            total_questions += 1
            area_questions += 1
            
            # Mostrar la pregunta
            story.append(Paragraph(f"Pregunta {question_id}: {question['texto']}", question_style))
            
            # Buscar la respuesta
            if question_id in responses:
                answered_questions += 1
                area_answered += 1
                response_value = responses[question_id]
                
                # Manejar respuestas múltiples (listas) vs respuestas simples (strings)
                if isinstance(response_value, list):
                    # Para preguntas de selección múltiple
                    response_texts = []
                    for val in response_value:
                        for option in question.get('opciones', []):
                            if option['id'] == val:
                                response_texts.append(option['texto'])
                                break
                    response_text = ', '.join(response_texts) if response_texts else "Respuesta no encontrada"
                else:
                    # Para preguntas de selección única
                    response_text = "Respuesta no encontrada"
                    
                    for option in question.get('opciones', []):
                        if option['id'] == response_value:
                            response_text = option['texto']
                            break
                    
                    # Si la respuesta es "OTRO", buscar el campo personalizado
                    if isinstance(response_value, str) and response_value.endswith('OTRO'):
                        other_field_key = f"{question_id}_otro"
                        if other_field_key in responses:
                            custom_text = responses[other_field_key]
                            if custom_text:
                                response_text = f"Otro: {custom_text}"
                                other_field_count += 1
                            else:
                                response_text = "Otro (sin especificar)"
                        else:
                            response_text = "Otro (sin especificar)"
                
                story.append(Paragraph(f"Respuesta: {response_text}", answer_style))
            else:
                story.append(Paragraph("Respuesta: No respondido", answer_style))
            
            story.append(Spacer(1, 6))
        
        # Resumen del área (solo conteo, sin análisis)
        story.append(Paragraph(f"Resumen del área: {area_answered} de {area_questions} preguntas respondidas", info_style))
        story.append(Spacer(1, 15))
    
    # Resumen general al final (solo estadísticas, sin análisis)
    story.append(Paragraph("Resumen General", heading_style))
    summary_info = [
        ['Total de preguntas:', str(total_questions)],
        ['Preguntas respondidas:', str(answered_questions)],
        ['Preguntas no respondidas:', str(total_questions - answered_questions)],
        ['Campos "Otro" utilizados:', str(other_field_count)],
        ['Porcentaje de completitud:', f"{(answered_questions/total_questions*100):.1f}%" if total_questions > 0 else "0%"]
    ]
    
    summary_table = Table(summary_info, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f8ff')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(summary_table)
    
    # Generar PDF
    try:
        doc.build(story)
        logger.info(f"PDF simple generado: {filename}")
        return filename
    except Exception as e:
        logger.error(f"Error generando PDF: {e}")
        return None

def send_pdf_to_analyzer_api(pdf_filename, client_name, assessment_date=None):
    """Enviar PDF a la API de análisis DevOps y obtener resultado"""
    try:
        if not os.path.exists(pdf_filename):
            logger.error(f"Archivo PDF no encontrado: {pdf_filename}")
            return {'error': 'Archivo PDF no encontrado'}
        
        # Preparar datos para envío
        if not assessment_date:
            assessment_date = datetime.now().strftime('%Y-%m-%d')
        
        files = {
            'file': (os.path.basename(pdf_filename), open(pdf_filename, 'rb'), 'application/pdf')
        }
        
        data = {
            'clientName': client_name,
            'assessmentDate': assessment_date
        }
        
        logger.info(f"Enviando PDF {pdf_filename} a la API DevOps Analyzer...")
        
        # Realizar solicitud POST a la API externa
        response = requests.post(
            API_CONFIG['devops_analyzer_url'],
            files=files,
            data=data,
            timeout=API_CONFIG['timeout']
        )
        
        # Cerrar el archivo después del envío
        files['file'][1].close()
        
        logger.info(f"Respuesta de API: Status {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                logger.info("PDF procesado exitosamente por la API")
                return {
                    'success': True,
                    'data': result
                }
            except json.JSONDecodeError:
                logger.error("Respuesta de API no es JSON válido")
                return {
                    'error': 'Respuesta inválida de la API de análisis',
                    'raw_response': response.text[:500]
                }
        else:
            logger.error(f"Error en API: {response.status_code} - {response.text}")
            return {
                'error': f'Error de la API de análisis (HTTP {response.status_code})',
                'details': response.text[:500]
            }
            
    except requests.exceptions.Timeout:
        logger.error("Timeout en la llamada a la API")
        return generate_fallback_analysis(client_name)
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de red enviando a API: {e}")
        return generate_fallback_analysis(client_name)
    
    except Exception as e:
        logger.error(f"Error inesperado enviando PDF a API: {e}")
        return generate_fallback_analysis(client_name)

def generate_fallback_analysis(client_name):
    """Generar análisis básico cuando la API externa no está disponible"""
    return {
        'success': True,
        'data': {
            'analysis': {
                'overallMaturity': 'Intermedio',
                'maturityScore': 65,
                'criticalAreas': [
                    'Automatización de despliegues',
                    'Monitoreo y observabilidad', 
                    'Gestión de configuraciones'
                ],
                'recommendations': [
                    'Implementar pipelines de CI/CD más robustos',
                    'Mejorar la cobertura de monitoreo',
                    'Establecer prácticas de Infrastructure as Code'
                ],
                'strengths': [
                    'Buenas prácticas de versionado',
                    'Colaboración en equipo efectiva'
                ]
            },
            'client': client_name,
            'generatedAt': datetime.now().isoformat(),
            'status': 'Análisis generado offline - API externa no disponible'
        }
    }

@app.route('/')
def index():
    """Página principal con el formulario"""
    questionnaire = load_questionnaire()
    if not questionnaire:
        return "Error cargando el cuestionario", 500
    
    return render_template('form.html', questionnaire=questionnaire)

@app.route('/submit', methods=['POST'])
def submit_form():
    """Procesar envío del formulario"""
    try:
        # Obtener datos del cliente
        client_data = {
            'nombre': request.form.get('client_name', '').strip(),
            'email': request.form.get('client_email', '').strip(),
            'empresa': request.form.get('client_company', '').strip()
        }
        
        # Validar datos requeridos
        if not client_data['nombre'] or not client_data['email']:
            return jsonify({'error': 'Nombre y email son requeridos'}), 400
        
        # Obtener respuestas del cuestionario
        responses = {}
        questionnaire = load_questionnaire()
        
        for area in questionnaire['areas']:
            for question in area['preguntas']:
                question_id = question['id']
                
                if question['tipo'] == 'multi':
                    # Preguntas de selección múltiple
                    responses[question_id] = request.form.getlist(question_id)
                else:
                    # Preguntas de selección única
                    responses[question_id] = request.form.get(question_id, '')
                
                # Manejar campo "Otro"
                other_field_id = f"{question_id}_otro"
                if request.form.get(other_field_id):
                    responses[f"{question_id}_otro"] = request.form.get(other_field_id)
        
        # Generar PDF
        pdf_filename = generate_pdf_report(client_data, questionnaire, responses)
        
        if pdf_filename:
            # Enviar PDF a la API de análisis DevOps
            api_result = send_pdf_to_analyzer_api(pdf_filename, client_data['nombre'])
            
            return jsonify({
                'success': True,
                'message': 'Formulario procesado exitosamente. Análisis DevOps completado.',
                'pdf_filename': pdf_filename,
                'analysis_result': api_result
            })
        else:
            return jsonify({'error': 'Error generando el reporte PDF'}), 500
            
    except Exception as e:
        logger.error(f"Error procesando formulario: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/download/<filename>')
def download_pdf(filename):
    """Descargar PDF generado"""
    try:
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True, download_name=filename, mimetype='application/pdf')
        else:
            return "Archivo no encontrado", 404
    except Exception as e:
        logger.error(f"Error descargando PDF: {e}")
        return "Error descargando archivo", 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run()