import React, { useState } from "react";
import HistorySingle from "./HistorySingle";
import "./HistoryScrollable.css";

interface HistoryItem {
  id: number;
  title: string;
  date: string;
  link: string;
}

const HistoryScrollable: React.FC = () => {
  const [historyItems, setHistoryItems] = useState<HistoryItem[]>([
    // Example items
    {
      id: 1,
      title: "Example Site 1",
      date: "2025-02-08",
      link: "https://example.com/1",
    },
    {
      id: 2,
      title: "Example Site 2",
      date: "2025-02-07",
      link: "https://example.com/2",
    },
    {
      id: 3,
      title: "Example Site 3",
      date: "2025-02-07",
      link: "https://example.com/2",
    },
    {
      id: 4,
      title: "Example Site 4",
      date: "2025-02-07",
      link: "https://example.com/2",
    },
  ]);

  const handleDelete = (id: number) => {
    setHistoryItems(historyItems.filter((item) => item.id !== id));
  };

  return (
    <div className="history-scrollable">
      {historyItems.map((item) => (
        <HistorySingle
          key={item.id}
          title={item.title}
          date={item.date}
          link={item.link}
          onDelete={() => handleDelete(item.id)}
        />
      ))}
    </div>
  );
};

export default HistoryScrollable;
