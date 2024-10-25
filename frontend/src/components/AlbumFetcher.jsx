import React, { useState } from 'react';
import { fetchAppleMusicAlbum } from '../api/api';
import '../styles/AlbumFetcher.css';

const AlbumFetcher = () => {
    const [albumId, setAlbumId] = useState('');
    const [albumData, setAlbumData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleFetchAlbum = async () => {
        setLoading(true);
        setError('');
        try {
            const data = await fetchAppleMusicAlbum(albumId);
            setAlbumData(data);
        } catch (error) {
            setError('Failed to fetch album');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="album-fetcher">
            <h2>Fetch Apple Music Album</h2>
            <input
                type="text"
                placeholder="Enter Album ID"
                value={albumId}
                onChange={(e) => setAlbumId(e.target.value)}
                className="form-control"
            />
            <button onClick={handleFetchAlbum} className="btn btn-primary mt-2">
                {loading ? 'Loading...' : 'Fetch Album'}
            </button>
            {error && <div className="alert alert-danger mt-2">{error}</div>}
            {albumData && (
                <div className="mt-4">
                    <h3>{albumData.name}</h3>
                    <ul className="list-group">
                        {albumData.tracks.map((track) => (
                            <li key={track.id} className="list-group-item">
                                {track.name}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default AlbumFetcher;
