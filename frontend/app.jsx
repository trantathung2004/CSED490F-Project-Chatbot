import React from 'react'
import ChatWindow from './components/ChatWindow'
import Sidebar from './components/Sidebar'
import HealthStatus from './components/HealthStatus'


export default function App() {
    return (
        <div className="app-root">
            <header className="app-header">
                <h1>Raspberry Pi Chatbot</h1>
                <HealthStatus />
            </header>
            <div className="app-body">
                <Sidebar />
                <main className="app-main">
                    <ChatWindow />
                </main>
            </div>
        </div>
    )
}