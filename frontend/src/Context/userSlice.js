import { createSlice } from "@reduxjs/toolkit";

const StoredUser = sessionStorage.getItem("user")
  ? JSON.parse(sessionStorage.getItem("user"))
  : null;

const userSlice = createSlice({
  name: "user",
  initialState: {
    user: StoredUser,
  },
  reducers: {
    login: (state, action) => {
      state.user = action.payload;
      sessionStorage.setItem("user", JSON.stringify(action.payload)); // ✅
    },
    logout: (state) => {
      state.user = null;
      sessionStorage.removeItem("user");
    },
  },
});

export const { login, logout } = userSlice.actions;
export default userSlice.reducer;
