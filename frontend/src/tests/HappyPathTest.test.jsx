
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

  const loginText = await screen.findByRole("heading", { name: /log in/i });
  expect(loginText).toBeInTheDocument();

  const emailField = await screen.findByRole("textbox", {
    name: /email address/i,
  });
  expect(emailField).toBeInTheDocument();

  const passwordField = await screen.findByLabelText(/password/i);
  expect(passwordField).toBeInTheDocument();

  const loginButton = await screen.findByRole("button", { name: /log in/i });
  expect(loginButton).toBeInTheDocument();
  expect(loginButton).toBeDisabled();

  const registerLink = await screen.findByRole("link", { name: /register/i });
  expect(registerLink).toBeInTheDocument();
  
})