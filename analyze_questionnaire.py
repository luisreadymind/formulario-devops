#!/usr/bin/env python3
"""
Script para obtener detalles específicos del error de validación
"""

import requests
import json

def get_questionnaire_structure():
    """Obtener la estructura real del cuestionario desde el servidor"""
    try:
        url = "https://formulario-devops-s2uxxgzelbnnk.azurewebsites.net/"
        response = requests.get(url)
        
        if response.status_code == 200:
            html_content = response.text
            
            # Intentar envío vacío para ver qué preguntas exactas se esperan
            submit_url = url.rstrip('/') + '/submit'
            empty_response = requests.post(submit_url, data={
                'client_name': 'Test',
                'client_email': 'test@test.com',
                'client_company': 'Test Company'
            })
            
            if empty_response.status_code == 400:
                error_data = empty_response.json()
                print("📋 ESTRUCTURA REAL DEL CUESTIONARIO:")
                print("=" * 60)
                print(f"Total de preguntas: {error_data.get('total_questions', 'N/A')}")
                print(f"Preguntas sin responder: {len(error_data.get('unanswered_questions', []))}")
                print()
                
                print("📝 LISTA DE PREGUNTAS REQUERIDAS:")
                print("-" * 40)
                
                for i, question in enumerate(error_data.get('unanswered_questions', []), 1):
                    area = question.get('area', 'N/A')
                    q_id = question.get('id', 'N/A')
                    title = question.get('title', 'N/A')[:60] + '...' if len(question.get('title', '')) > 60 else question.get('title', 'N/A')
                    
                    print(f"{i:2d}. [{q_id}] {area}")
                    print(f"    {title}")
                    print()
                
                # Guardar estructura completa en JSON
                with open('questionnaire_structure.json', 'w', encoding='utf-8') as f:
                    json.dump(error_data, f, indent=2, ensure_ascii=False)
                
                print("💾 Estructura completa guardada en: questionnaire_structure.json")
                return error_data
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🔍 ANALIZANDO ESTRUCTURA DEL CUESTIONARIO DEVOPS")
    print("=" * 60)
    get_questionnaire_structure()