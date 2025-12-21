# VyperMods Bot

Un bot simple de Discord que envía un mensaje con enlaces útiles a un canal específico.

## Características
- Envía un mensaje con enlaces a drivers, emuladores y versiones de Free Fire
- Fácil de configurar
- Sin comandos, solo envía el mensaje al iniciar

## Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## Instalación

1. Descarga los archivos del bot
2. Instala las dependencias:
   ```
   pip install discord.py python-dotenv
   ```
3. Crea un archivo `.env` y configura tu token de bot:
   ```
   DISCORD_TOKEN=tu_token_aquí
   ```

## Configuración

1. Crea un bot en el [Portal de Desarrolladores de Discord](https://discord.com/developers/applications)
2. Ve a "Bot" y haz clic en "Add Bot"
3. Copia el token del bot y pégualo en el archivo `.env`
4. En `main.py`, cambia el ID del canal (línea 21) al canal donde quieres que se envíe el mensaje:
   ```python
   TARGET_CHANNEL_ID = 1234567890  # Reemplaza con el ID de tu canal
   ```

## Uso

1. Inicia el bot:
   ```
   python main.py
   ```
   O si no funciona, prueba con:
   ```
   py main.py
   ```

2. El bot enviará automáticamente el mensaje al canal especificado y se apagará.

## Personalización

Puedes personalizar los mensajes editando el archivo `main.py`. Los mensajes de bienvenida, los requisitos, emuladores y versiones de Free Fire se pueden modificar según tus necesidades.

## Notas

- Asegúrate de que el bot tenga los permisos necesarios en tu servidor de Discord.
- Para que el mensaje de bienvenida funcione correctamente, asegúrate de que el canal del sistema esté configurado en la configuración del servidor.
