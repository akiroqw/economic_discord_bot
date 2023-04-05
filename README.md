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

The bot system is implemented using 2 types, experience and levels, experience is accrued weekly, or for chatting. The bot also has a system of economy, shop, jackets, salaries and profiles

### Bot events
* bot.bot_ready_event() // Event triggered when the bot starts.
* bot.member_join_event() // Event triggered when a new user joins the server.
* bot.commands_error_event() // Event triggered when an error occurs in a command.
* bot.on_message_event() // Event triggered when a message is received on the server.

#### Various configs

To specify which roles will be served when using the `bot.collect_event(collecting_roles, 0, 0):` method, you need to specify the name of the role here, and the amount how much users will receive from this role.

```py
collecting_roles = {"Administrator" : 250000,
                    "Moderator" : 12323,
                    "G. Administrator": 123
}
```
To specify which words will be output when displaying the work message when we use the command `not.work_event(70000, 100000, text_work, 0, 0):`, we need to replace the following elements:

```py
text_work = {1: 'None', //1st option, other...
             2: 'None2', 
             3: 'None3'}
}

```

Description of the methods themselves: 
`bot.collect_event(collecting_roles, 0, 0):` - 1 argument takes the mapping, 2 and 3 are the time interval
`not.work_event(70000, 100000, text_work, 0, 0):`- 1 and 2 arguments take int values, this is the range of random salary for work. 3 argument accepts mappings for phrases, 4-5 time range


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

