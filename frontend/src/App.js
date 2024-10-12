import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';


function App() {
  const [message, setMessage] = useState('');
  const [items, setItems] = useState([]);
  const [newItem, setNewItem] = useState('');

  useEffect(() => {
    // Načtení zprávy ze serveru
    axios.get('http://localhost:8007/')  // Backend běží na portu 8007
      .then(response => {
        setMessage(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching the message!", error);
      });

    // Načtení položek z databáze
    axios.get('http://localhost:8007/items')  // Načtení položek z API
      .then(response => {
        setItems(response.data);
      })
      .catch(error => {
        console.error("There was an error fetching items!", error);
      });
  }, []);

  const handleAddItem = () => {
    if (!newItem.trim()) return; // Prevent adding empty items
    axios.post('http://localhost:8007/items', { name: newItem })  // Přidání položky
      .then(response => {
        setItems([...items, response.data]); // Use response data to reflect the added item
        setNewItem('');
      })
      .catch(error => {
        console.error("There was an error adding the item!", error);
      });
  };

  return (
    <div className="App">
      <h1>{message}</h1>
      <h2>Items:</h2>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item.name}</li>
        ))}
      </ul>
      <div className="input-container">
        <input 
          type="text" 
          value={newItem} 
          onChange={(e) => setNewItem(e.target.value)} 
          placeholder="Add new item" 
        />
        <button onClick={handleAddItem}>Add Item</button>
      </div>
    </div>
  );
}

export default App;
