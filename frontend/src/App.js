import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [books, setBooks] = useState([]); // Pro ukládání knih

  useEffect(() => {
    axios.get('http://sk08-web:5000/')  // Změna na název backend služby
      .then(response => {
        setBooks(response.data.books); // Předpokládáme, že odpověď obsahuje pole knih
      })
      .catch(error => {
        console.error("There was an error fetching the books!", error);
      });
  }, []);

  return (
    <div className="App">
      <h1>Katalog Knih</h1>
      <div className="book-container">
        {books.map(book => (
          <div className="book" key={book.id}>
            <img src={book.image_url} alt={book.title} />
            <h2>{book.title}</h2>
            <p>Cena: {book.price} Kč</p>
          </div>
        ))}
      </div>

      <style jsx>{`
        .book-container {
          display: flex;
          flex-wrap: wrap;
          justify-content: center;
        }
        .book {
          border: 1px solid #ccc;
          border-radius: 8px;
          padding: 10px;
          margin: 10px;
          text-align: center;
          width: 150px;
        }
        img {
          max-width: 100%;
          height: auto;
          border-radius: 4px;
        }
      `}</style>
    </div>
  );
}

export default App;
