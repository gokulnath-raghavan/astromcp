from google.cloud import aiplatform
from google.cloud.aiplatform import NotebookLLM
import os

def initialize_notebook_llm(project_id, location="us-central1"):
    """
    Initialize connection to Google Cloud NotebookLLM.
    
    Args:
        project_id (str): Your Google Cloud project ID
        location (str): The location where your NotebookLLM instance is deployed
    """
    # Initialize the Vertex AI platform
    aiplatform.init(project=project_id, location=location)
    
    # Create a NotebookLLM instance
    notebook_llm = NotebookLLM()
    
    return notebook_llm

def main():
    # Replace with your Google Cloud project ID
    PROJECT_ID = "your-project-id"
    
    try:
        # Initialize the connection
        notebook_llm = initialize_notebook_llm(PROJECT_ID)
        print("Successfully connected to NotebookLLM!")
        
        # Example: Get model information
        model_info = notebook_llm.get_model_info()
        print(f"Model information: {model_info}")
        
    except Exception as e:
        print(f"Error connecting to NotebookLLM: {str(e)}")

if __name__ == "__main__":
    main() 