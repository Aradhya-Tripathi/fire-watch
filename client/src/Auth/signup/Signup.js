import React, { useState } from "react";
import axios from "axios";
import { signup } from "../../flux/actions/authAction";
import { useSelector, useDispatch } from "react-redux";
import "./Signup.css";
import { Redirect } from "react-router";

function Signup() {
  const dispatch = useDispatch();
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [auth, setAuth] = useState(false);
  const handleChangeName = (e) => setName(e.target.value);
  const handleChangeEmail = (e) => setEmail(e.target.value);
  const handleChangePassword = (e) => setPassword(e.target.value);

  const handleOnSubmit = (e) => {
    e.preventDefault();
    const user = {
      name,
      email,
      password,
    };
    const body = JSON.stringify(user);
    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    axios
      .post("url/signup", body, config)
      .then((res) => {
        dispatch(signup(res.data));
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
    //   user: user,
    // };
    // dispatch(signup(data));
  };
  const authenticated = useSelector((state) => state.auth.isAuthenticated);
  if (auth || authenticated) {
    return <Redirect to="/dashboard" />;
  }
  //code for the signup here
  return (
    <div>
      <form>
        <h1 class="h3 mb-3 fw-normal">Please sign up</h1>

        <div class="form-floating">
          <input
            type="text"
            onChange={handleChangeName}
            class="form-control"
            id="floatingInput"
          />
          <label for="floatingInput">Name</label>
        </div>

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
          Sign up
        </button>
        <p class="mt-5 mb-3 text-muted">&copy; 2017–2021</p>
      </form>
    </div>
  );
}

export default Signup;
