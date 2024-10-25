import React, { useState } from 'react';
import { getPlaylists, importSongsToSpotify } from '../api/api';
import '../styles/PlaylistImport.css';

const PlaylistImport = () => {
    const [playlists, setPlaylists] = useState([]);
    const [selectedSongs, setSelectedSongs] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleGetPlaylists = async () => {
        setLoading(true);
        setError('');
        try {
            const data = await getPlaylists();
            setPlaylists(data);
        } catch (error) {
            setError('Failed to fetch playlists');
        } finally {
            setLoading(false);
        }
    };

    const handleImportSongs = async () => {
        if (selectedSongs.length === 0) {
            alert('Please select songs to import.');
            return;
        }
        if (window.confirm('Are you sure you want to import the selected songs?')) {
            setLoading(true);
            setError('');
            try {
                await importSongsToSpotify(selectedSongs);
                alert('Songs imported successfully!');
            } catch (error) {
                setError('Failed to import songs');
            } finally {
                setLoading(false);
            }
        }
    };

    return (
        <div className="playlist-import">
            <h2>Import Songs to Spotify</h2>
            <button onClick={handleGetPlaylists} className="btn btn-primary">
                {loading ? 'Loading...' : 'Get Playlists'}
            </button>
            {error && <div className="alert alert-danger mt-2">{error}</div>}
            <ul className="list-group mt-2">
                {playlists.map((playlist) => (
                    <li key={playlist.id} className="list-group-item">
                        <label>
                            <input
                                type="checkbox"
                                value={playlist.songs}
                                onChange={(e) => {
                                    const songs = Array.from(e.target.selectedOptions, option => option.value);
                                    setSelectedSongs(songs);
                                }}
                            />
                            {playlist.name}
                        </label>
                    </li>
                ))}
            </ul>
            <button onClick={handleImportSongs} className="btn btn-success mt-2">
                Import Selected Songs
            </button>
        </div>
    );
};

export default PlaylistImport;
