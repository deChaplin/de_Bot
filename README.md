# de_Bot
A combination of my bots. Made to be used in private discord server.

## Commands

### Help Commands
- "help main" - "Shows the main help commands"
- "help vac" - "Displays commands for the VAC Checker"
- "help search" - "Displays commands for the search tools"

### Vac Checker
Uses the steam api to check if a user is VAC banned. You can manually add steam accounts to the database and check their status. Once added any you will get a pm every hour for any account banned.

## Vac Checker Commands

- "vac status <steamID>" - "Check the status of a specific account"
- "vac add <steamID>" - "Add a steam account to the database"
- "vac remove <steamID>" - "Remove a steam account from the database"
  
![image](https://github.com/deChaplin/VAC-Checker/assets/85872356/bdcde8f5-397d-4ee3-88ff-c848328f6d95)

### Search Features
Uses verious APIs.

## Search commands
- "image <prompt>" - "Gets an image" (You will need an API key from  - https://console.cloud.google.com/ and a search engine ID from - https://cse.google.com/cse/all)
- "wiki <prompt>" - "Searches using the Wikipedia search engine"
- "define <prompt>" - "Gets the definition of a word"
- "arrr <game>" - "Searches using the Rezi.one search engine"
- "checkPrefix" - "Shows current prefix for the server"
- "help" - "Shows this help menu"

### Todo
    1. Add a command to check the status of all your accounts in the database
    2. Subscribe option for private message updates
    3. Remove accounts when confirmed banned
    4. Generate AI images command
    5. Search using a search engine

  
## .env file format
  
TOKEN=discord bot token

STEAM_API_KEY=steam API key

GOOGLE_API_KEY=Google API key

SEARCH_ENGINE_ID=Custom search engine ID

REZI_API_KEY=rezi search engine API key
