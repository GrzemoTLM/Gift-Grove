import React, { useState } from "react";
import axios from "axios";
import AddPoolForm from "./AddPoolForm";
import MyPoolsList from "./MyPoolsList";
import EditPoolForm from "./EditPoolForm";
import InvitationsList from "./InvitationsList";

export default function MainBoard({ onLogout }) {
  const [profile, setProfile] = useState(null);
  const [error, setError] = useState("");
  const [showAddPool, setShowAddPool] = useState(false);
  const [showMyPools, setShowMyPools] = useState(false);
  const [editingPool, setEditingPool] = useState(null);
  const [showInvitations, setShowInvitations] = useState(false);

  const handleShowProfile = async () => {
    setError("");
    try {
      const accessToken = localStorage.getItem("accessToken");
      const response = await axios.get("/api/auth/me/", {
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
      setProfile(response.data);
    } catch (err) {
      setError("Failed to fetch profile");
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 40 }}>
      <h1>Main Board</h1>
      <button style={{ margin: 10, padding: '10px 30px' }} onClick={() => setShowAddPool((v) => !v)}>
        Dodaj zbiórkę
      </button>
      <button style={{ margin: 10, padding: '10px 30px' }} onClick={() => setShowInvitations((v) => !v)}>
        Zaproszenia
      </button>
      <button style={{ margin: 10, padding: '10px 30px' }} onClick={handleShowProfile}>Mój profil</button>
      <button style={{ margin: 10, padding: '10px 30px' }} onClick={() => setShowMyPools((v) => !v)}>
        Wyświetl moje zbiórki
      </button>
      <button style={{ margin: 10, padding: '10px 30px', background: '#e74c3c', color: 'white' }} onClick={onLogout}>
        Wyloguj
      </button>
      {showAddPool && <AddPoolForm onSuccess={() => setShowAddPool(false)} />}
      {showInvitations && <InvitationsList />}
      {showMyPools && !editingPool && <MyPoolsList onEdit={pool => setEditingPool(pool)} />}
      {editingPool && <EditPoolForm pool={editingPool} onSuccess={() => { setEditingPool(null); setShowMyPools(false); }} onCancel={() => setEditingPool(null)} />}
      {profile && (
        <div style={{ marginTop: 20, border: '1px solid #ccc', padding: 20, borderRadius: 8 }}>
          <h2>Twój profil</h2>
          <p><b>Username:</b> {profile.username}</p>
          <p><b>Email:</b> {profile.email}</p>
          <p><b>Role:</b> {profile.role}</p>
        </div>
      )}
      {error && <div style={{color: 'red', marginTop: 10}}>{error}</div>}
    </div>
  );
} 