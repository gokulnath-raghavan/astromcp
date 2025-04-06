"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const mermaid_1 = __importDefault(require("mermaid"));
const fs_1 = require("fs");
const path_1 = require("path");
const app = (0, express_1.default)();
const port = 3000;
// Initialize mermaid
mermaid_1.default.initialize({
    startOnLoad: true,
    theme: 'default',
    securityLevel: 'loose',
});
app.use(express_1.default.json());
// Create diagrams directory if it doesn't exist
const diagramsDir = (0, path_1.join)(__dirname, 'diagrams');
if (!require('fs').existsSync(diagramsDir)) {
    require('fs').mkdirSync(diagramsDir);
}
// Endpoint to generate diagram
const generateDiagramHandler = (req, res) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const { diagramType, content, filename } = req.body;
        if (!diagramType || !content || !filename) {
            res.status(400).json({ error: 'Missing required parameters' });
            return;
        }
        // Generate SVG using mermaid
        const { svg } = yield mermaid_1.default.render(filename, content);
        // Save SVG to file
        const filePath = (0, path_1.join)(diagramsDir, `${filename}.svg`);
        (0, fs_1.writeFileSync)(filePath, svg);
        res.json({
            success: true,
            filePath,
            svg
        });
    }
    catch (error) {
        console.error('Error generating diagram:', error);
        res.status(500).json({ error: 'Failed to generate diagram' });
    }
});
app.post('/generate-diagram', generateDiagramHandler);
// Endpoint to list generated diagrams
const listDiagramsHandler = (req, res) => {
    const files = require('fs').readdirSync(diagramsDir);
    res.json({ diagrams: files });
};
app.get('/diagrams', listDiagramsHandler);
app.listen(port, () => {
    console.log(`Diagram server running at http://localhost:${port}`);
});
