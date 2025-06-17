import React, { useEffect, useState } from "react";
import axios from "axios";

export default function DonationHistory({ poolId, onClose }) {
  const [donations, setDonations] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDonations = async () => {
      setError("");
      setLoading(true);
      try {
        const accessToken = localStorage.getItem("accessToken");
        const response = await axios.get(`/api/pools/donations/${poolId}/`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        setDonations(response.data);
      } catch (err) {
        setError("Błąd podczas pobierania historii wpłat");
      }
      setLoading(false);
    };
    fetchDonations();
  }, [poolId]);

  if (loading) return <div>Ładowanie historii wpłat...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <div style={{ marginTop: 10, marginBottom: 10, border: '1px solid #ccc', borderRadius: 8, padding: 10 }}>
      <h3>Historia wpłat</h3>
      <button onClick={onClose} style={{ marginBottom: 10 }}>Zamknij</button>
      {donations.length === 0 && <div>Brak wpłat.</div>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {donations.map(donation => (
          <li key={donation.id} style={{ marginBottom: 8 }}>
            <b>{donation.donor.username}</b>: {donation.amount} zł — {new Date(donation.donated_at).toLocaleString()}
          </li>
        ))}
      </ul>
    </div>
  );
} 