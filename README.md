# discord-key-system

advanced key system bot.

## commands

### generate_key
- args: discord user (ping, required), not_user (can generate a key for yourself and not give it to any user still needs to ping a user, not required)
- will check if you are allowed to generate key
- checks if user already has a key
- returns a random string

### keys and users
- will return a json content of the system table (only owners)

### delete_key
- args: key (required)
- delete a key
