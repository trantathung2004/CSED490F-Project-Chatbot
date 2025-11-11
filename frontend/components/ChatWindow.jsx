import React, { useState, useEffect, useRef } from 'react'
import useChatAPI from '../hooks/useChatAPI'


export default function ChatWindow() {
    const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'
    const { sendMessage, lastResponse, isLoading } = useChatAPI()
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState('')
    const bottomRef = useRef(null)


    useEffect(() => {
        if (lastResponse) {
            setMessages(prev => [...prev, { role: 'assistant', text: lastResponse }])
        }
    }, [lastResponse])


    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])


    async function onSend() {
        if (!input.trim()) return
        const userText = input.trim()
        setMessages(prev => [...prev, { role: 'user', text: userText }])
        setInput('')
        await sendMessage({ message: userText })
        // bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }


    return (
        <div className="chat-window">
            <div className="messages">
                {messages.map((m, i) => (
                    <div key={i} className={`bubble ${m.role}`}>
                        <pre className="bubble-text">{m.text}</pre>
                    </div>
                ))}
                {isLoading && (
                    <div className="bubble assistant">...
                    </div>
                )}
                <div ref={bottomRef} />
            </div>


            <div className="composer">
                <textarea value={input} onChange={e => setInput(e.target.value)} placeholder="Type a message..." />
                <div className="composer-actions">
                    <button onClick={onSend} disabled={isLoading}>Send</button>
                </div>
            </div>


            <div className="footer-note">API base: <code>{API_BASE}</code></div>
        </div>
    )
}