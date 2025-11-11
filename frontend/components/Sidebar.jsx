import React, { useEffect, useState } from 'react'
import useChatAPI from '../hooks/useChatAPI'


export default function Sidebar() {
    const { getModels, loadModel, unloadModel } = useChatAPI()
    const [models, setModels] = useState([])
    const [selected, setSelected] = useState(null)


    useEffect(() => {
        async function fetchModels() {
            const m = await getModels()
            if (m?.models) setModels(m.models)
        }
        fetchModels()
    }, [])


    return (
        <aside className="sidebar">
            <div className="sidebar-section">
                <h3>Model Management</h3>
                <div className="model-list">
                    {models.length === 0 && <div className="muted">No models detected</div>}
                    {models.map((mod) => (
                        <div key={mod.name} className="model-item">
                            <div className="model-name">{mod.name}</div>
                            <div className="model-actions">
                                <button onClick={() => { setSelected(mod.name); loadModel({ model: mod.name, keep_alive: '30m' }) }}>Load</button>
                                <button onClick={() => unloadModel({ model: mod.name })}>Unload</button>
                            </div>
                        </div>
                    ))}
                </div>
            </div>


            <div className="sidebar-section">
                <h3>Conversations</h3>
                <div className="conversations">
                    <button onClick={() => localStorage.removeItem('chat_history')}>Clear History</button>
                    <div className="muted">Saved locally in browser</div>
                </div>
            </div>
        </aside>
    )
}