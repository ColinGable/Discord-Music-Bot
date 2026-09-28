# Discord Music Bot

A Python Discord bot that joins voice channels, searches for music, streams audio, and manages a song queue using Discord.py, yt-dlp, and FFmpeg.

I built this project to learn more about asynchronous Python programming, APIs, audio streaming, and event-driven applications.

## Features

- Joins and leaves Discord voice channels
- Searches for songs using a title or search query
- Streams audio into Discord voice channels
- Maintains a song queue
- Automatically plays the next song in the queue
- Allows users to skip songs
- Displays the current queue
- Handles connection and playback errors

## Commands

| Command | Description |
| --- | --- |
| `!join` | Connects the bot to your current voice channel |
| `!leave` | Disconnects the bot from the voice channel |
| `!play <song>` | Searches for a song and adds it to the queue |
| `!skip` | Skips the currently playing song |
| `!queue` | Displays the songs currently waiting in the queue |
| `!stop` | Stops the currently playing audio |

## Screenshot

<img width="1044" height="805" alt="Music bot Img" src="https://github.com/user-attachments/assets/59e9c781-9d9e-4a4e-bf24-d0f8edb3466d" />


## Technologies

- Python
- Discord.py
- yt-dlp
- FFmpeg
- asyncio
- Python collections

## How It Works

When a user enters a command such as:

```text
!play Metallica Enter Sandman
```

the bot sends the search query to yt-dlp, retrieves the audio stream information, and adds the song to a queue.

The bot then uses FFmpeg and Discord's voice functionality to stream the audio into the user's voice channel.

When a song finishes, the bot automatically removes the next song from the queue and begins playing it.

## Installation

Clone the repository:

```bash
git clone https://github.com/ColinGable/Discord-Music-Bot.git
```

Move into the project directory:

```bash
cd Discord-Music-Bot
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

FFmpeg must also be installed on the computer running the bot.

## Discord Bot Setup

This project requires a Discord bot application and bot token.

For security, the bot token should **not** be stored directly in the source code or committed to GitHub.

The token should instead be stored in an environment variable or `.env` file.

Example:

```text
DISCORD_TOKEN=your_token_here
```

The `.env` file is excluded from Git through `.gitignore`.

## What I Learned

This project gave me experience with:

- Asynchronous programming with Python
- Event-driven application development
- Working with the Discord API
- Managing queues with Python's `deque`
- Streaming audio with FFmpeg
- Searching and retrieving media with yt-dlp
- Handling errors in external services
- Managing Discord voice connections
- Using Git and GitHub for version control

## Future Improvements

- Improve the `stop` command so it can completely clear and end the queue
- Add pause and resume commands
- Add a command to remove specific songs from the queue
- Move FFmpeg configuration out of the source code
- Improve command error handling
