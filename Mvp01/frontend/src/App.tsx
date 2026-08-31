import { useState } from 'react'
import './App.css'

type Status = "idle" | "selected" | "loading" | "error" | "success"

const API_URL = "https://data-quality-platform-a7xn.onrender.com"

function App() {
  const [status, setStatus] = useState<Status>("idle")
  const [file, setFile] = useState<File | null>(null)
  const [report, setReport] = useState<any>(null)
  const [errorMessage, setErrorMessage] = useState<string | null>(null)

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
    setStatus("idle")
  }

  return (
    <div className="container">
      <h1>Data Quality Platform</h1>

      {(status === "idle" || status === "selected") && (
        <div className="upload-box">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={status === "loading"}
          />
          <button
            onClick={handleAnalyze}
            disabled={status !== "selected"}
          >
            Analizar
          </button>
        </div>
      )}

      {status === "loading" && (
        <p>Analizando tu dataset... (puede tardar hasta un minuto si el servidor estaba dormido)</p>
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
          <pre>{JSON.stringify(report, null, 2)}</pre>
          <button onClick={handleReset}>Analizar otro archivo</button>
        </div>
      )}
    </div>
  )
}

export default App