# How to run
```
git clone https://github.com/Adjuntor/shiva.git
cd shiva
pip install --no-cache-dir -r requirements.txt
```
Edit with the correct values and rename the config file to "config.py". You can delete the cog folders you don't need.
Run the bot.
```
python3 main.py
```

# Docker Image
Requires docker to be installed.
```
git clone https://github.com/Adjuntor/shiva.git
cd shiva
```
Edit with the correct values and rename the config file to "config.py". You can delete the cog folders you don't need.
```
docker build -t shiva .
docker run -d --name=shiva --restart=always shiva
```

# Docker Compose
Requires docker and docker compose to be installed.
```
git clone https://github.com/Adjuntor/shiva.git
cd shiva
```
Edit with the correct values and rename the config file to "config.py". You can delete the cog folders you don't need.
```
docker-compose up -d
```

# Delete Docker Container
```
docker stop shiva
docker rm shiva
```

# Updating
To update the bot use the command below to ignore updating the config.py, keeping your local version.
```
git update-index --skip-worktree config.py
```
and just do an update.
```
git pull
```
