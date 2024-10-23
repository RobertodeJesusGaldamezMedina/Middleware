const express = require('express');
const app = express();
const PORT = 3000;

// Middleware para manejar JSON
app.use(express.json());
app.use(express.static('public')); // Carpeta para servir HTML estático

// Simularemos una base de datos en memoria con un array
let notes = [];

// Ruta para obtener todas las notas
app.get('/notes', (req, res) => {
    res.json(notes);
});

// Ruta para crear una nueva nota
app.post('/notes', (req, res) => {
    const { title, content } = req.body;
    const newNote = { id: Date.now(), title, content };
    notes.push(newNote);
    res.json(newNote);
});

// Ruta para actualizar una nota
app.put('/notes/:id', (req, res) => {
    const { id } = req.params;
    const { title, content } = req.body;

    const note = notes.find(note => note.id == id);
    if (note) {
        note.title = title;
        note.content = content;
        res.json(note);
    } else {
        res.status(404).json({ message: 'Note not found' });
    }
});

// Ruta para eliminar una nota
app.delete('/notes/:id', (req, res) => {
    const { id } = req.params;
    notes = notes.filter(note => note.id != id);
    res.json({ message: 'Note deleted' });
});

// Iniciar el servidor
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
