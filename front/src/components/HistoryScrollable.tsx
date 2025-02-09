import React, { useState, useEffect } from "react";
import HistorySingle from "./HistorySingle";
import "./HistoryScrollable.css";

interface HistoryItem {
  id: number;
  title: string;
  date: string;
  link: string;
}

const HistoryScrollable: React.FC = () => {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([]);

  useEffect(() => {
    if (chrome.storage) {
      chrome.storage.local.get({ history: [] }, (result) => {
        const history = result.history.map((url: string, index: number) => ({
          id: index,
          title: url,
          date: new Date().toISOString().split("T")[0],
          link: url,
        }));
        setHistoryItems(history);
      });
    }
  }, []);

  const handleDelete = (id: number) => {
    setHistoryItems(historyItems.filter((item) => item.id !== id));
  };

  return (
    <div className="history-scrollable">
      {historyItems.length === 0 ? (
        <p>No history items found.</p>
      ) : (
        historyItems.map((item) => (
          <HistorySingle
            key={item.id}
            title={item.title}
            date={item.date}
            link={item.link}
            onDelete={() => handleDelete(item.id)}
          />
        ))
      )}
    </div>
  );
};

export default HistoryScrollable;
