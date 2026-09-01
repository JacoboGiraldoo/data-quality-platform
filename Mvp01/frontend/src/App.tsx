import { useState } from 'react'
import './App.css'

type Status = "idle" | "selected" | "loading" | "error" | "success"
type PdfStatus = "idle" | "downloading" | "error"

const API_URL = "https://data-quality-platform-a7xn.onrender.com"

const SEVERITY_COLORS: Record<string, string> = {
  yellow: "#FFC107",
  red: "#F44336",
}

function App() {
  const [status, setStatus] = useState<Status>("idle")
  const [file, setFile] = useState<File | null>(null)
  const [report, setReport] = useState<any>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

  const [pdfStatus, setPdfStatus] = useState<PdfStatus>("idle")
  const [pdfErrorMessage, setPdfErrorMessage] = useState<string | null>(null)

  function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const selectedFile = event.target.files?.[0]
    if (selectedFile) {
      setFile(selectedFile)
      setStatus("selected")
    }
  }

  async function handleAnalyze() {
    if (!file) return

    setStatus("loading")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      })

      const data = await response.json()

      if (!response.ok) {
        setErrorMessage(translateError(response.status))
        setStatus("error")
        return
      }

      setReport(data)
      setStatus("success")

    } catch (err) {
      setErrorMessage("No se pudo conectar con el servidor. Verifica tu conexión.")
      setStatus("error")
    }
  }

  async function handleDownloadPdf() {
    if (!file) return

    setPdfStatus("downloading")

    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch(`${API_URL}/analyze/pdf`, {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        setPdfErrorMessage("No se pudo generar el PDF. Intenta de nuevo.")
        setPdfStatus("error")
        return
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const link = document.createElement("a")
      link.href = url
      link.download = "report.pdf"
      link.click()
      URL.revokeObjectURL(url)

      setPdfStatus("idle")

    } catch (err) {
      setPdfErrorMessage("No se pudo conectar con el servidor.")
      setPdfStatus("error")
    }
  }

  function translateError(statusCode: number): string {
    if (statusCode === 422) return "El archivo no es un CSV válido."
    if (statusCode === 413) return "El archivo es demasiado grande (máximo 10MB)."
    if (statusCode === 400) return "El archivo está vacío."
    return "Ocurrió un error inesperado."
  }

  function handleReset() {
    setFile(null)
    setReport(null)
    setErrorMessage(null)
    setPdfStatus("idle")
    setPdfErrorMessage(null)
    setStatus("idle")
  }

  return (
  <div className="container">
    <h1>Data Quality Platform</h1>
    <p className="subtitle">Sube un CSV y recibe un reporte de calidad con recomendaciones accionables.</p>

    <div className="ticket">
      {(status === "idle" || status === "selected") && (
        <div className="upload-box">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={status === "loading"}
          />
          <button
            className="btn-primary"
            onClick={handleAnalyze}
            disabled={status !== "selected"}
          >
            Analizar
          </button>
        </div>
      )}

      {status === "loading" && (
        <p className="loading-message">Analizando tu dataset... (puede tardar hasta un minuto si el servidor estaba dormido)</p>
      )}

      {status === "error" && (
        <div>
          <p className="error">{errorMessage}</p>
          <input type="file" accept=".csv" onChange={handleFileChange} />
        </div>
      )}

      {status === "success" && report && (
        <div>
          <h2>Resultado del análisis</h2>

          {report.recommendations.length === 0 ? (
            <p className="no-issues">No se encontraron problemas en tu dataset.</p>
          ) : (
            <ul className="recommendations-list">
              {report.recommendations.map((rec: any, index: number) => (
                <li key={index} className="recommendation-item">
                  <span
                    className="severity-dot"
                    style={{ backgroundColor: SEVERITY_COLORS[rec.severity] }}
                  />
                  <span>
                    {rec.column && <span className="column-tag">{rec.column}</span>} {rec.message}
                  </span>
                </li>
              ))}
            </ul>
          )}

          <div className="actions">
            <button className="btn-primary" onClick={handleDownloadPdf} disabled={pdfStatus === "downloading"}>
              {pdfStatus === "downloading" ? "Generando PDF..." : "Descargar PDF"}
            </button>
            <button className="btn-secondary" onClick={handleReset}>Analizar otro archivo</button>
          </div>
          {pdfStatus === "error" && <p className="error">{pdfErrorMessage}</p>}
        </div>
      )}
    </div>
  </div>
)
}

export default App