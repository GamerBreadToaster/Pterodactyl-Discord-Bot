import discord
import time
from pydactyl import PterodactylClient
from modules.pte_manager import get_server_ids, get_server_info, wait_until_update


def ctime():
    return f"{time.strftime('%d-%m-%y | %H:%M:%S: ')}"

def get_info_with_name(name: str, api: PterodactylClient):
    # To search for the server with the same name as given
    # probably breaks if two servers are the same exact name,
    # as it will choose the first one with the same name.
    # idens stands for identifications (ids is already something????).
    # with how this is setup will return last info if name doesn't match with any server because there isn't
    # anything that checks if the name is even in the server list.
    for idens in get_server_ids(api):
        info = get_server_info(idens, api)
        if info.name == name:
            break
    return info


async def status(ctx: discord.ApplicationContext, name: str, api: PterodactylClient):
    def make_embed() -> discord.Embed:
        embed = discord.Embed(
            title=info.name,
            description=info.description,
            footer=discord.EmbedFooter("API updates about every 20 seconds!") # might be different for different pte servers. am not sure.
        )
        embed.add_field(
            name="ip addres:",
            value=f"{info.ip}"
        )
        embed.add_field(
            name="uptime:",
            value=f"{round((info.uptime / 1000), 1)} s" # to round the uptime from ms to seconds
        )
        embed.add_field(
            name="state:",
            value=f"{info.state}"
        )
        embed.add_field(
            name="ram usage:",
            value=f"{info.usage_ram}/{info.max_ram}"
        )
        embed.add_field(
            name="cpu usage:",
            value=f"{info.usage_cpu}/{info.max_cpu}"
        )
        embed.add_field(
            name="disk usage:",
            value=f"{info.usage_space}/{info.max_space}"
        )
        return embed
    info = get_info_with_name(name, api)

    # prob should make live updating but when I do that something with the
    # Discord autocomplete COMPLETELY shits itself when this command is still active for no fucking reason.
    await ctx.respond(embeds=[make_embed()])

async def power_options(ctx: discord.ApplicationContext, name: str, power_option: str, timer: int, api: PterodactylClient):
    info = get_info_with_name(name, api)
    time.sleep(timer)
    api.client.servers.send_power_action(info.ids, power_option)
    if power_option == "stop": await ctx.respond(f"stopping {info.name}")
    else: await ctx.respond(f"{power_option}ing {info.name}")

def main():
    pass


if __name__ == "__main__":
    main()
