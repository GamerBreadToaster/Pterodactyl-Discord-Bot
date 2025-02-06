# Pterodactyl Discord Bot #

This is a little discord bot I made that interacts with your pterodactyl (or pelican) panel via discord!

## what is this?
This project is a discord bot where users on discord can interact with the Pterodactyl servers from discord.
It is fully written in python with the use of py-cord and py-dactyl and is my first 'real' project I published to GitHub.
I used a couple of things that were fairly new to me like a database and modules, but is far from perfect, and it doesn't have features I wish I could add.
It also lacks features for the admin side, for example adding a server. This is because I only have access to the user side of Pterodactyl and only have a user api.

## current features
* will automatically find server names for easy selection in the discord command
* start/stop/restart a server
* See the status of a singular server

## things to do:
* Add a permissions system (maybe with discord roles) so not everyone can do everything (only administrators can change the api tho).
* Add more admin settings like making a server. I'll need to set up a local pte panel, so I can test this.
* Learn how to do webhook and websocket things so you can see console because you can't at the moment. (I do not know how these work)

## how to install: (todo)
* Bot invite link: (not yet)
* Hosting yourself can be done by getting a bot token from discord.com/developers and putting it down in main file after downloading the latest version.
* more detailed install guide will be added soon

## Python packages needed:
* `py-cord`
* `py-dactyl`
* `adiooop-lts` (only if python version is 3.13)