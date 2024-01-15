import React, { useState } from 'react';
import Modal from 'react-modal';
import VideoPlayer from './VideoPlayer';

const customModalStyles = {
    content: {
        top: '50%',
        left: '50%',
        right: 'auto',
        bottom: 'auto',
        marginRight: '-50%',
        transform: 'translate(-50%, -50%)',
        backgroundColor: 'white',
        padding: '20px',
        borderRadius: '8px',
        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    },
};

const MainComponent = () => {
    const [file, setFile] = useState(null);
    const [youtubeLink, setYoutubeLink] = useState('');
    const [modalIsOpen, setModalIsOpen] = useState(false);
    const [errorMessage, setErrorMessage] = useState('');
    const [videoFile, setVideoFile] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleFileChange = (event) => {
        setFile(event.target.files[0]);
    };

    const handleYouTubeLinkChange = (event) => {
        setYoutubeLink(event.target.value);
    };

    const handleUpload = async () => {
        try {
            setLoading(true);
            let response = null

            if (file) {
                const formData = new FormData();
                formData.append('file', file);

                response = await fetch(process.env.REACT_APP_FILE_UPLOAD_ENDPOINT, {
                    method: 'POST',
                    body: formData,
                });
            } else if (youtubeLink) {
                response = await fetch(process.env.REACT_APP_YOUTUBE_ENDPOINT + '?yt_url=' + youtubeLink, {
                    method: 'POST'
                });
            }

            if (response.ok) {
                const blob = await response.blob();
                setVideoFile(blob);
            } else {
                const error_msg = JSON.parse(JSON.stringify(await response.json())).detail;
                console.error('Error:', error_msg);
                setErrorMessage(error_msg);
                setModalIsOpen(true);
            }
            setLoading(false);
        } catch (error) {
            console.error('Error:', error);
            setErrorMessage('Failed to upload video. Please try again.');
            setModalIsOpen(true);
            setLoading(false);
        }
    };

    const closeModal = () => {
        setModalIsOpen(false);
    };

    const handleBack = () => {
        setVideoFile(null);
        setFile(null);
        setYoutubeLink(null);
    };

    return (
        <>
            {loading && (
                <div className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-lg font-semibold text-white bg-gray-800 p-4 rounded-md">
                    Loading...
                </div>
            )}

            {videoFile ? (
                <div className="mx-auto w-3/4 xl:w-1/2">
                    <button
                        onClick={handleBack}
                        className="bg-red-500 text-white p-2 rounded-md cursor-pointer hover:bg-red-600 my-4"
                    >
                        Back
                    </button>
                    <VideoPlayer zipFile={videoFile} />
                </div>
            ) : (
                <div className="max-w-md mx-auto p-6 bg-white shadow-md rounded-md">
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700">Choose a File</label>
                        <input type="file" onChange={handleFileChange} className="mt-1 p-2 border rounded-md w-full" />
                    </div>
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700">YouTube Link</label>
                        <input
                            type="text"
                            placeholder="Enter YouTube link"
                            value={youtubeLink}
                            onChange={handleYouTubeLinkChange}
                            className="mt-1 p-2 border rounded-md w-full"
                        />
                    </div>
                    <button
                        onClick={handleUpload}
                        className="bg-blue-500 text-white p-3 rounded-md cursor-pointer hover:bg-blue-600"
                    >
                        Upload
                    </button>

                    <Modal
                        isOpen={modalIsOpen}
                        onRequestClose={closeModal}
                        style={customModalStyles}
                        contentLabel="Error Modal"
                    >
                        <h2 className="text-xl font-bold mb-2">Error</h2>
                        <p>{errorMessage}</p>
                        <button
                            onClick={closeModal}
                            className="mt-4 bg-blue-500 text-white p-2 rounded-md cursor-pointer hover:bg-blue-600"
                        >
                            Close
                        </button>
                    </Modal>
                </div>
            )}
        </>
    );
};

export default MainComponent;
