import React from 'react';
import { spotifyAuth } from '../api/api';
import '../styles/SpotifyAuth.css';

const SpotifyAuth = () => {
    return (
        <div className="spotify-auth">
            <h2>Spotify Authentication</h2>
            <button onClick={spotifyAuth} className="btn btn-success">
                Sign in to Spotify
            </button>
        </div>
    );
};

export default SpotifyAuth;
