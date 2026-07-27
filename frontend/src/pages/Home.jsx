import { Link } from 'react-router-dom'
import logo from '../assets/logo.png'
import {
  FiUploadCloud,
  FiCheckCircle,
  FiShield,
  FiGlobe,
  FiClock,
  FiFileText,
} from 'react-icons/fi'
import '../styles/Home.css'

function Home() {
  return (
    <div className="home-page">
      {/* Navbar */}
      <nav className="navbar">
        <div className="navbar-inner">
          <Link to="/" className="navbar-brand">
            <img src={logo} alt="Barcelona Bites Gastro Club" className="navbar-logo-img" />
            <span className="navbar-logo-text">Barcelona Bites</span>
          </Link>
          <div className="navbar-links">
            <a href="#features">Features</a>
            <a href="#how-it-works">How It Works</a>
            <Link to="/upload" className="btn btn-primary btn-sm">Upload PDF</Link>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="hero">
        <div className="hero-content">
          <span className="hero-eyebrow">AI-Powered Allergen Detection</span>
          <h1 className="hero-title">
            Stop copying allergens by hand from supplier PDFs.
          </h1>
          <p className="hero-subtitle">
            Upload a supplier specification sheet and let AI extract ingredients
            and flag allergens automatically — reviewed by your team before it
            ever reaches a menu.
          </p>
          <div className="hero-actions">
            <Link to="/upload" className="btn btn-primary">
              <FiUploadCloud /> Upload PDF
            </Link>
            <Link to="/upload" className="btn btn-secondary">
              Try Demo
            </Link>
            <a href="#how-it-works" className="btn btn-ghost">
              Learn More
            </a>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features" id="features">
        <h2 className="section-title">Built for restaurant kitchens</h2>
        <div className="features-grid">
          <div className="feature-card">
            <FiFileText className="feature-icon" />
            <h3>Any supplier format</h3>
            <p>Tables, matrices, prose, footnotes — the extraction pipeline handles varied document layouts.</p>
          </div>
          <div className="feature-card">
            <FiGlobe className="feature-icon" />
            <h3>Multilingual</h3>
            <p>Reads Spanish, Catalan, and English supplier documents, including bilingual pages.</p>
          </div>
          <div className="feature-card">
            <FiShield className="feature-icon" />
            <h3>Human-reviewed</h3>
            <p>Every extraction is designed to be checked by a person before it reaches your menu system.</p>
          </div>
          <div className="feature-card">
            <FiClock className="feature-icon" />
            <h3>Minutes, not hours</h3>
            <p>Replace manual copy-paste from spec sheets with an automated first pass.</p>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="how-it-works" id="how-it-works">
        <h2 className="section-title">How it works</h2>
        <div className="steps-grid">
          <div className="step-card">
            <span className="step-number">1</span>
            <h3>Upload the PDF</h3>
            <p>Drag and drop a supplier specification sheet, or browse to select one.</p>
          </div>
          <div className="step-card">
            <span className="step-number">2</span>
            <h3>AI extracts the data</h3>
            <p>Ingredients are parsed and matched against the 14 EU Annex II allergens.</p>
          </div>
          <div className="step-card">
            <span className="step-number">3</span>
            <h3>Review the results</h3>
            <p>Check the flagged allergens, confirm accuracy, and export for your menu system.</p>
          </div>
        </div>
      </section>

      {/* AI Benefits */}
      <section className="benefits">
        <div className="benefits-content">
          <h2 className="section-title">Why it matters</h2>
          <ul className="benefits-list">
            <li><FiCheckCircle /> Reduces the risk of a missed allergen reaching a customer</li>
            <li><FiCheckCircle /> Cuts manual data-entry time for kitchen staff</li>
            <li><FiCheckCircle /> Creates a consistent, reviewable record for every supplier document</li>
          </ul>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <p>Barcelona Bites — Allergen Extraction MVP</p>
      </footer>
    </div>
  )
}

export default Home