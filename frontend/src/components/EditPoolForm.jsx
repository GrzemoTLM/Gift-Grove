import React, { useState } from "react";
import axios from "axios";

export default function EditPoolForm({ pool, onSuccess, onCancel }) {
  const [title, setTitle] = useState(pool.title);
  const [description, setDescription] = useState(pool.description);
  const [occasion, setOccasion] = useState(pool.occasion);
  const [targetAmount, setTargetAmount] = useState(pool.target_amount);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const accessToken = localStorage.getItem("accessToken");
      // Zakładam, że endpoint PATCH /api/pools/{id}/edit/ będzie dostępny
      await axios.patch(
        `/api/pools/${pool.id}/edit/`,
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
      setSuccess("Zbiórka została zaktualizowana!");
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.response?.data?.error || "Błąd podczas edycji zbiórki");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 20, border: '1px solid #ccc', padding: 20, borderRadius: 8, maxWidth: 400 }}>
      <h2>Edytuj zbiórkę</h2>
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
      <button type="submit">Zapisz zmiany</button>
      <button type="button" onClick={onCancel} style={{ marginLeft: 10 }}>Anuluj</button>
      {error && <div style={{color: 'red', marginTop: 10}}>{error}</div>}
      {success && <div style={{color: 'green', marginTop: 10}}>{success}</div>}
    </form>
  );
} 