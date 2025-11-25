# 🪪 events-certificates-service — Documentação da API

## 📝 Resumo

- Serviço responsável pela **emissão, validação e listagem de certificados em PDF**.
- **Base path:** `/certificados`

---

# 📌 Endpoints

## 1️⃣ Emitir certificado

**POST** `/certificados/emitir/{id_inscricao}`

### Parâmetros

| Nome           | Tipo    | Local | Descrição                                |
| -------------- | ------- | ----- | ---------------------------------------- |
| `id_inscricao` | integer | path  | ID da inscrição para gerar o certificado |

### Respostas

- ✔️ **200** — retorna o PDF do certificado (`Content-Type: application/pdf`)
- ❌ **500** — erro ao gerar certificado

### Exemplo cURL (baixar o PDF)

```bash
curl -v -X POST "http://localhost:8085/certificados/emitir/123" -o certificado.pdf
```

---

## 2️⃣ Validar e baixar certificado por hash

**GET** `/certificados/validar/{hash_confirmacao}`

### Parâmetros

| Nome               | Tipo   | Local | Descrição                               |
| ------------------ | ------ | ----- | --------------------------------------- |
| `hash_confirmacao` | string | path  | Hash único que identifica o certificado |

### Respostas

- ✔️ **200** — retorna o PDF correspondente
- ❌ **404** — certificado não encontrado ou arquivo ausente

### Exemplo cURL

```bash
curl -v "http://localhost:8085/certificados/validar/9c25d10a75524ed6b3be50f490e48436"
```

---

## 3️⃣ Listar certificados de um usuário

**GET** `/certificados`

### Query params

| Nome         | Tipo    | Descrição                                   |
| ------------ | ------- | ------------------------------------------- |
| `id_usuario` | integer | ID do usuário proprietário dos certificados |

### Respostas

#### ✔️ 200 — Lista de certificados

```json
{
  "certificados": [
    {
      "hash_confirmacao": "abcd1234",
      "data_emissao": "2025-11-24T10:00:00",
      "evento": {
        "titulo": "Nome do Evento",
        "data_inicio": "2025-10-01",
        "data_fim": "2025-10-02",
        "local": "Local do Evento"
      }
    }
  ]
}
```

#### ❌ 404 — usuário não possui certificados
