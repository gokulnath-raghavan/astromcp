import express, { Request, Response, RequestHandler } from 'express';
import mermaid from 'mermaid';
import { writeFileSync } from 'fs';
import { join } from 'path';

const app = express();
const port = 3000;

// Initialize mermaid
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
});

app.use(express.json());

// Create diagrams directory if it doesn't exist
const diagramsDir = join(__dirname, 'diagrams');
if (!require('fs').existsSync(diagramsDir)) {
    require('fs').mkdirSync(diagramsDir);
}

// Endpoint to generate diagram
const generateDiagramHandler: RequestHandler = async (req, res) => {
    try {
        const { diagramType, content, filename } = req.body;
        
        if (!diagramType || !content || !filename) {
            res.status(400).json({ error: 'Missing required parameters' });
            return;
        }

        // Generate SVG using mermaid
        const { svg } = await mermaid.render(filename, content);
        
        // Save SVG to file
        const filePath = join(diagramsDir, `${filename}.svg`);
        writeFileSync(filePath, svg);

        res.json({
            success: true,
            filePath,
            svg
        });
    } catch (error) {
        console.error('Error generating diagram:', error);
        res.status(500).json({ error: 'Failed to generate diagram' });
    }
};

app.post('/generate-diagram', generateDiagramHandler);

// Endpoint to list generated diagrams
const listDiagramsHandler: RequestHandler = (req, res) => {
    const files = require('fs').readdirSync(diagramsDir);
    res.json({ diagrams: files });
};

app.get('/diagrams', listDiagramsHandler);

app.listen(port, () => {
    console.log(`Diagram server running at http://localhost:${port}`);
}); 