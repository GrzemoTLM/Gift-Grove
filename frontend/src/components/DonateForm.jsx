import React, { useState } from "react";
import axios from "axios";

export default function DonateForm({ poolId, onSuccess, onCancel }) {
  const [amount, setAmount] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const accessToken = localStorage.getItem("accessToken");
      await axios.post(
        `/api/pools/${poolId}/donate/`,
        { amount },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      setSuccess("Wpłata udana!");
      setAmount("");
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.response?.data?.error || "Błąd podczas wpłaty");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 10, marginBottom: 10 }}>
      <input
        type="number"
        placeholder="Kwota"
        value={amount}
        onChange={e => setAmount(e.target.value)}
        required
        min="1"
        step="0.01"
        style={{ marginRight: 10 }}
      />
      <button type="submit">Wpłać</button>
      <button type="button" onClick={onCancel} style={{ marginLeft: 5 }}>Anuluj</button>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {success && <div style={{color: 'green'}}>{success}</div>}
    </form>
  );
} 