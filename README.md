# Akiro DiscordBot

## Introduction

A project in which an economic bot was developed specifically for your discord server. It contains various functions for building an economy on your server.

![Introduction](https://i.pinimg.com/originals/74/5c/c9/745cc90fcc688569610f84bc5d2b2fd6.gif)"

## Technologies were used in this project:

* [Python] (https://www.python.org): a simple syntactic programming language;
* [SQLite] (https://sqlite.org/index.html): SQLite is a software library that provides a relational database management system. It is a serverless, self-contained SQL database engine with zero configuration and transactions. SQLite is widely used in various applications due to its compact size, low maintenance costs and ease of use;
* [Discord Developer Portal] (https://discord.com/developers/applications): website for registering your application;
* [Discord.py ] (https://discord py.readthedocs.io/en/latest): library for integration with discord;

## Requirement

* To have Python version 3.11.3 installed (during development we started with version 3.11.3, so we cannot guarantee that earlier versions will work);
* Create a .env file, fill it with the following data:

```py
TOKEN = "" Bot Token
NAME = "" Bot Name
ID = "" Client ID(App)
PREFIX = "!" Prefix (To call the command)
```
* or we can change the config file and enter this data here:

```py
setting = {
    'TOKEN' : "",
    'NAME BOT' : "",
    'ID'       : "",
    'PREFIX'   : ""
}
```

## Bot system

The bot system is implemented using 2 types, experience and levels, experience is accrued weekly, or for chatting.

## Basic bot commands

### Evens
* bot.bot_ready_event() // Event triggered when the bot starts.
* bot.member_join_event() // Event triggered when a new user joins the server.
* bot.commands_error_event() // Event triggered when an error occurs in a command.
* bot.on_message_event() // Event triggered when a message is received on the server.

### Balance
* bot.balance_event() //Event triggered to get a user's balance.
* bot.give_event() // Event triggered to give money to a user.
* bot.remove_bal_event() // Event triggered to remove money from a user.
* bot.set_money_event() // Event triggered to set a user's balance.

### Shop
* bot.add_shop_event() // Event triggered to add an item to the shop.
* bot.remove_shop_event() // Event triggered to remove an item from the shop.
* bot.shop_event() // Event triggered to view items in the shop.
* bot.buy_event() // Event triggered to buy an item from the shop.

### Inventory
* bot.inventory_event() // Event triggered to view a user's inventory.
* bot.use_event() // Event triggered to use an item from the inventory.
* bot.remove_all_inventory() // Event triggered to remove all items from a user's inventory.

### Other

* bot.info_event() // Event triggered to get information about a user.
* bot.clear_event() // Event triggered to clear the chat.
* bot.roll_event() // Event triggered to roll a dice.
* bot.avatar_event() // Event triggered to change a user's avatar.
* bot.collect_event(collecting_roles, 0, 0) // Event triggered to collect funds from users with a specific role.
* bot.work_event(70000, 100000, text_work, 0, 0) // Event triggered for a user to perform a job.
* bot.remove_all_balance() // Event triggered to remove all money from a user.
* bot.remove_all_roles() // Event triggered to remove all roles from a user.
* bot.wipe_event() // Event triggered to wipe all bot data.
* bot.banner_event() // Event triggered to set a banner on the server.
* bot.level_event() // Event triggered to get a user's level.
* bot.set_xp_event() // Event triggered to set a user's experience.

#### pymongo operações

Essas informações que estão sendo mostradas é apenas para enteder como deve ser utilizado o pymongo

* **Insert**
```py
data = {
  'nome': 'Jef',
  'idade': 45
}

responseData = collection.insert_one(data)
# responseData é do tipo InsertOneResult, só vi que tem o inserted_id até agora
```
[Infos sobre InsertOneResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.InsertOneResult)

* **Replace**
```py
data = {
  'nome': 'Jef',
  'idade': 45
}

responseData = collection.replace_one({'nome': 'Mateus'}, data)
# responseData é do tipo UpdateResult, só vi que tem matched_count,modified_count e upserted_id de informações relevantes
```
[Infos sobre UpdateResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.UpdateResult)

* **Update**
```py

responseData = collection.update_one({'nome': 'Mateus'}, {'$inc': {'idade': 2}}, upsert)
# responseData é do tipo UpdateResult, só vi que tem matched_count,modified_count e upserted_id de informações relevantes
# incrementa o valor idade em 2
# upsert é um valor booleano, que vai definir se é necessário inserir o objeto ou não
```
[Infos sobre UpdateResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.UpdateResult)
* Outros operadores interessantes:
  * $set: vai definir um valor específico
  * $mul: vai múltiplicar a propriedade pelo valor especificado
  * $rename: vai trocar o campo
  * $setOnInsert: se a query não resultar em nada, e o objeto tiver que ser inserido, adiciona os campos
  * $unset: remove o campo
* Para arrays:
  * $: atualiza o primeiro que encontrar na condição
  * $[]: atualiza todos os elementos encontrados
  * $[\<identifiers\>]: atualiza todos que combinarem com a condição dentro do parênteses

[Infos sobre Update Operators](https://docs.mongodb.com/manual/reference/operator/update/#std-label-update-operators)


* **update_many**
```py
responseData = collection.update_many(
    {'valor': 10}, {'$set': {'teste2':'novo'}})
# procura todo lugar onde valor é igual a 10, e altera/adiciona o campo teste2 = novo
```
[Infos sobre UpdateResult](https://pymongo.readthedocs.io/en/stable/api/pymongo/results.html#pymongo.results.UpdateResult)

