import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Header } from './components/Header';
import { SearchForm } from './components/SearchForm';
import { BookList } from './components/BookList';
import { Pagination } from './components/Pagination';
import { translations } from './components/Translations';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import './App.css';

function App() {
  // Stavové proměnné
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const [searchQueries, setSearchQueries] = useState({
    title: '',
    author: '',
    isbn: ''
  });
  const [currentSearchQueries, setCurrentSearchQueries] = useState({
    title: '',
    author: '',
    isbn: ''
  });
  const [language, setLanguage] = useState('cs');
  const [user, setUser] = useState(null);
  const [showLoginForm, setShowLoginForm] = useState(false);
  const [showRegisterForm, setShowRegisterForm] = useState(false);

  // Efekty
  useEffect(() => {
    fetchBooks(currentPage, currentSearchQueries);
    checkLoggedInUser();
  }, [currentPage, currentSearchQueries]);

  // API volání
  const fetchBooks = (page, queries) => {
    setLoading(true);
    const queryParams = new URLSearchParams({
      page: page,
      per_page: 25,
      title: queries.title,
      author: queries.author,
      isbn: queries.isbn
    });

    axios.get(`http://localhost:8007/api/books?${queryParams.toString()}`)
      .then(response => {
        setBooks(response.data.books);
        setTotalPages(response.data.total_pages);
        setLoading(false);
      })
      .catch(error => {
        console.error("There was an error fetching the books!", error);
        setError(translations[language].error);
        setLoading(false);
      });
  };

  const checkLoggedInUser = async () => {
    try {
      const response = await axios.get('http://localhost:8007/api/user');
      setUser(response.data.user);
    } catch (error) {
      console.error("Error checking logged in user", error);
    }
  };

  // Handlery
  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  const handleSearchChange = (field) => (event) => {
    setSearchQueries(prev => ({
      ...prev,
      [field]: event.target.value
    }));
  };

  const handleSearchSubmit = (event) => {
    event.preventDefault();
    setCurrentSearchQueries(searchQueries);
    setCurrentPage(1);
  };

  const handleClearSearch = () => {
    setSearchQueries({
      title: '',
      author: '',
      isbn: ''
    });
    setCurrentSearchQueries({
      title: '',
      author: '',
      isbn: ''
    });
    setCurrentPage(1);
  };

  const toggleLanguage = () => {
    setLanguage(prev => (prev === 'cs' ? 'en' : 'cs'));
  };

  const handleLogin = (userData) => {
    setUser(userData);
    setShowLoginForm(false);
    setShowRegisterForm(false);
  };

  const handleRegister = () => {
    setShowRegisterForm(false);
    setShowLoginForm(true);
  };

  const handleLogout = async () => {
    try {
      await axios.post('http://localhost:8007/api/logout');
      setUser(null);
    } catch (error) {
      console.error("Error logging out", error);
    }
  };

  const toggleLoginForm = () => {
    setShowLoginForm(!showLoginForm);
    setShowRegisterForm(false);
  };

  const toggleRegisterForm = () => {
    setShowRegisterForm(!showRegisterForm);
    setShowLoginForm(false);
  };

  // Loading a Error stavy
  if (loading) return (
    <div className="loading-container">
      <div className="loading">{translations[language].loading}</div>
    </div>
  );

  if (error) return (
    <div className="error-container">
      <div className="error">{error}</div>
    </div>
  );

  // Render
  return (
    <div className="App">
      <Header 
        language={language}
        toggleLanguage={toggleLanguage}
        user={user}
        handleLogout={handleLogout}
        toggleLoginForm={toggleLoginForm}
        toggleRegisterForm={toggleRegisterForm}
        translations={translations}
      />
      
      {showLoginForm && (
        <LoginForm 
          onLogin={handleLogin} 
          translations={translations} 
          language={language} 
        />
      )}
      
      {showRegisterForm && (
        <RegisterForm 
          onRegister={handleRegister} 
          translations={translations} 
          language={language} 
        />
      )}
      
      <SearchForm 
        searchQueries={searchQueries}
        handleSearchChange={handleSearchChange}
        handleSearchSubmit={handleSearchSubmit}
        handleClearSearch={handleClearSearch}
        currentSearchQueries={currentSearchQueries}
        translations={translations}
        language={language}
      />

      {books.length > 0 ? (
        <>
          <BookList 
            books={books}
            translations={translations}
            language={language}
          />
          <Pagination 
            currentPage={currentPage}
            totalPages={totalPages}
            handlePageChange={handlePageChange}
            translations={translations}
            language={language}
          />
        </>
      ) : (
        <div className="no-results">{translations[language].noResults}</div>
      )}
    </div>
  );
}

export default App;