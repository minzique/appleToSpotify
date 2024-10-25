# ApplyToSpotify 🎶

<p align="center">
  <img src="https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg" alt="Spotify Logo" />
</p>

**ApplyToSpotify** alows you to sync Apple Music playlists to Spotify, without needing an Apple Music account (for public playlists). Currently only supports public playlists from Apple Music. WIP.

## Installation

You can follow these steps to setup a local development environment:

1. **Clone the repo:**
   ```bash
   git clone https://github.com/yourusername/ApplyToSpotify.git
   cd ApplyToSpotify/frontend
   ```

2. **Install dependencies and start the server:**
   ```bash
   pnpm install && pnpm start
   ```

3. **Visit:**
   ```
   http://localhost:3000

## Usage

1. Fetch an album from Apple Music by entering the album name or ID.
2. Sign in to your Spotify account.
3. Choose the tracks you want from the Apple Music album.
4. Click the import button, and you’re good to go!

# TODO

- [x] Fetch songs from Apple Music API
- [x] Implement Spotify token retrieval with callback
- [x] Save Spotify tokens for sessions
- [x] Move API logic to handle new playlists

- [] Display fetched songs and playlist details
- [] Add song selection from playlist
- [] Implement playlist creation endpoint

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Spotify API](https://developer.spotify.com/documentation/web-api/)
- [Apple Music API](https://developer.apple.com/documentation/applemusicapi)
