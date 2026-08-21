import { useState } from "react";
import { MessageCircle, Moon, MoonIcon, Sparkles } from "lucide-react";
import ChatWidget from "./components/ChatWidget";
import "./App.css";

function App() {
  const [chatOpen, setChatOpen] = useState(true);

  return (
    <main className="app">
      <section className="hero">
        <div className="hero-badge">
          <MoonIcon size={15} />
          soul of sathish
        </div>

        <h1>
          Get to know <span>Sathish..</span>
        </h1>

        <p>
          Ask me anything about Sathish — his skills, interests, education,
          projects, and pretty much everything else you want to know.
        </p>

        <button type="button" className="hero-button" onClick={() => setChatOpen(true)}>
          <MessageCircle size={18} />
          Start chatting
        </button>
      </section>

      <ChatWidget open={chatOpen} onClose={() => setChatOpen(false)} />

      {!chatOpen && (
        <button
          type="button"
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