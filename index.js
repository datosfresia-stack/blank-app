const express = require('express');
const cors = require('cors');
const { Configuration, OpenAIApi } = require('openai');

const app = express();
app.use(cors());
app.use(express.json());

// 🗝️ TOMAMOS LAS CLAVES
const OPENAI_KEY = process.env.OPENAI_API_KEY;
const configuration = new Configuration({ apiKey: OPENAI_KEY });
const openai = new OpenAIApi(configuration);

// 🚀 RUTA DEL CHAT
app.post('/chat', async (req, res) => {
  try {
    const { mensaje } = req.body;
    console.log("Mensaje recibido:", mensaje);

    const respuesta = await openai.createChatCompletion({
      model: "gpt-3.5-turbo",
      messages: [
        { role: "system", content: "Eres IA Libre, un asistente muy inteligente y amigable. Responde en español claro y preciso." },
        { role: "user", content: mensaje }
      ],
      temperature: 0.7
    });

    res.send(respuesta.data.choices[0].message.content);

  } catch (error) {
    console.error("ERROR:", error);
    res.status(500).send("❌ Error: " + error.message);
  }
});

// 🟢 INICIAR SERVIDOR
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`✅ Servidor LISTO y corriendo en puerto ${PORT}`);
});
