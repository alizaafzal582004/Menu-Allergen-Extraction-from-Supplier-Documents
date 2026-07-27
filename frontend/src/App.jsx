import { useState } from 'react'
import './App.css'

const API_BASE_URL = 'http://127.0.0.1:8000'

function App() {
  const [selectedFile, setSelectedFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadResult, setUploadResult] = useState(null)
  const [error, setError] = useState(null)

  const [processing, setProcessing] = useState(false)
  const [documentDetail, setDocumentDetail] = useState(null)

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0])
    setUploadResult(null)
    setDocumentDetail(null)
    setError(null)
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Select a PDF file before uploading.')
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

  const handleProcess = async () => {
    if (!uploadResult) return

    setProcessing(true)
    setError(null)

    try {
      const response = await fetch(`${API_BASE_URL}/documents/${uploadResult.id}/process`, {
        method: 'POST',
      })

      if (!response.ok) {
        throw new Error(`Processing failed with status ${response.status}`)
      }

      await response.json()

      const detailResponse = await fetch(`${API_BASE_URL}/documents/${uploadResult.id}`)
      const detailData = await detailResponse.json()
      setDocumentDetail(detailData)
    } catch (err) {
      setError(err.message)
    } finally {
      setProcessing(false)
    }
  }

  return (
    <div className="app-shell">
      <header className="app-header">
        <p className="app-eyebrow">Supplier Spec Sheet — Allergen Check</p>
        <h1 className="app-title">Barcelona Bites</h1>
        <p className="app-subtitle">Upload a supplier PDF to extract ingredients and flag allergens.</p>
      </header>

      {error && <div className="error-banner">Error: {error}</div>}

      <section className="ticket">
        <p className="ticket-label">01 — Upload document</p>
        <div className="upload-row">
          <input type="file" accept="application/pdf" onChange={handleFileChange} />
          <button className="btn-primary" onClick={handleUpload} disabled={uploading}>
            {uploading ? 'Uploading…' : 'Upload PDF'}
          </button>
        </div>
      </section>

      {uploadResult && (
        <section className="ticket">
          <p className="ticket-label">02 — Document</p>
          <div className="meta-row">
            <span className="meta-label">ID</span>
            <span className="meta-value">{uploadResult.id}</span>
          </div>
          <div className="meta-row">
            <span className="meta-label">Filename</span>
            <span className="meta-value">{uploadResult.filename}</span>
          </div>
          <div className="meta-row">
            <span className="meta-label">Status</span>
            <span className={`meta-value status-${documentDetail?.status || uploadResult.status}`}>
              {documentDetail?.status || uploadResult.status}
            </span>
          </div>

          <button className="btn-secondary" onClick={handleProcess} disabled={processing}>
            {processing ? 'Processing… (1–3 min)' : 'Process Document'}
          </button>
        </section>
      )}

      {documentDetail && (
        <section className="ticket results-ticket">
          <div className="results-header">
            <p className="results-title">Results</p>
          </div>

          <div className="ingredient-list">
            {documentDetail.ingredients.map((ingredient) => (
              <div className="ingredient-row" key={ingredient.id}>
                <span className="ingredient-name">{ingredient.name}</span>
                {ingredient.allergens.length > 0 && (
                  <span className="allergen-tag">⚠ {ingredient.allergens.join(', ')}</span>
                )}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  )
}

export default App