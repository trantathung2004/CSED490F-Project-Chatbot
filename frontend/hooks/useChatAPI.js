import { useState } from 'react'


export default function useChatAPI() {
    const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
    const [isLoading, setIsLoading] = useState(false)
    const [lastResponse, setLastResponse] = useState(null)


    async function sendMessage({ message, model = 'llama3.2', stream = false }) {
        setIsLoading(true)
        try {
            const res = await fetch(`${API}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message, model, stream })
            })
            if (!res.ok) {
                const e = await res.json().catch(() => null)
                setLastResponse(`Error: ${res.status} ${e?.detail || ''}`)
                return null
            }
            const j = await res.json()
            setLastResponse(j.response)
            return j
        } catch (err) {
            setLastResponse(`Network error: ${err.message}`)
            return null
        } finally {
            setIsLoading(false)
        }
    }


    async function getModels() {
        try {
            const res = await fetch(`${API}/api/models`)
            if (!res.ok) return null
            return await res.json()
        } catch (e) { return null }
    }


    async function loadModel(body = { model: 'llama3.2', keep_alive: '5m' }) {
        try {
            const res = await fetch(`${API}/api/models/load`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
            })
            return await res.json()
        } catch (e) { return null }
    }


    async function unloadModel(body = { model: 'llama3.2' }) {
        try {
            const res = await fetch(`${API}/api/models/unload`, {
                method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body)
            })
            return await res.json()
        } catch (e) { return null }
    }


    return { sendMessage, getModels, loadModel, unloadModel, isLoading, lastResponse }
}