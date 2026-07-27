import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Results from './pages/Results'
import './styles/App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/upload" element={<Upload />} />
        <Route path="/results/:documentId" element={<Results />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App