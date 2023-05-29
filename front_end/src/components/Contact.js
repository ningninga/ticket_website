import React from 'react';

function Contact() {
  return (
    <div>
      <div className="center-black"></div>
      <div className='center-content'>
        <img src='/images/bg-image.jpg' className='halfSteamerImage item' alt='backgroundpic'/>
        <div className="sub-content item">
          <p className="subtitle">Contact us</p>
          <p className="sub-desp">We are aimed at solving your travel problems. </p>
          <p className="sub-desp">
            If you have any question, please contact: <a href="mailto:jjhelpcenter@outlook.com">jjhelpcenter@outlook.com</a>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Contact;