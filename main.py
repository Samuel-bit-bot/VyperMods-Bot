import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

# Cargar variables de entorno
load_dotenv()


# Configuración del bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.invites = True  # <-- AGREGAR ESTA LÍNEA

# Configurar el bot
bot = commands.Bot(command_prefix='!', intents=intents)


# ID del canal de bienvenida
WELCOME_CHANNEL_ID = 1444535044277534931

# ID del canal de despedida
GOODBYE_CHANNEL_ID = 1444541465580540097  # Canal de despedida actualizado

# ID del rol automático (autorole)
AUTOROLE_ID = 1428535811850240082  # Cambia esto por el ID del rol que quieres asignar

# Configuraci�n del sistema de tickets
TICKET_CATEGORY_ID = 123456789012345678
SUPPORT_ROLE_ID = 987654321098765432
TICKET_LOGS_CHANNEL_ID = 112233445566778899

# Para evitar mensajes duplicados
last_welcome = {}

# Almacenamiento de tickets en memoria
tickets = {}


@bot.event
async def on_member_join(member):
    """Envía un mensaje de bienvenida cuando un nuevo miembro se une al servidor."""
    try:
        # Siempre procesar nuevos miembros (sin cooldown para re-entradas)
        current_time = discord.utils.utcnow()
        last_welcome[member.id] = current_time

        welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)

        if welcome_channel is None:
            print(f"No se pudo encontrar el canal de bienvenida con ID: {WELCOME_CHANNEL_ID}")
            return

        if not welcome_channel.permissions_for(welcome_channel.guild.me).send_messages:
            print("No tengo permisos para enviar mensajes en el canal de bienvenida")
            return

        member_count = member.guild.member_count

        # Crear el mensaje de bienvenida
        embed = discord.Embed(
            title=f"**🎉 𝗕𝗜𝗘𝗡𝗩𝗜𝗗𝗢 𝗔 𝗩𝗬𝗣𝗘𝗥 𝗠𝗢𝗗𝗦  🎉**",
            description=f"**Hola {member.mention} eres el miembro #{member_count}!**\n\n"

            f"**👑 Para conocer más sobre nuestros productos, revisa nuestros canales:**\n\n"
              f"•  <#1441593476415226059>\n"
              f"•  <#1441593489329750237>\n"
              f"•  <#1443697381362241768>\n\n"
              f"**📌 Reglas importantes**\n\n"
              f"•  Por favor lee las <#1444538512971010229>\n"
              f"• Diviértete y comparte\n\n"
              f"**💡 ¿Necesitas ayuda?**\n\n"
              f"• Pregunta a los moderadores\n"
              f"• Usa los comandos de ayuda",
            color=0x00ff00
        )

        # Añadir imagen grande (GIF)
        embed.set_image(url="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/Logo-VyperMods.png")

        # Añadir thumbnail con logo estático
        embed.set_thumbnail(url="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/banner.gif")

        # Añadir pie de página con ícono estático
        embed.set_footer(
            text="Created by MonitoSamuel",
            icon_url="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/Logo-VyperMods.png"
        )

        # Eliminar mensajes anteriores de bienvenida para este usuario
        async for message in welcome_channel.history(limit=10):
            if message.author == bot.user and message.embeds and member.mention in message.embeds[0].description:
                try:
                    await message.delete()
                except:
                    pass

        # Enviar mensaje de bienvenida
        mensaje = await welcome_channel.send(embed=embed)

        # Añadir reacciones
        try:
            await mensaje.add_reaction('👋')
        except Exception as e:
            print(f"Error al agregar reacciones: {e}")

        print(f"Mensaje de bienvenida enviado a {member.name}")

        # Asignar rol automático (autorole)
        if AUTOROLE_ID is not None:
            try:
                print(f"Intentando asignar rol con ID: {AUTOROLE_ID}")
                role = member.guild.get_role(AUTOROLE_ID)
                if role is None:
                    print(f"No se pudo encontrar el rol con ID: {AUTOROLE_ID}")
                    print(f"Roles disponibles: {[r.name + ' (ID: ' + str(r.id) + ')' for r in member.guild.roles]}")
                else:
                    print(f"Rol encontrado: '{role.name}' (ID: {role.id})")
                    print(f"Bot tiene permisos: {member.guild.me.guild_permissions.manage_roles}")
                    print(f"Posición del bot: {member.guild.me.top_role.position}")
                    print(f"Posición del rol: {role.position}")
                    print(f"Roles actuales del miembro: {[r.name for r in member.roles]}")

                    # Verificar si ya tiene el rol
                    if role in member.roles:
                        print(f"El miembro ya tiene el rol '{role.name}', pero se verificará nuevamente")

                    await member.add_roles(role, reason="Autorole automático")
                    print(f"Rol '{role.name}' asignado exitosamente a {member.name}")
            except discord.Forbidden as e:
                print(f"Error de permisos al asignar rol: {e}")
                print(f"Bot tiene permiso manage_roles: {member.guild.me.guild_permissions.manage_roles}")
            except discord.HTTPException as e:
                print(f"Error HTTP al asignar rol: {e}")
            except Exception as e:
                print(f"Error inesperado al asignar rol: {e}")
                import traceback
                traceback.print_exc()

    except Exception as e:
        print(f"Error al enviar mensaje de bienvenida: {e}")

        # Asegúrate de que 'bot' sea el nombre de tu instancia de comandos (commands.Bot o discord.Client)
