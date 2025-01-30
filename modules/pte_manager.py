from pydactyl import PterodactylClient
import time


def ctime():
    return f"{time.strftime("%d-%m-%y | %H:%M:%S: ")}"


def get_server_ids(api: PterodactylClient) -> list:
    """
    Gets all server id's from the api
    :param api:
    :return: a list of server id's
    """
    print(f"{ctime()}requesting server ids")
    servers = api.client.servers.list_servers()
    ids = []
    for server in range(len(servers)):
        ids += [servers.data[server]['attributes']['identifier']]
    return ids


def get_server_info(server_id: str, api: PterodactylClient) -> type["info"]:
    """
    Returns a class with the useful and important information of a pte server
    :param api: needed to work. Use PterodactylClient(url, api_key)
    :param server_id: string of the server id
    :return:
    """
    time_begin = time.time()
    servers = api.client.servers.get_server(server_id)
    servers_usage = api.client.servers.get_server_utilization(server_id)

    # i tried to make it a bit clear what everything is, but maybe it's just an extra api call when its not needed idk.
    class info():
        name = servers["name"]
        ids = server_id
        description = servers["description"]
        ip = servers['relationships']['allocations']['data'][0]['attributes']['ip_alias'] + ":" + str(
            servers["relationships"]["allocations"]["data"][0]["attributes"]["port"])
        max_ram = str(servers["limits"]["memory"] / 1000) + " GiB" # from MiB to GiB
        max_cpu = str(servers["limits"]["cpu"]) + "%"
        max_space = str(servers["limits"]["disk"] / 1000) + " GiB" # same here
        state = servers_usage["current_state"]
        usage_ram = round((servers_usage["resources"]["memory_bytes"] / 1000000000), 3) # from bytes to GiB (i think i did it right)
        usage_cpu = servers_usage["resources"]["cpu_absolute"]
        usage_space = round((servers_usage["resources"]["disk_bytes"] / 1000000000), 2) # same here
        uptime = servers_usage["resources"]["uptime"]
        update = None

    info.update = round((time.time() - time_begin), 4) # some info on how long it took to update.
    print(f"{ctime()}requesting server info: server_id: {server_id}, in {info.update} s")
    return info


def wait_until_update(server_id: str, api: PterodactylClient, last_uptime: int | None):
    """
    Use this to wait for a server to update because of rate_limiting
    :param last_uptime: optional param if the last uptime is already available and need to see when the next time the server updates.
    :param api: needed to work. Use PterodactylClient(url, api_key)
    :param server_id: string of the server id
    :return:
    """
    if last_uptime is None:
        info = get_server_info(server_id, api)
        last_uptime = info.uptime
    else:
        info = get_server_info(server_id, api)

    while info.uptime == last_uptime and info.state != "offline":
        info = get_server_info(server_id, api)
        time.sleep(2.5)
    # basically checks if the uptime is the same as every last time
    # so to check if the server is being rate limited and when the last update is

    # somehow this fucks everything up, I think tho.

    print("stopped")


def main():
    pass


if __name__ == "__main__":
    main()
