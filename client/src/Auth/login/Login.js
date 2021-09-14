import React, { useState } from "react";
import { login } from "../../flux/actions/authAction";
import axios from "axios";
import { Redirect } from "react-router";
import { useSelector, useDispatch } from "react-redux";
import "./Login.css";

const Login = () => {
  const dispatch = useDispatch();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [auth, setAuth] = useState(false);
  //   const [msg, setMsg] = useState(null);
  const handleChangeEmail = (e) => setEmail(e.target.value);
  const handleChangePassword = (e) => setPassword(e.target.value);

  const handleOnSubmit = (e) => {
    e.preventDefault();
    const user = { email, password };
    // Attempt to login
    const body = JSON.stringify(user);
    // Headers
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    // Request body
    axios
      .post("url/login", body, config)
      .then((res) => {
        dispatch(login(res.data));
        setAuth(true);
      })
      .catch((err) => {
        console.log(err);
        dispatch({
          type: "REGISTER_FAIL",
        });
      });

    // const data = {
    //   token: "#7135623",
    //   user: body,
    // };
    // dispatch(login(data));
  };
  const authenticated = useSelector((state) => state.auth.isAuthenticated);
  if (auth || authenticated) {
    return <Redirect to="/dashboard" />;
  }
  // login code goes here
  return (
    <div>
      <form>
        <h1 class="h3 mb-3 fw-normal">Please sign in</h1>

        <div class="form-floating">
          <input
            type="email"
            onChange={handleChangeEmail}
            class="form-control"
            id="floatingInput"
          />
          <label for="floatingInput">Email address</label>
        </div>
        <div class="form-floating">
          <input
            type="password"
            onChange={handleChangePassword}
            class="form-control"
            id="floatingPassword"
          />
          <label for="floatingPassword">Password</label>
        </div>

        <button
          class="w-100 btn btn-lg btn-primary"
          onClick={handleOnSubmit}
          type="submit"
        >
          Sign in
        </button>
        <p class="mt-5 mb-3 text-muted">&copy; 2017–2021</p>
      </form>
    </div>
  );
};

export default Login;
