import { useState } from 'react'
import './App.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState(null)

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0])
    setUploadResult(null)
    setError(null)
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file first.')
      return
    }

    setUploading(true)
    setError(null)

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      const response = await fetch(`${API_BASE_URL}/documents/upload`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        throw new Error(`Upload failed with status ${response.status}`)
      }

      const data = await response.json()
      setUploadResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div style={{ maxWidth: '600px', margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>Barcelona Bites - Allergen Extraction</h1>

      <div style={{ marginTop: '20px' }}>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={uploading} style={{ marginLeft: '10px' }}>
          {uploading ? 'Uploading...' : 'Upload PDF'}
        </button>
      </div>

      {error && (
        <p style={{ color: 'red', marginTop: '10px' }}>Error: {error}</p>
      )}

      {uploadResult && (
        <div style={{ marginTop: '20px', padding: '15px', border: '1px solid #ccc', borderRadius: '8px' }}>
          <p><strong>Document ID:</strong> {uploadResult.id}</p>
          <p><strong>Filename:</strong> {uploadResult.filename}</p>
          <p><strong>Status:</strong> {uploadResult.status}</p>
        </div>
      )}
    </div>
  )
}

export default App