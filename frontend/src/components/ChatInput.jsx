import { useState } from "react";
import { Send } from "lucide-react";
import "./ChatInput.css";

function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");

  const submit = () => {
    if (!value.trim() || disabled) return;
    onSend(value);
    setValue("");
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  };

  return (
    <div className="input-area">
      <div className="input-box">
        <input
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Ask something about Sathish..."
          aria-label="Message"
        />
        <button
          type="button"
          onClick={submit}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
        >
          <Send size={17} />
        </button>
      </div>
      <span className="input-hint">Press Enter to send</span>
    </div>
  );
}

export default ChatInput;