import { useState } from "react";
import { MessageCircle, Sparkles } from "lucide-react";
import ChatWidget from "./components/ChatWidget";
import "./App.css";

function App() {
  const [chatOpen, setChatOpen] = useState(true);

  return (
    <main className="app">
      <section className="hero">
        <div className="hero-badge">
          <Sparkles size={15} />
          Personal RAG Assistant
        </div>

        <h1>
          Get to know <span>Baz.</span>
        </h1>

        <p>
          Ask questions about Sathish's skills, interests, education,
          projects, and more.
        </p>

        <button className="hero-button" onClick={() => setChatOpen(true)}>
          <MessageCircle size={18} />
          Start chatting
        </button>
      </section>

      <ChatWidget open={chatOpen} onClose={() => setChatOpen(false)} />

      {!chatOpen && (
        <button
          className="floating-chat-button"
          onClick={() => setChatOpen(true)}
          aria-label="Open chat"
        >
          <MessageCircle size={24} />
        </button>
      )}
    </main>
  );
}

export default App;