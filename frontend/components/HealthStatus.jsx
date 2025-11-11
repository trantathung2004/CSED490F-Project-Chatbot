import React, { useEffect, useState } from 'react'


export default function HealthStatus() {
    const [status, setStatus] = useState(null)
    const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'


    async function check() {
        try {
            const res = await fetch(`${API}/api/health`)
            if (!res.ok) { setStatus({ ok: false }) ; return }
            const j = await res.json()
            setStatus({ ok: true, info: j })
        } catch (e) {
            setStatus({ ok: false, error: e.message })
        }
    }


    useEffect(() => { check(); const t = setInterval(check, 30000); return () => clearInterval(t) }, [])


    if (!status) return <div className="health">Checking...</div>
    return (
        <div className="health">
            {status.ok ? <span className="healthy">🟢 {status.info?.status || 'healthy'}</span> : <span className="down">🔴 Down</span>}
        </div>
    )
}