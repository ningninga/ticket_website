import React, { useState } from 'react';
import './App.css';
import TopNavbar from './components/TopNavbar';
import 'bootstrap/dist/css/bootstrap.min.css';
import MainText from './components/MainText';
import MainButton from './components/MainButton';
import InfoForm from './components/InfoForm';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import About from './components/About';
import Contact from './components/Contact';

function App() {
  const [showForm, setShowForm] = useState(false);

  const toggleFormVisibility = () => {
    setShowForm(!showForm);
  };

  return (

    <BrowserRouter>
      <div className="App">
        
        <TopNavbar />
        <Routes>
        <Route path="" element={
            <>
              <div className="background-image"></div>
              <MainText />
              {!showForm && <MainButton onClick={toggleFormVisibility} text="Explore More"/>}
              {showForm && (
                <div className="FormWrapper">
                  <InfoForm onClose={toggleFormVisibility} />
                </div>
              )}
            </>
          } />
          <Route path="/home" element={
            <>
              <div className="background-image"></div>
              <MainText />
              {!showForm && <MainButton onClick={toggleFormVisibility} text="Explore More"/>}
              {showForm && (
                <div className="FormWrapper">
                  <InfoForm onClose={toggleFormVisibility} />
                </div>
              )}
            </>
          } />
          <Route path="/about" element={ 
          <>
            
            <About />
            
          </>
          } 
          />
          <Route path="/contact" element={<Contact />} />
        </Routes>

      </div>
    </BrowserRouter>
  );
}

export default App;
