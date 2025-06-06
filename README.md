
# Piper TTS API

API Flask que utiliza o Piper para gerar áudio com voz natural (TTS).

## Endpoint

`POST /tts`

**Body JSON:**
```json
{
  "text": "Olá, tudo bem?"
}
```

**Resposta:** arquivo de áudio `.wav` com a voz.

---

Este projeto inclui:

- Código do Piper (`piper/`)
- Modelo de voz pt_BR-faber-medium (.onnx)
- API Flask pronta para deploy no Railway
