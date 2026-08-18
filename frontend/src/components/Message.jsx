import { Bot, User } from "lucide-react";
import "./Message.css";

function Message({ message }) {
  const isUser = message.role === "user";

  return (
    <div className={`message-row ${isUser ? "user-row" : "assistant-row"}`}>
      {!isUser && (
        <div className="message-avatar assistant-avatar">
          <Bot size={15} />
        </div>
      )}

      <div className={`message-bubble ${isUser ? "user-bubble" : "assistant-bubble"} ${message.error ? "error-bubble" : ""}`}>
        {message.text}
      </div>

      {isUser && (
        <div className="message-avatar user-avatar">
          <User size={15} />
        </div>
      )}
    </div>
  );
}

export default Message;