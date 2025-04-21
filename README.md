# WhatsApp Automation Bot – Soporte Operativo para Exchange

Bot desarrollado en Python para automatizar interacciones en WhatsApp Web usando Selenium y Web Scraping. Sirvió como asistente operativo para un equipo que gestionaba tareas en un exchange.

## 🧠 ¿Cómo funciona?

- Lee mensajes en WhatsApp Web desde contactos específicos (usando Selenium).
- Se activa si detecta la palabra clave `bot` en el mensaje.
- Despliega un menú de funciones relacionadas con la operativa: 
  - Consulta de saldos
  - Accesos a cuentas bancarias
  - Envío de documentos
  - Otros accesos clave
- Si no hay respuesta en 2 minutos, se desactiva del chat.
- Cuando está inactivo, el chat funciona como una conversación normal (humana).

## ⚙️ Tecnologías utilizadas

- Python
- Selenium
- Web Scraping (WhatsApp Web)
- Lógica de sesión y temporización

## 💡 Aplicación real

Este bot funcionaba en conjunto con [exchange-validation-bot](https://github.com/Mogo943/Bot-ana), automatizando la comunicación operativa con el equipo mediante WhatsApp Web y reduciendo intervención manual.

---

**Autor:** Carlos Mogollón  
[LinkedIn](https://www.linkedin.com/in/carlosmogollon-it/)
