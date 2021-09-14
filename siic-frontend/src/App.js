import { useDispatch } from "react-redux";
import "./App.css";
import { BrowserRouter as Router, Route } from "react-router-dom";
import PrivateRoute from "./Auth/PrivateRoute";
import { loadUser } from "./flux/actions/authAction";
import axios from "axios";
import Routes from "./Routes/Routes";

function App() {
  // const token = useSelector((state) => state.auth.token);
  const token = localStorage.getItem("token");
  const dispatch = useDispatch();
  const config = {
    headers: {
      "Content-type": "application/json",
    },
  };
  if (token) {
    config.headers["x-auth-token"] = token;
  }
  // get user through token if no token then through a error
  axios
    .get("url/getUser", config)
    .then((res) => dispatch(loadUser(res.data)))
    .catch((err) => {
      console.log(err);
      dispatch({
        type: "AUTH_ERROR",
      });
    });

  return (
    <div>
      <Router>
        <div className="App">
          {Routes.map((route) =>
            route.private === true ? (
              <PrivateRoute
                path={route.path}
                exact
                component={route.component}
              />
            ) : (
              <Route path={route.path} exact component={route.component} />
            )
          )}
        </div>
      </Router>
    </div>
  );
}

export default App;
