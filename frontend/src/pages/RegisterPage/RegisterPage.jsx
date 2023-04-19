import React from 'react';
import { Container, Row, Col, Button, Form } from 'react-bootstrap';
import { Link } from 'react-router-dom';

function RegisterPage() {
    return (
        <Container>
            <Row>
                <Col>
                    <h1>Register</h1>
                    <Form>
                    <Form.Group controlId='name'>
                        <Form.Label>Full Name</Form.Label>
                        <Form.Control type='name' placeholder="Enter Full Name"/>
                    </Form.Group>
                    <Form.Group controlId='email'>
                        <Form.Label>Enter Email</Form.Label>
                        <Form.Control type='email' placeholder='Email'></Form.Control>
                    </Form.Group>
                    <Form.Group controlId='password'>
                        <Form.Label>Enter Password</Form.Label>
                        <Form.Control type='password' placeholder='Enter Password'></Form.Control>
                    </Form.Group>
                    <Form.Group controlId='confirmPassword'>
                        <Form.Label>Confirm Password</Form.Label>
                        <Form.Control type='password' placeholder='Confirm Password'></Form.Control>
                    </Form.Group>
                    <Button type='submit' variant='primary'>Register</Button>
                    </Form>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Link to='../login'>Sign In</Link> if you have an account!
                </Col>
            </Row>
        </Container>
    );
}

export default RegisterPage;