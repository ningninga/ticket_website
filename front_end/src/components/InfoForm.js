import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import React, { useEffect, useState } from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { useRef } from 'react';

function InfoForm({ onClose }) {
  const formRef = useRef();
  const [showFlightDateForm, setShowFlightDateForm] = useState(false);
  const [showAirlineForm, setShowAirlineForm] = useState(false);
  const [showFlightNumber, setShowFlightNumber] = useState(false);
  const [startDate, setStartDate] = useState(new Date());
  const [flightDate, setFlightDate] = useState(new Date());

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (formRef.current && !formRef.current.contains(event.target)) {
        onClose();
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [onClose])

  const handleSelectChange = (event) => {
    const selectedValue = event.target.value;
    if (selectedValue === 'HKA') {
      setShowFlightDateForm(true);
      setShowAirlineForm(true);
      setShowFlightNumber(true);
    } else {
      setShowFlightDateForm(false);
      setShowAirlineForm(false);
      setShowFlightNumber(false);
    }
  }

  // const handleSubmit = async (event) => {
  //   event.preventDefault();
  //   const formData = {
  //     departurePort: 'Shekou',
  //     arrivalPort: event.target.elements.arrivalPort.value,
  //     departureDate: startDate,
  //     flightDate: showFlightDateForm ? flightDate : null,
  //     airlines: showAirlineForm ? event.target.elements.airlines.value : null,
  //     email: event.target.elements.email.value,
  //   };
  //   // Send form data to the server
  //   const corsAnywhereUrl = 'http://0.0.0.0:8080/';
  //   const webAppUrl = 'https://script.google.com/macros/s/AKfycbzUCFdfgvZ7L9Cr3Y_9Y6M3yyHwHXLrKV1SYZh-aHGC1Uv4YwGK5pcRIvpC-zcXZv7z/exec';

  //   fetch(corsAnywhereUrl + webAppUrl, {
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //     },
  //     body: JSON.stringify(formData),
  //   })
  //     .then((response) => {
  //       if (!response.ok) {
  //         throw new Error(`HTTP error ${response.status}`);
  //       }
  //     })
  //     .then((data) => console.log(data))
  //     .catch((error) => console.error('Error:', error));
  //   // Close the form after submission
  //   onClose();

  // }

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = {
      departurePort: 'Shekou',
      arrivalPort: event.target.elements.arrivalPort.value,
      departureDate: startDate,
      flightDate: showFlightDateForm ? flightDate : null,
      airlines: showAirlineForm ? event.target.elements.airlines.value : null,
      flightnumber: showFlightNumber ? event.target.elements.flightnumber.value : null,
      email: event.target.elements.email.value,
    };
    console.log(formData);
    const apiUrl = 'http://localhost:8000';

    fetch(`${apiUrl}/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Acess-Control-Allow-Credentials': true,
      },
      body: JSON.stringify(formData),
      mode: 'cors',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error ${response.status}`);
        }
        return response.json();
      })
      .then((data) => console.log(data))
      .catch((error) => console.error('Error:', error));

    // Close the form after submission
    onClose();
  }
  return (
    <div className="FormWrapper">
      <div className='FormContainer' ref={formRef}>
        <Form onSubmit={(event) => handleSubmit(event)}>
          <Form.Group className='formItem'>
            <Row>
              <Col xs={12} sm={3}>
                <Form.Label>Departure Port</Form.Label>
              </Col>
              <Col xs={12} sm={9}>
                <Form.Control type="text" placeholder="Shekou" disabled />
              </Col>
            </Row>
          </Form.Group>

          <Form.Group className='formItem'>
            <Row>
              <Col xs={12} sm={3}>
                <Form.Label>Arrival Port</Form.Label>
              </Col>
              <Col xs={12} sm={9}>
                <Form.Select name="arrivalPort" onChange={handleSelectChange}>
                  <option>Arrival Port</option>
                  <option value="HKA">HongKong  Airport</option>
                  <option value="2">Two</option>
                  <option value="3">Three</option>
                </Form.Select>
              </Col>
            </Row>
          </Form.Group>

          <Form.Group className='formItem'>
            <Row>
              <Col xs={12} sm={3}>
                <Form.Label>Departure Date</Form.Label>
              </Col>
              <Col xs={12} sm={9}>
                <DatePicker name="departureDate"
                  selected={startDate}
                  onChange={(date) => setStartDate(date)}
                  style={{ marginTop: '2px' }}
                />
              </Col>
            </Row>
          </Form.Group>

          {showFlightDateForm && showAirlineForm && showFlightNumber &&(
            <>
              <Form.Group className='formItem'>
                <Row>
                  <Col xs={12} sm={3}>
                    <Form.Label>Flight Date</Form.Label>
                  </Col>
                  <Col xs={12} sm={9}>
                    <DatePicker name="flightDate"
                      selected={flightDate}
                      onChange={(date) => setFlightDate(date)}
                      showTimeSelect
                      dateFormat="Pp"
                    />
                  </Col>
                </Row>
                <Row>
                  <Col xs={12} sm={3}>
                    <Form.Label>Airlines</Form.Label>
                  </Col>
                  <Col xs={12} sm={9}>
                    <Form.Select name="airlines">
                      <option>Airlines</option>
                      <option value="QR">Qatar</option>
                      <option value="2">Two</option>
                      <option value="3">Three</option>
                    </Form.Select>
                  </Col>
                </Row>
                <Row>
                  <Col xs={12} sm={3}>
                    <Form.Label>Flight Number</Form.Label>
                  </Col>
                  <Col xs={12} sm={9}>
                    <Form.Control name="flightnumber" type="text" placeholder="please type your flight number" />
                  </Col>
                </Row>
              </Form.Group>
            </>
          )}

          <Form.Group className='formItem'>
            <Row>
              <Col xs={12} sm={3}>
                <Form.Label>Email</Form.Label>
              </Col>
              <Col xs={12} sm={9}>
                <Form.Control name="email" type="text" placeholder="please type your email address" />
              </Col>
            </Row>
          </Form.Group>

          <Form.Group className='buttons'>

            <Row>
              <Col xs={12} sm={6}>
                <Button className="close-button" onClick={onClose}>
                  Cancel
                </Button>
              </Col>
              <Col xs={12} sm={6}>
                <Button variant="primary" type="submit" className='SubmitButton'>
                  Submit
                </Button>
              </Col>
            </Row>


          </Form.Group>

        </Form>
      </div >
    </div>

  );
}

export default InfoForm;