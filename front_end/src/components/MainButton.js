import Button from 'react-bootstrap/Button';
import React from 'react';

function MainButton({onClick, text}) {
  return (
    <>
      <div className="mb-2 fixed-button">
        <Button 
        variant="secondary" 
        size="lg"
        onClick={onClick}
        >
          {text}
        </Button>
      </div>
    
    </>
  );
}

export default MainButton;