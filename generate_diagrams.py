import os
from pathlib import Path
import subprocess

class DiagramGenerator:
    def __init__(self, output_dir='diagrams'):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_diagram(self, name, content):
        # Create a DOT file for the diagram
        dot_file = self.output_dir / f"{name}.dot"
        with open(dot_file, 'w') as f:
            f.write(self.create_dot_content(content))
        
        print(f"Generated {name}.dot")
        print(f"To visualize this diagram, you can:")
        print("1. Visit https://dreampuf.github.io/GraphvizOnline/")
        print("2. Copy the contents of the .dot file")
        print("3. Paste it into the online editor")
        print("\n---\n")

    def create_dot_content(self, content):
        # Convert our diagram description to DOT format
        dot = ['digraph G {']
        dot.append('  rankdir=LR;')  # Left to right direction
        dot.append('  node [shape=box];')  # Box shape for nodes

        # Add nodes and edges based on content
        for line in content.split('\n'):
            if '->' in line:
                source, target = line.split('->')
                dot.append(f'  "{source.strip()}" -> "{target.strip()}";')
            elif '[' in line and ']' in line:
                node = line.strip()
                name = node[0:node.index('[')]
                label = node[node.index('[')+1:node.index(']')]
                dot.append(f'  "{name}" [label="{label}"];')

        dot.append('}')
        return '\n'.join(dot)

# Create generator instance
generator = DiagramGenerator()

# 1. ETL Pipeline Overview
pipeline = """
Start_Pipeline[Start Pipeline Lambda]
Setup_Jobs[Setup Jobs Lambda]
Check_Dependencies[Check Dependencies Lambda]
Update_Status[Update Status Lambda]
Run_Glue[Run Glue Job Lambda]
Monitor[Monitor Glue Jobs Lambda]
Notify[Send Notification Lambda]

Start_Pipeline->Setup_Jobs
Setup_Jobs->Check_Dependencies
Check_Dependencies->Update_Status
Update_Status->Run_Glue
Run_Glue->Monitor
Monitor->Update_Status
Update_Status->Notify
"""
generator.generate_diagram('pipeline', pipeline)

# 2. Job Flow
job_flow = """
Scheduler[CloudWatch]
Lambda[ETL Controller]
Glue[Glue Job]
Control[Control Tables]

Scheduler->Lambda
Lambda->Control
Control->Lambda
Lambda->Glue
Glue->Control
"""
generator.generate_diagram('job_flow', job_flow)

# 3. Control Tables Relationship
tables = """
ETL_Objects[ETL Objects Table]
ETL_Dependencies[Dependencies Table]
ETL_Status[Execution Status Table]
ETL_Metrics[Metrics Table]

ETL_Objects->ETL_Dependencies
ETL_Dependencies->ETL_Status
ETL_Status->ETL_Metrics
"""
generator.generate_diagram('tables', tables)

print("Diagram files generated successfully!")
print("You can visualize them using https://dreampuf.github.io/GraphvizOnline/") 