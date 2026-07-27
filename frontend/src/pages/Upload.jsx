import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { FiUploadCloud, FiFile, FiX, FiLoader } from 'react-icons/fi'
import { uploadDocument, processDocument, listDocuments } from '../services/api'
import '../styles/Upload.css'

const MAX_FILE_SIZE_MB = 10

function Upload() {
  const navigate = useNavigate()
  const fileInputRef = useRef(null)

  const [selectedFile, setSelectedFile] = useState(null)
  const [isDragging, setIsDragging] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [uploadedDoc, setUploadedDoc] = useState(null)
  const [processing, setProcessing] = useState(false)
  const [error, setError] = useState(null)
  const [recentDocs, setRecentDocs] = useState([])

  useEffect(() => {
    loadRecentDocuments()
  }, [])

  const loadRecentDocuments = async () => {
    try {
      const response = await listDocuments()
      setRecentDocs(response.data.slice(-5).reverse())
    } catch (err) {
      // Non-critical — recent documents list is a convenience, not required for upload to work
      console.error('Could not load recent documents:', err)
    }
  }

  const validateAndSetFile = (file) => {
    setError(null)

    if (!file) return

    if (file.type !== 'application/pdf') {
      setError('Only PDF files are supported.')
      return
    }

    const fileSizeMB = file.size / (1024 * 1024)
    if (fileSizeMB > MAX_FILE_SIZE_MB) {
      setError(`File is too large. Maximum size is ${MAX_FILE_SIZE_MB}MB.`)
      return
    }

    setSelectedFile(file)
    setUploadedDoc(null)
  }

  const handleFileInputChange = (event) => {
    validateAndSetFile(event.target.files[0])
  }

  const handleDrop = (event) => {
    event.preventDefault()
    setIsDragging(false)
    validateAndSetFile(event.dataTransfer.files[0])
  }

  const handleDragOver = (event) => {
    event.preventDefault()
    setIsDragging(true)
  }

  const handleDragLeave = () => {
    setIsDragging(false)
  }

  const handleReset = () => {
    setSelectedFile(null)
    setUploadedDoc(null)
    setError(null)
    if (fileInputRef.current) fileInputRef.current.value = ''
  }

  const handleUpload = async () => {
    if (!selectedFile) return

    setUploading(true)
    setError(null)

    try {
      const response = await uploadDocument(selectedFile)
      setUploadedDoc(response.data)
      loadRecentDocuments()
    } catch (err) {
      setError('Upload failed. Please check your connection and try again.')
    } finally {
      setUploading(false)
    }
  }

  const handleExtract = async () => {
    if (!uploadedDoc) return

    setProcessing(true)
    setError(null)

    try {
      await processDocument(uploadedDoc.id)
      navigate(`/results/${uploadedDoc.id}`)
    } catch (err) {
      setError('Extraction failed. This can happen if the AI service is temporarily busy — please try again.')
      setProcessing(false)
    }
  }

  return (
    <div className="upload-page">
      <div className="upload-container">
        <h1 className="upload-title">Upload a supplier document</h1>
        <p className="upload-subtitle">
          Drop a PDF below or browse your files. Supported: PDF only, up to {MAX_FILE_SIZE_MB}MB.
        </p>

        {error && <div className="upload-error">{error}</div>}

        {!uploadedDoc && (
          <div
            className={`dropzone ${isDragging ? 'dropzone-active' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => fileInputRef.current.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept="application/pdf"
              onChange={handleFileInputChange}
              hidden
            />
            <FiUploadCloud className="dropzone-icon" />
            <p className="dropzone-text">
              {selectedFile ? selectedFile.name : 'Drag & drop your PDF here, or click to browse'}
            </p>
          </div>
        )}

        {selectedFile && !uploadedDoc && (
          <div className="file-card">
            <FiFile className="file-card-icon" />
            <div className="file-card-info">
              <span className="file-card-name">{selectedFile.name}</span>
              <span className="file-card-size">{(selectedFile.size / 1024).toFixed(0)} KB</span>
            </div>
            <button className="file-card-remove" onClick={handleReset} aria-label="Remove file">
              <FiX />
            </button>
          </div>
        )}

        {selectedFile && !uploadedDoc && (
          <div className="upload-actions">
            <button className="btn btn-ghost" onClick={handleReset} disabled={uploading}>
              Reset
            </button>
            <button className="btn btn-primary" onClick={handleUpload} disabled={uploading}>
              {uploading ? (<><FiLoader className="spin" /> Uploading…</>) : 'Upload'}
            </button>
          </div>
        )}

        {uploadedDoc && (
          <div className="uploaded-card">
            <FiFile className="file-card-icon" />
            <div className="file-card-info">
              <span className="file-card-name">{uploadedDoc.filename}</span>
              <span className="status-badge status-uploaded">{uploadedDoc.status}</span>
            </div>
          </div>
        )}

        {uploadedDoc && (
          <div className="upload-actions">
            <button className="btn btn-ghost" onClick={handleReset} disabled={processing}>
              Upload Another
            </button>
            <button className="btn btn-primary" onClick={handleExtract} disabled={processing}>
              {processing ? (<><FiLoader className="spin" /> Extracting… (1–3 min)</>) : 'Extract Allergens'}
            </button>
          </div>
        )}

        {recentDocs.length > 0 && (
          <div className="recent-docs">
            <h2 className="recent-docs-title">Recent uploads</h2>
            <div className="recent-docs-list">
              {recentDocs.map((doc) => (
                <div
                  key={doc.id}
                  className="recent-doc-item"
                  onClick={() => navigate(`/results/${doc.id}`)}
                >
                  <FiFile />
                  <span className="recent-doc-name">{doc.filename}</span>
                  <span className={`status-badge status-${doc.status}`}>{doc.status}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default Upload