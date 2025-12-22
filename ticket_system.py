import discord
from discord.ui import Modal, TextInput, View, button
from discord import ButtonStyle, Interaction

class TicketModal(Modal, title='Formulario de Soporte'):
    def __init__(self):
        super().__init__()
        
        dias = TextInput(
            label='¿Cuántos días deseas adquirir?',
            placeholder='Ej: 7, 15, 30...',
            style=discord.TextStyle.short,
            required=True,
            max_length=10
        )
        
        metodo_pago = TextInput(
            label='¿Qué método de pago usarás?',
            placeholder='Ej: PayPal, Tarjeta, Transferencia...',
            style=discord.TextStyle.short,
            required=True,
            max_length=50
        )
        
        descripcion = TextInput(
            label='Descripción adicional',
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
        
        # Crear categoría si no existe
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
            
            # Enviar mensaje de confirmación
            await interaction.response.send_message(
                f'¡Ticket creado! Ve a {ticket_channel.mention} para continuar.',
                ephemeral=True
            )
            
            # Crear embed para el ticket
            embed = discord.Embed(
                title=f'Ticket #{ticket_number} - {user.name}',
                description='**Días solicitados:** ' + dias + '\n**Método de Pago:** ' + metodo_pago + '\n**Descripción:** ' + (descripcion or 'No proporcionada'),
                color=discord.Color.blue()
            )
            
            embed.set_footer(text=f'Creado por {user.name} | ID: {user.id}')
            
            await ticket_channel.send(f'{user.mention} ¡Tu ticket ha sido creado!', embed=embed, view=TicketControlView())
            
        except Exception as e:
            await interaction.response.send_message(f'Error al crear el ticket: {str(e)}', ephemeral=True)

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label='Cerrar Ticket', style=ButtonStyle.red, custom_id='close_ticket')
    async def close_ticket_button(self, interaction: Interaction, button: button):
        await interaction.response.send_message('¿Estás seguro de que quieres cerrar este ticket?', view=ConfirmCloseView(), ephemeral=True)
    
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
