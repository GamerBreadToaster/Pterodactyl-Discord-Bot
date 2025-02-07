# Pte Panel Discord Bot #

this is a little discord bot I made that interacts with your pydactyl panel via discord!
You are probably better off just using your pte panel and giving your friends or mods or whatever access.

## current features
* will automatically find server names for easy selection in the discord command
* start/stop/restart a server

## things to do: ##
* Add a permissions system (maybe with discord roles) so not everyone can do everything (only administrators can change the api tho).
* Add more admin settings like making a server. I'll need to set up a local pte panel, so I can test this.
* Learn how to do webhook and websocket things so you can see console because you can't at the moment. (I do not know how these work)

## how to install: (todo)
* Bot invite link: (not yet)
* Hosting yourself can be done by getting a bot token from discord.com/developers and putting it down in main file after downloading the latest version.
* more detailed installation guide will be added soon

## Python packages needed:
* `py-cord`
* `py-dactyl`
* `adioop-lts` (only if python version is 3.13)
```commandline
py -m pip install py-cord py-dactyl audioop-lts
```