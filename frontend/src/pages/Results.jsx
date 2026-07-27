import { useState, useEffect, useMemo } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import {
  FiAlertTriangle,
  FiSearch,
  FiDownload,
  FiArrowLeft,
  FiLoader,
} from 'react-icons/fi'
import { getDocument } from '../services/api'
import '../styles/Results.css'

function Results() {
  const { documentId } = useParams()
  const navigate = useNavigate()

  const [document, setDocument] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchTerm, setSearchTerm] = useState('')
  const [filter, setFilter] = useState('all') // 'all' | 'allergens' | 'safe'

  useEffect(() => {
    loadDocument()
  }, [documentId])

  const loadDocument = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await getDocument(documentId)
      setDocument(response.data)
    } catch (err) {
      setError('Could not load this document. It may not exist.')
    } finally {
      setLoading(false)
    }
  }

  const filteredIngredients = useMemo(() => {
    if (!document) return []

    return document.ingredients.filter((ingredient) => {
      const matchesSearch = ingredient.name.toLowerCase().includes(searchTerm.toLowerCase())
      const hasAllergens = ingredient.allergens.length > 0

      if (filter === 'allergens' && !hasAllergens) return false
      if (filter === 'safe' && hasAllergens) return false

      return matchesSearch
    })
  }, [document, searchTerm, filter])

  const allDetectedAllergens = useMemo(() => {
    if (!document) return []
    const set = new Set()
    document.ingredients.forEach((ing) => ing.allergens.forEach((a) => set.add(a)))
    return Array.from(set)
  }, [document])

  const handleExportJSON = () => {
    const blob = new Blob([JSON.stringify(document, null, 2)], { type: 'application/json' })
    downloadBlob(blob, `${document.filename.replace('.pdf', '')}_allergens.json`)
  }

  const handleExportCSV = () => {
    const rows = [['Ingredient', 'Allergens']]
    document.ingredients.forEach((ing) => {
      rows.push([ing.name, ing.allergens.join('; ')])
    })
    const csvContent = rows.map((row) => row.map((cell) => `"${cell}"`).join(',')).join('\n')
    const blob = new Blob([csvContent], { type: 'text/csv' })
    downloadBlob(blob, `${document.filename.replace('.pdf', '')}_allergens.csv`)
  }

  const downloadBlob = (blob, filename) => {
    const url = URL.createObjectURL(blob)
    const link = window.document.createElement('a')
    link.href = url
    link.download = filename
    link.click()
    URL.revokeObjectURL(url)
  }

  if (loading) {
    return (
      <div className="results-page results-centered">
        <FiLoader className="spin results-loading-icon" />
        <p>Loading results…</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="results-page results-centered">
        <p className="results-error">{error}</p>
        <Link to="/upload" className="btn btn-primary">Upload a document</Link>
      </div>
    )
  }

  return (
    <div className="results-page">
      <div className="results-container">
        <button className="back-link" onClick={() => navigate('/upload')}>
          <FiArrowLeft /> Upload another PDF
        </button>

        <div className="results-header">
          <div>
            <h1 className="results-title">{document.filename}</h1>
            <span className={`status-badge status-${document.status}`}>{document.status}</span>
          </div>
          <div className="export-actions">
            <button className="btn btn-ghost btn-sm" onClick={handleExportCSV}>
              <FiDownload /> CSV
            </button>
            <button className="btn btn-ghost btn-sm" onClick={handleExportJSON}>
              <FiDownload /> JSON
            </button>
          </div>
        </div>

        {allDetectedAllergens.length > 0 && (
          <div className="allergen-summary">
            <FiAlertTriangle className="allergen-summary-icon" />
            <div>
              <strong>{allDetectedAllergens.length} allergen{allDetectedAllergens.length > 1 ? 's' : ''} detected:</strong>{' '}
              {allDetectedAllergens.join(', ')}
            </div>
          </div>
        )}

        <div className="results-toolbar">
          <div className="search-box">
            <FiSearch />
            <input
              type="text"
              placeholder="Search ingredients…"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="filter-tabs">
            <button
              className={filter === 'all' ? 'filter-tab active' : 'filter-tab'}
              onClick={() => setFilter('all')}
            >
              All ({document.ingredients.length})
            </button>
            <button
              className={filter === 'allergens' ? 'filter-tab active' : 'filter-tab'}
              onClick={() => setFilter('allergens')}
            >
              With Allergens
            </button>
            <button
              className={filter === 'safe' ? 'filter-tab active' : 'filter-tab'}
              onClick={() => setFilter('safe')}
            >
              Safe
            </button>
          </div>
        </div>

        <div className="results-table">
          <div className="results-table-header">
            <span>Ingredient</span>
            <span>Allergens</span>
          </div>
          {filteredIngredients.length === 0 && (
            <p className="results-empty">No ingredients match your search or filter.</p>
          )}
          {filteredIngredients.map((ingredient) => (
            <div className="results-table-row" key={ingredient.id}>
              <span className="ingredient-cell">{ingredient.name}</span>
              <span className="allergen-cell">
                {ingredient.allergens.length > 0 ? (
                  ingredient.allergens.map((allergen) => (
                    <span className="allergen-pill" key={allergen}>
                      <FiAlertTriangle /> {allergen}
                    </span>
                  ))
                ) : (
                  <span className="safe-label">No allergens detected</span>
                )}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Results