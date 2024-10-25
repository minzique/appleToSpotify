const API_BASE_URL = "http://localhost:5000"; // Adjust according to your Flask backend

export const fetchAppleMusicAlbum = async (albumId) => {
  const response = await fetch(
    `${API_BASE_URL}/fetch-apple-music-album/${albumId}`
  );
  if (!response.ok) {
    throw new Error("Failed to fetch album");
  }
  return await response.json();
};

export const spotifyAuth = async () => {
  window.location.href = `${API_BASE_URL}/spotify-auth`;
};

export const getPlaylists = async () => {
  const response = await fetch(`${API_BASE_URL}/get-playlists`);
  if (!response.ok) {
    throw new Error("Failed to fetch playlists");
  }
  return await response.json();
};

export const importSongsToSpotify = async (songs) => {
  const response = await fetch(`${API_BASE_URL}/import-songs`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(songs),
  });
  if (!response.ok) {
    throw new Error("Failed to import songs");
  }
  return await response.json();
};
