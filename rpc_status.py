import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta

class RPCStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Start counting from now
        self.start_time = datetime.utcnow()
        self.update_status.start()

    def cog_unload(self):
        self.update_status.cancel()

    @tasks.loop(seconds=30)  # Update every 30 seconds
    async def update_status(self):
        try:
            # Calculate time difference from start time
            elapsed = datetime.utcnow() - self.start_time
            days = elapsed.days
            hours, remainder = divmod(int(elapsed.total_seconds()), 3600)
            hours = hours % 24  # Get hours within current day
            minutes, _ = divmod(remainder, 60)
            
            # Format the time
            if days > 0:
                time_str = f"{days}d {hours}h {minutes}m"
            else:
                time_str = f"{hours}h {minutes}m"
            
            # Update bot's status with Vyper Mods RPC
            activity = discord.Activity(
                type=discord.ActivityType.playing,
                name="VyperMods - Bot",
                details="</> Dev: @kikitieneelbody",
                state=f"Playing VyperMods - Bot | {time_str}",
                large_image="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/Logo-VyperMods.png",  # Must be uploaded to Discord Dev Portal
                large_text="Copyright ©VyperMods - Bot",
                small_image="https://github.com/Samuel-bit-bot/URLS/releases/download/v1/banner.gif",  # Must be uploaded to Discord Dev Portal
                small_text="Rogue - Level 100"
            )
            await self.bot.change_presence(activity=activity)
            
        except Exception as e:
            print(f"Error actualizando el estado: {e}")

    @update_status.before_loop
    async def before_update_status(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(RPCStatus(bot))