export const loadUser = (data) => {
  return {
    type: "USER_LOADED",
    payload: data,
  };
};
export const signup = (data) => {
  return {
    type: "REGISTER",
    payload: {
      token: data.token,
      user: data.user,
    },
  };
};
export const login = (data) => {
  return {
    type: "LOGIN",
    payload: {
      token: data.token,
      user: data.user,
    },
  };
};
export const logout = () => {
  return {
    type: "LOGOUT_SUCCESS",
  };
};
