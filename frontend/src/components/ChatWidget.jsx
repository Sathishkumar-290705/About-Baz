import { useEffect, useRef, useState } from "react";
import {
  Bot,
  LockKeyhole,
  RotateCcw,
  X,
} from "lucide-react";
import { sendMessage } from "../services/api";
import Message from "./Message";
import ChatInput from "./ChatInput";
import PasswordPrompt from "./PasswordPrompt";
import "./ChatWidget.css";

const initialMessage = {
  id: 1,
  role: "assistant",
  text: "Hi! I'm About Sathish. Ask me anything about him.",
};

function ChatWidget({ open, onClose }) {
  const [messages, setMessages] = useState([initialMessage]);
  const [loading, setLoading] = useState(false);
  const [passwordPrompt, setPasswordPrompt] = useState(null);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading, passwordPrompt]);

  if (!open) return null;

  const askBackend = async (question, password = null) => {
    setLoading(true);

    try {
      const data = await sendMessage(question, password);

      if (data.requires_password) {
        setPasswordPrompt({ question });
      } else {
        setPasswordPrompt(null);
        setMessages((prev) => [
          ...prev,
          {
            id: crypto.randomUUID(),
            role: "assistant",
            text: data.answer,
          },
        ]);
      }
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: "assistant",
          text: error.message || "Something went wrong. Please try again.",
          error: true,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (question) => {
    if (!question.trim() || loading) return;

    setMessages((prev) => [
      ...prev,
      {
        id: crypto.randomUUID(),
        role: "user",
        text: question.trim(),
      },
    ]);

    await askBackend(question.trim());
  };

  const handlePassword = async (password) => {
    if (!password.trim() || loading || !passwordPrompt) return;
    await askBackend(passwordPrompt.question, password);
  };

  const resetChat = () => {
    setMessages([initialMessage]);
    setPasswordPrompt(null);
  };

  return (
    <section className="chat-widget" aria-label="About Sathish chatbot">
      <header className="chat-header">
        <div className="chat-title">
          <div className="bot-avatar">
            <Bot size={21} />
          </div>
          <div>
            <strong>About Sathish</strong>
            <span><i /> Online</span>
          </div>
        </div>

        <div className="header-actions">
          <button type="button" onClick={resetChat} title="New chat" aria-label="New chat">
            <RotateCcw size={17} />
          </button>
          <button type="button" onClick={onClose} title="Close chat" aria-label="Close chat">
            <X size={19} />
          </button>
        </div>
      </header>

      <div className="chat-messages">
        <div className="privacy-note">
          <LockKeyhole size={14} />
          Some personal information is password protected.
        </div>

        {messages.map((message) => (
          <Message key={message.id} message={message} />
        ))}

        {loading && (
          <div className="message-row assistant-row">
            <div className="message-avatar assistant-avatar">
              <Bot size={16} />
            </div>
            <div className="typing">
              <span />
              <span />
              <span />
            </div>
          </div>
        )}

        {passwordPrompt && !loading && (
          <PasswordPrompt
            onSubmit={handlePassword}
            onCancel={() => setPasswordPrompt(null)}
          />
        )}

        <div ref={bottomRef} />
      </div>

      <ChatInput disabled={loading || Boolean(passwordPrompt)} onSend={handleSend} />
        
      <footer className="chat-footer">
        <span>Powered by RAG + Gemini</span>
      </footer>
    </section>
  );
}

export default ChatWidget;