// frontend/src/components/ChatInterface.jsx
import { useState } from 'react'
import ReactMarkdown from 'react-markdown'

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I can help you with questions about Crustdata APIs. What would you like to know?' }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async (e) => {
    e.preventDefault()
    if (!inputMessage.trim()) return

    const userMessage = { role: 'user', content: inputMessage }
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputMessage }),
      })

      const data = await response.json()

      setMessages(prev => [...prev, {
        role: 'assistant',
        content: data.response
      }])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.'
      }])
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <div className="bg-gray-800 p-4">
        <h1 className="text-xl font-bold text-white">Crustdata API Assistant</h1>
      </div>

      {/* Chat Messages Area */}
      <div className="flex-1 bg-gray-900 overflow-y-auto p-4 space-y-6">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} max-w-4xl mx-auto`}
          >
            <div className={`max-w-[80%] space-y-2 ${message.role === 'user' ? 'ml-auto' : ''}`}>
              {/* Role Label */}
              <div className={`text-sm text-gray-400 ${message.role === 'user' ? 'text-right' : 'flex items-center gap-2'}`}>
                {message.role === 'user' ? (
                  'You'
                ) : (
                  <>
                    <span className="w-6 h-6 rounded-full bg-gray-600 flex items-center justify-center">🤖</span>
                    <span>Assistant</span>
                  </>
                )}
              </div>

              {/* Message Content */}
              <div
                className={`p-4 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-gray-700 text-white'
                }`}
              >
                <div className="prose prose-invert max-w-none">
                  <ReactMarkdown>
                    {message.content}
                  </ReactMarkdown>
                </div>
              </div>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start max-w-4xl mx-auto">
            <div className="bg-gray-700 p-4 rounded-lg">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-gray-800 border-t border-gray-700 p-6">
        <form onSubmit={sendMessage} className="max-w-4xl mx-auto flex gap-4">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask about Crustdata's APIs..."
            className="flex-1 p-4 rounded-lg bg-gray-700 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 min-h-[60px] max-h-[200px] resize-y"
            disabled={isLoading}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault()
                sendMessage(e)
              }
            }}
          />
          <button
            type="submit"
            disabled={isLoading}
            className="px-8 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-blue-800 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}