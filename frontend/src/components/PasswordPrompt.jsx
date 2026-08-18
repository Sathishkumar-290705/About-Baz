import { useState } from "react";
import { Check, Eye, EyeOff, LockKeyhole, X } from "lucide-react";
import "./PasswordPrompt.css";

function PasswordPrompt({ onSubmit, onCancel }) {
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);

  const submit = () => {
    if (password.trim()) onSubmit(password);
  };

  return (
    <div className="password-card">
      <div className="password-icon">
        <LockKeyhole size={17} />
      </div>

      <div className="password-content">
        <strong>Private information</strong>
        <p>This question requires a password to continue.</p>

        <div className="password-input">
          <input
            autoFocus
            type={show ? "text" : "password"}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") submit();
            }}
            placeholder="Enter password"
            aria-label="Password"
          />

          <button
            type="button"
            onClick={() => setShow((v) => !v)}
            aria-label={show ? "Hide password" : "Show password"}
          >
            {show ? <EyeOff size={16} /> : <Eye size={16} />}
          </button>
        </div>

        <div className="password-actions">
          <button className="cancel-button" onClick={onCancel}>
            <X size={14} /> Cancel
          </button>
          <button
            className="unlock-button"
            onClick={submit}
            disabled={!password.trim()}
          >
            <Check size={14} /> Unlock
          </button>
        </div>
      </div>
    </div>
  );
}

export default PasswordPrompt;