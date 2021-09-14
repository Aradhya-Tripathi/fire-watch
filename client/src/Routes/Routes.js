import Login from "../Auth/login/Login";
import Signup from "../Auth/signup/Signup";
import Dashboard from "../Dashboard/Dashboard";

const routes = [
  {
    path: "/login",
    component: Login,
    private: false,
  },
  {
    path: "/signup",
    component: Signup,
    private: false,
  },
  {
    path: "/",
    component: Dashboard,
    private: false, //for now
  },
];
export default routes;
