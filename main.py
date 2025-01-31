from modules.pte_manager import get_server_ids, get_server_info
from modules.database_manager import set_data, check_data, get_data
from modules.commands import status, power_options
from pydactyl import PterodactylClient
import discord
from discord import option
import time

def main():
    intents = discord.Intents.all()
    bot = discord.Bot(intents = intents)

    # for logging
    def ctime():
        return f"{time.strftime("%d-%m-%y | %H:%M:%S: ")}"

    # checks
    @bot.event
    async def on_ready():
        print(f"{ctime()}logged in as {bot.user}, total guild count: {len(bot.guilds)}, all guilds i am in:")
        for servers in bot.guilds:
            print(servers)
    @bot.event
    async def on_guild_join(guild: discord.guild):
        check_data(guild.id) # to make a database entry if server has none


    @bot.slash_command()
    @discord.default_permissions(administrator=True,)
    @option("url", description = f"The url of your pte panel")
    @option("api_key", description = f"the api key from your pte panel")
    async def set_api(ctx: discord.ApplicationContext, url: str, api_key: str):
        try:
            set_data("servers", ctx.guild.id, "url", url)
            set_data("servers", ctx.guild.id, "api_key", api_key)
        except Exception as err:
            await ctx.respond(f"error: {err}")
        await ctx.respond("success")


    # so people can test if the api key works.
    @bot.slash_command()
    @discord.default_permissions(administrator=True,)
    async def testkey(ctx: discord.ApplicationContext):
        response = ""
        try:
            api = PterodactylClient(get_data("servers", ctx.guild_id, "url"),
                                    get_data("servers", ctx.guild_id, "api_key"))
            permissions = api.client.account.get_account()
            await ctx.respond(f"Api holder is\nadmin: {permissions['attributes']['admin']}\nroot admin: {permissions['attributes']['root_admin']}")
        except Exception as err:
            await ctx.respond(f"there is an error, probably api key not working: {err}")

    async def server_search(ctx: discord.AutocompleteContext):
        # why are you like this?
        # why when status_per_server is active must you shit yourself?
        # why won't you work while another command is active?
        # why must I suffer?
        try:
            print(f"{ctime()}trying to get data")
            api = PterodactylClient(get_data("servers", ctx.interaction.guild_id, "url"),
                                    get_data("servers", ctx.interaction.guild_id, "api_key"))
            ids = get_server_ids(api)
            names = []
            for iden in ids:
                names += [get_server_info(iden, api).name]
            if names is []:
                names = ["No servers available"]
            return names
        except Exception as err:
            print(f"something fucking annoying has happend: {err}")
            return ["something went wrong, please try again"]
        # mf just does nothing if |  is fucking active like if it has the live updating and the thread is still active
        # why do you do just fuck | ing nothing
        # Like the print() just  \|/ doesn't output anything as long as that command is active

    @bot.slash_command(name="status")
    @option("name", description = "name of the server", autocomplete=server_search)
    async def status_per_server(ctx: discord.ApplicationContext, name: str):
        try:
            if name == "No servers available":
                await ctx.respond("There are no servers available, make one via the pte panel!")
                return
            api = PterodactylClient(get_data("servers", ctx.interaction.guild_id, "url"),
                                    get_data("servers", ctx.interaction.guild_id, "api_key"))
            await status(ctx, name, api)
        except Exception as err:
            await ctx.respond(f"Something went wrong: {err}")

    @bot.slash_command(name="power")
    @option("name", description = "name of the server", autocomplete=server_search)
    @option("option", choices = ["start", "stop", "restart"])
    @option("timer", description = "How long before the action is done in seconds", input_type=int, min_value = 0, max_value = 120, default = 0)
    async def power(ctx: discord.ApplicationContext, name: str, option: str, timer:int):
        try:
            if name == "No servers available":
                await ctx.respond("There are no servers available, make one via the pte panel!")
                return
            api = PterodactylClient(get_data("servers", ctx.interaction.guild_id, "url"),
                                    get_data("servers", ctx.interaction.guild_id, "api_key"))
            await power_options(ctx, name, option, timer, api)
        except Exception as err:
            await ctx.respond(f"Something went wrong: {err}")

    bot.run("DISCORD_BOT_TOKEN")


if __name__ == "__main__":
    main()