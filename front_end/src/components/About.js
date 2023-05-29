import React from 'react';

function About() {
  return (
    <div>
      <div className="center-black"></div>
      <div className='center-content'>
        <img src='/images/bg-image.jpg' className='halfSteamerImage item' alt='backgroundpic'/>
        <div className="sub-content item">
          <p className="subtitle">About us</p>
          <p className="sub-desp">We are aimed at solving your travel problems.</p>
          <p className="sub-desp">We know how hard it is to get a ticket; we know that without a ticket,
            the next ticket will be null and void; we understand your anxiety because we've been there.</p>
          <p className="sub-desp">That's why we are here! </p>
          <p className="sub-desp">We monitor the ticket information all the time, so that you don't miss any chance to buy tickets! </p>
        </div>
      </div>
    </div>
  );
}

export default About;