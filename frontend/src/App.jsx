import React from 'react';
import AlbumFetcher from './components/AlbumFetcher';
import SpotifyAuth from './components/SpotifyAuth';
import PlaylistImport from './components/PlaylistImport';

const App = () => {
    return (
        <div className="App">
            <h1>ApplyToSpotify</h1>
            <SpotifyAuth />
            <AlbumFetcher />
            <PlaylistImport />
        </div>
    );
};

export default App;
