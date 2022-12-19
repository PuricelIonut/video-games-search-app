# World of Games
## Video Demo:  https://www.youtube.com/watch?v=NqtevBrDYuo
## Description:
Web app for searching games and managing progress made using Python, Flask, SQL, Bootstrap, HTML and CSS.
Made by one person.All the data used by the app is provided by https://rawg.io and is received via GET requests, note that each request must contain the API key.

Register: A basic username/password/check-password implementation of register system.It will not let user register and prompt alerts if all fields are not filled or without providing valid data as unique username and matching passwords.Once the user provided valid data they will be redirected to login page.All the data from a valid registration is stored inside a database.

Login: Username/password login system.On submit the app checks the database for existing credentials.It will not work and prompt user alerts if all fields are not filled or username and password do not exist.

Logout: The user can close the current session and log out of their account.After loging out the user is unable to use search and my collection.

Change password: The user can change passwords either loged in or loged out.When password is changed the user will have to log in again.On valid input the old password is changed with the new one.All fields are required and providing invalid credentials will prompt de user pointing their mistake.

Search game: The user can provide the name of a game(it does not have to be exactly the title of that game eg. "The witcher 3" will generate results for "The Witcher 3: Wild Hunt") and the app will display a page with details about the game such as: game title, release date, playtime, game description, genre, platforms, screenshots, links to stores and game website.If the input provided does not match a game(existing in https://rawg.io database) they will be prompted about invalid game name.

My collection: The user can add games to collection by clicking a button on any game they searched for.If game is already in my collection the user won't be able to add it again.On My collection tab the user can check all the games added and the progress of each.The user can either delete a game or change it's progress.The user can provide anything as input for progress.If My collection is empty the user will be noticed.My collection is unique for each user.

## Limitations
Video of each game: I really wanted to implement this feature but i simply could not find the video link inside json files.

Search suggestions: I wanted to implement this feature but did not find a way to get only the name of all available games from RAWG.io.

Search game from My collection: Could not find a way to be able to just click any game from my collection and be redirected to their page.

## Important
The app will not work without providing API key.Get yours freely from https://rawg.io/apidocs and use the command export API_KEY=KEY HERE in terminal.