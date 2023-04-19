
import { screen, render } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import App from "../App";

test("Happy path test", async () => {
  render(<App />);

  const copyrightText = await screen.findByText(/copyright/i);
  expect(copyrightText).toBeInTheDocument();

  const loginLink = await screen.findByRole("link", { name: /login/i });
  expect(loginLink).toBeInTheDocument();
  userEvent.click(loginLink);

  const loginText = await screen.findByRole("heading", { name: /sign in/i });
  expect(loginText).toBeInTheDocument();

  const emailField = await screen.findByRole("textbox", {
    name: /email address/i,
  });
  expect(emailField).toBeInTheDocument();

  const passwordField = await screen.findByLabelText(/password/i);
  expect(passwordField).toBeInTheDocument();

  const loginButton = await screen.findByRole("button", { name: /sign in/i });
  expect(loginButton).toBeInTheDocument();
  expect(loginButton).toBeDisabled();

  const registerLink = await screen.findByRole("link", { name: /register/i });
  expect(registerLink).toBeInTheDocument();
  userEvent.click(registerLink);

  const registerHeader = await screen.findByRole('heading', {name: /register/i});
  expect(registerHeader).toBeInTheDocument();

  const nameText = await screen.findByRole('textbox', {name: /full name/i});
  expect(nameText).toBeInTheDocument();

  const emailText = await screen.findByRole('textbox', {name: /email/i});
  expect(emailText).toBeInTheDocument();

  const passwordText = await screen.findByLabelText(/enter password/i);
  expect(passwordText).toBeInTheDocument();

  const confirmPassword = await screen.findByLabelText(/confirm password/i);
  expect(confirmPassword).toBeInTheDocument();

  const signinLink = await screen.findByRole('link', {name: /sign in/i});
  expect(signinLink).toBeInTheDocument(); 

  const registerButton = await screen.findByRole('button', {name: /register/i})
  expect(registerButton).toBeInTheDocument();
  expect(registerButton).toBeDisabled()

  userEvent.clear(nameText);
  userEvent.type(nameText, 'Someone new');

  userEvent.clear(emailText);
  userEvent.type(emailText, "email@email.com");

  userEvent.clear(passwordText);
  userEvent.type(passwordText, "Password@123");

  userEvent.clear(confirmPassword);
  userEvent.type(confirmPassword, "Password@123");

  expect(registerButton).tobeEnabled();
})