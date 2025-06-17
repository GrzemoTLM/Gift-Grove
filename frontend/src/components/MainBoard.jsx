import React from "react";

export default function MainBoard() {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 40 }}>
      <h1>Main Board</h1>
      <button style={{ margin: 10, padding: '10px 30px' }}>Dodaj zbiórkę</button>
      <button style={{ margin: 10, padding: '10px 30px' }}>Zaproszenia</button>
      <button style={{ margin: 10, padding: '10px 30px' }}>Mój profil</button>
      <button style={{ margin: 10, padding: '10px 30px' }}>Wyświetl moje zbiórki</button>
    </div>
  );
} 