@bot.event
async def on_member_remove(member):
    """Envía un mensaje de despedida cuando un miembro sale del servidor."""
    
    # Ignorar si el usuario es un bot para evitar logs innecesarios
    if member.bot:
        return
        
    try:
        # Usamos member.guild.get_channel() o bot.get_channel() si tienes el ID.
        # Usar bot.get_channel() es mejor si el ID está definido globalmente.
        goodbye_channel = bot.get_channel(GOODBYE_CHANNEL_ID)
        
        if goodbye_channel is None:
            # Puedes usar member.guild.name si no se encuentra el canal, para saber de qué servidor viene el error
            print(f"No se pudo encontrar el canal de despedida con ID: {GOODBYE_CHANNEL_ID} en el servidor {member.guild.name}.")
            return
            
        # Verificar permisos
        if not goodbye_channel.permissions_for(goodbye_channel.guild.me).send_messages:
            print(f"No tengo permisos para enviar mensajes en el canal de despedida: {goodbye_channel.name}")
            return
        
        # Crear mensaje de despedida (Completando tu código)
        embed = discord.Embed(
            title=f"**👋 𝗔𝗗𝗜𝗢𝗦 𝗗𝗘 𝗩𝗬𝗣𝗘𝗥 𝗠𝗢𝗗𝗦 👋**",
            description=f"**{member.mention}** Ojala no vuelvas",
            color=discord.Color.dark_red(),
            timestamp=discord.utils.utcnow()
        )
        
        embed.add_field(
            name="Información",
            value=f"Se fue un gay: `{member.name}#{member.discriminator}`",
            inline=False
        )
        
        embed.add_field(
            name="Miembros Restantes",
            value=f"El servidor ahora tiene **{member.guild.member_count}** miembros.",
            inline=True
        )

        # Añadir imagen grande (GIF)
        embed.set_image(url="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/Logo-VyperMods.png")

        # Añadir thumbnail con logo estático
        embed.set_thumbnail(url="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/banner.gif")

        # Añadir pie de página con ícono estático
        embed.set_footer(
            text="Created by MonitoSamuel",
            icon_url="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/Logo-VyperMods.png"
        )
        
        await goodbye_channel.send(embed=embed)

    except Exception as e:
        print(f"Error general al procesar on_member_remove para {member.display_name}: {e}")

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    
    # Enviar mensaje del sistema de tickets
    ticket_channel = bot.get_channel(1441593476415226059)
    if ticket_channel:
        embed = discord.Embed(
            title='Sistema de Tickets',
            description='Haz clic en el botón de abajo para crear un ticket de soporte.\n\nNuestro equipo te ayudará lo antes posible.',
            color=discord.Color.blue()
        )
        embed.set_footer(text='Crea un ticket para recibir ayuda')
        await ticket_channel.send(embed=embed, view=TicketPanelView())
    
    # Cargar extensiones
    EXTENSIONS = ['rpc_status']
    for extension in EXTENSIONS:
        try:
            await bot.load_extension(extension)
            print(f"Extensión cargada: {extension}")
        except Exception as e:
            print(f"Error al cargar {extension}: {e}")

