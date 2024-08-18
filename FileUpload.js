import React, { useState } from 'react';
import './FileUpload.css'

function FileUpload() {
    const [file, setFile] = useState(null);

    function handleFile(event) { 
        setFile(event.target.files[0]);
    }

    function handleUpload(event) {
        event.preventDefault(); // Prevents the default form submission behavior

        if (!file) {
            console.error("No file selected.");
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        fetch('url', {
            method: "POST",
            body: formData
        })
        .then((response) => response.json())
        .then((result) => {
            console.log('Success:', result);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    }

    return (
        <div className="upload-container">
            <h2>Video Uploader</h2>
            <form onSubmit={handleUpload}>
                <input type="file" name="file" onChange={handleFile} />
                <button type="submit" disabled={!file}>Upload</button>
            </form>
        </div>
    );
}

export default FileUpload;
