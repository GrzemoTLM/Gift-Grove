import React, { useEffect, useState } from "react";
import axios from "axios";

export default function InvitationsList() {
  const [invitations, setInvitations] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [success, setSuccess] = useState("");

  const fetchInvitations = async () => {
    setError("");
    setSuccess("");
    setLoading(true);
    try {
      const accessToken = localStorage.getItem("accessToken");
      const response = await axios.get("/api/pools/invitations/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setInvitations(response.data);
    } catch (err) {
      setError("Błąd podczas pobierania zaproszeń");
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchInvitations();
  }, []);

  const handleAccept = async (invitationId) => {
    setError("");
    setSuccess("");
    try {
      const accessToken = localStorage.getItem("accessToken");
      await axios.post(`/api/pools/invitations/${invitationId}/accept/`, {}, {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setSuccess("Zaproszenie zaakceptowane!");
      setInvitations(invitations.filter(inv => inv.id !== invitationId));
    } catch (err) {
      setError("Błąd podczas akceptowania zaproszenia");
    }
  };

  if (loading) return <div>Ładowanie...</div>;
  if (error) return <div style={{color: 'red'}}>{error}</div>;

  return (
    <div style={{ marginTop: 20, maxWidth: 600 }}>
      <h2>Twoje zaproszenia</h2>
      {success && <div style={{color: 'green'}}>{success}</div>}
      {invitations.length === 0 && <div>Brak zaproszeń.</div>}
      <ul style={{ listStyle: 'none', padding: 0 }}>
        {invitations.map(inv => (
          <li key={inv.id} style={{ border: '1px solid #ccc', borderRadius: 8, marginBottom: 10, padding: 10 }}>
            <b>{inv.pool_title}</b> — zaproszenie od <b>{inv.invited_by.username}</b><br/>
            <button style={{ marginTop: 5 }} onClick={() => handleAccept(inv.id)}>Akceptuj</button>
          </li>
        ))}
      </ul>
    </div>
  );
} 