import requests
import json

def generate_diagram(diagram_type, content, filename):
    url = 'http://localhost:3000/generate-diagram'
    payload = {
        'diagramType': diagram_type,
        'content': content,
        'filename': filename
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        result = response.json()
        print(f"Diagram generated successfully!")
        print(f"File saved at: {result['filePath']}")
    else:
        print(f"Error generating diagram: {response.text}")

# Example: Generate a flowchart
flowchart_content = """
graph TD
    A[Start] --> B[Process Data]
    B --> C[Transform]
    C --> D[Load]
    D --> E[End]
"""

generate_diagram('flowchart', flowchart_content, 'test_flowchart') 