import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "./HistorySingle.css";

interface HistorySingleProps {
  title: string;
  date: string;
  link: string;
  onDelete: () => void;
}

const HistorySingle: React.FC<HistorySingleProps> = ({
  title,
  date,
  link,
  onDelete,
}) => {
  return (
    <div
      className="toast show"
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div className="toast-header">
        <strong className="me-auto">{title}</strong>
        <small>{date}</small>
        <button
          type="button"
          className="btn-close"
          aria-label="Close"
          onClick={onDelete}
        ></button>
      </div>
      <div className="toast-body">
        <a
          href={link}
          target="_blank"
          rel="noopener noreferrer"
          className="toast-link"
        >
          {link}
        </a>
      </div>
    </div>
  );
};

export default HistorySingle;
