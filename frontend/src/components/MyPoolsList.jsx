import React, { useEffect, useState } from "react";
import axios from "axios";
import DonateForm from "./DonateForm";
import DonationHistory from "./DonationHistory";

function InviteUserForm({ poolId, onSuccess, onCancel }) {
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    try {
      const accessToken = localStorage.getItem("accessToken");
      await axios.post(
        `/api/pools/${poolId}/invite/`,
        { invited_username: username },
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        }
      );
      setSuccess("Użytkownik został zaproszony!");
      setUsername("");
      if (onSuccess) onSuccess();
    } catch (err) {
      setError(err.response?.data?.error || "Błąd podczas zapraszania");
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: 10, marginBottom: 10 }}>
      <input
        type="text"
        placeholder="Nazwa użytkownika"
        value={username}
        onChange={e => setUsername(e.target.value)}
        required
        style={{ marginRight: 10 }}
      />
      <button type="submit">Zaproś</button>
      <button type="button" onClick={onCancel} style={{ marginLeft: 5 }}>Anuluj</button>
      {error && <div style={{color: 'red'}}>{error}</div>}
      {success && <div style={{color: 'green'}}>{success}</div>}
    </form>
  );
}

export default function MyPoolsList({ onEdit }) {
  const [pools, setPools] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [invitePoolId, setInvitePoolId] = useState(null);
  const [donatePoolId, setDonatePoolId] = useState(null);
  const [historyPoolId, setHistoryPoolId] = useState(null);

  const fetchPools = async () => {
    setError("");
    setLoading(true);
    try {
      const accessToken = localStorage.getItem("accessToken");
      const response = await axios.get("/api/pools/all/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setPools(response.data);
    } catch (err) {
      setError("Błąd podczas pobierania zbiórek");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchPools();
  }, []);

  const handleDelete = async (poolId) => {
    if (!window.confirm("Czy na pewno chcesz usunąć tę zbiórkę?")) return;
    try {
      const accessToken = localStorage.getItem("accessToken");
      await axios.delete(`/api/pools/${poolId}/delete/`, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setPools(pools.filter(pool => pool.id !== poolId));
    } catch (err) {
      setError("Błąd podczas usuwania zbiórki");
    }
  };

  if (loading) return <div>Ładowanie...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <div style={{ marginTop: 20, maxWidth: 600 }}>
      <h2>Moje zbiórki</h2>
      {pools.length === 0 && <div>Brak zbiórek.</div>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {pools.map(pool => (
          <li key={pool.id} style={{ border: '1px solid #ccc', borderRadius: 8, marginBottom: 10, padding: 10 }}>
            <b>{pool.title}</b> ({pool.occasion})<br/>
            <span>Cel: {pool.target_amount} zł, Zebrano: {pool.current_amount} zł</span><br/>
            <button style={{ marginTop: 5, marginRight: 10 }} onClick={() => onEdit(pool)}>Edytuj</button>
            <button style={{ marginTop: 5, marginRight: 10 }} onClick={() => setInvitePoolId(pool.id)}>Zaproś</button>
            <button style={{ marginTop: 5, marginRight: 10 }} onClick={() => setDonatePoolId(pool.id)}>Wpłać</button>
            <button style={{ marginTop: 5, marginRight: 10 }} onClick={() => setHistoryPoolId(pool.id)}>Historia wpłat</button>
            <button style={{ marginTop: 5 }} onClick={() => handleDelete(pool.id)}>Usuń</button>
            {invitePoolId === pool.id && (
              <InviteUserForm
                poolId={pool.id}
                onSuccess={() => setInvitePoolId(null)}
                onCancel={() => setInvitePoolId(null)}
              />
            )}
            {donatePoolId === pool.id && (
              <DonateForm
                poolId={pool.id}
                onSuccess={() => { setDonatePoolId(null); fetchPools(); }}
                onCancel={() => setDonatePoolId(null)}
              />
            )}
            {historyPoolId === pool.id && (
              <DonationHistory
                poolId={pool.id}
                onClose={() => setHistoryPoolId(null)}
              />
            )}
          </li>
        ))}
      </ul>
    </div>
  );
} 