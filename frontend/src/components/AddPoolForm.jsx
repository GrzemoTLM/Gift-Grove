import React, { useState } from "react";
import axios from "axios";

export default function AddPoolForm({ onSuccess }) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [occasion, setOccasion] = useState("");
  const [targetAmount, setTargetAmount] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const accessToken = localStorage.getItem("accessToken");
      await axios.post(
        "/api/pools/create/",
        {
          title,
          description,
          occasion,
          target_amount: targetAmount,
        },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      setSuccess("Zbiórka została utworzona!");
      setTitle("");
      setDescription("");
      setOccasion("");
      setTargetAmount("");
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.response?.data?.error || "Błąd podczas tworzenia zbiórki");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 20, border: '1px solid #ccc', padding: 20, borderRadius: 8, maxWidth: 400 }}>
      <h2>Dodaj zbiórkę</h2>
      <input
        type="text"
        placeholder="Tytuł"
        value={title}
        onChange={e => setTitle(e.target.value)}
        required
        style={{ display: 'block', marginBottom: 10, width: '100%' }}
      />
      <input
        type="text"
        placeholder="Okazja"
        value={occasion}
        onChange={e => setOccasion(e.target.value)}
        required
        style={{ display: 'block', marginBottom: 10, width: '100%' }}
      />
      <textarea
        placeholder="Opis"
        value={description}
        onChange={e => setDescription(e.target.value)}
        style={{ display: 'block', marginBottom: 10, width: '100%' }}
      />
      <input
        type="number"
        placeholder="Kwota docelowa"
        value={targetAmount}
        onChange={e => setTargetAmount(e.target.value)}
        required
        min="1"
        step="0.01"
        style={{ display: 'block', marginBottom: 10, width: '100%' }}
      />
      <button type="submit">Utwórz zbiórkę</button>
      {error && <div style={{color: 'red', marginTop: 10}}>{error}</div>}
      {success && <div style={{color: 'green', marginTop: 10}}>{success}</div>}
    </form>
  );
} 