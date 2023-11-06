import React from 'react';
import './Toast.css';

const Toast = ({ message, onClose, style }) => {
  if (!message) {
    style = { opacity: 0, pointerEvents: 'none' };
  }

  return (
    <div className="error-toast" style={style}>
      <div className="error-toast-content">
        <span className="error-toast-message">{message}</span>
        <button className="error-toast-close" onClick={onClose}>
          &times;
        </button>
      </div>
    </div>
  );
};

export default Toast;