# Iniciar el bot
if __name__ == "__main__":
    TOKEN = os.getenv('DISCORD_TOKEN')
    if not TOKEN:
        print("Error: No se encontró el token de Discord en las variables de entorno")
    else:
        while True:
            try:
                print("Iniciando bot...")
                bot.run(TOKEN)
            except Exception as e:
                print(f"Bot desconectado: {e}")
                print("Reiniciando en 10 segundos...")
from discord.ui import Modal, TextInput, View, button
from discord import ButtonStyle, Interaction

class TicketModal(Modal, title='Formulario de Soporte'):
    def __init__(self):
        super().__init__()
        
        dias = TextInput(
            label='�Cu�ntos d�as deseas adquirir?',
            placeholder='Ej: 7, 15, 30...',
            style=discord.TextStyle.short,
            required=True,
            max_length=10
        )
        
        metodo_pago = TextInput(
            label='�Qu� m�todo de pago usar�s?',
            placeholder='Ej: PayPal, Tarjeta, Transferencia...',
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        
        descripcion = TextInput(
            label='Descripci�n adicional',
            placeholder='Describe tu solicitud o problema...',
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=1000
        )
        
        self.add_item(dias)
        self.add_item(metodo_pago)
        self.add_item(descripcion)
    
    async def on_submit(self, interaction: Interaction):
        dias = self.children[0].value
        metodo_pago = self.children[1].value
        descripcion = self.children[2].value
        
        await self.create_ticket(interaction, dias, metodo_pago, descripcion)
    
    async def create_ticket(self, interaction: Interaction, dias: str, metodo_pago: str, descripcion: str):
        guild = interaction.guild
        user = interaction.user
        
        # Crear categor�a si no existe
        category = discord.utils.get(guild.categories, name='Tickets')
        if not category:
            category = await guild.create_category('Tickets')
        
        # Configurar permisos del canal
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
        
        # Crear canal del ticket
        ticket_number = len([c for c in guild.text_channels if c.name.startswith('ticket-')]) + 1
        channel_name = f'ticket-{ticket_number:04d}-{user.name}'
        
        try:
            ticket_channel = await guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites
            )
            
            # Enviar mensaje de confirmaci�n
            await interaction.response.send_message(
                f'�Ticket creado! Ve a {ticket_channel.mention} para continuar.',
                ephemeral=True
            )
            
            # Crear embed para el ticket
            embed = discord.Embed(
                title=f'Ticket #{ticket_number} - {user.name}',
                description='**D�as solicitados:** ' + dias + '\\n**M�todo de Pago:** ' + metodo_pago + '\\n**Descripci�n:** ' + (descripcion or 'No proporcionada'),
                color=discord.Color.blue()
            )
            
            embed.set_footer(text=f'Creado por {user.name} | ID: {user.id}')
            
            await ticket_channel.send(f'{user.mention} �Tu ticket ha sido creado!', embed=embed, view=TicketControlView())
            
        except Exception as e:
            await interaction.response.send_message(f'Error al crear el ticket: {str(e)}', ephemeral=True)

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label='Cerrar Ticket', style=ButtonStyle.red, custom_id='close_ticket')
    async def close_ticket_button(self, interaction: Interaction, button: button):
        await interaction.response.send_message('�Est�s seguro de que quieres cerrar este ticket?', view=ConfirmCloseView(), ephemeral=True)
    
    @button(label='Reclamar Ticket', style=ButtonStyle.blurple, custom_id='claim_ticket')
    async def claim_ticket_button(self, interaction: Interaction, button: button):
        await interaction.response.send_message(f'{interaction.user.mention} ha reclamado este ticket.', ephemeral=False)
        button.disabled = True
        await interaction.message.edit(view=self)

class ConfirmCloseView(View):
    def __init__(self):
        super().__init__(timeout=60)
    
    @button(label='Confirmar Cierre', style=ButtonStyle.red, custom_id='confirm_close')
    async def confirm_close(self, interaction: Interaction, button: button):
        await interaction.channel.delete()
    
    @button(label='Cancelar', style=ButtonStyle.grey, custom_id='cancel_close')
    async def cancel_close(self, interaction: Interaction, button: button):
        await interaction.response.send_message('Cierre de ticket cancelado.', ephemeral=True)
        await interaction.message.delete()

class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label='Crear Ticket', style=ButtonStyle.green, custom_id='create_ticket_panel')
    async def create_ticket_panel(self, interaction: Interaction, button: button):
        await interaction.response.send_modal(TicketModal())
