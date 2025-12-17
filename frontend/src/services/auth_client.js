// Custom auth client to work with our Better Auth-compatible endpoints
const API_BASE_URL = "http://localhost:8005/api/better-auth/auth";

// Function to get user session
export const getSession = async () => {
  try {
    const token = localStorage.getItem('access_token');
    if (!token) {
      return null;
    }

    const response = await fetch(`${API_BASE_URL}/get-session`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error getting session:", error);
    return null;
  }
};

// Function to sign up with background information
export const signUpWithBackground = async (email, password, backgroundData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/sign-up`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
        ...backgroundData
      })
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error during signup:", error);
    throw error;
  }
};

// Function to sign in
export const signIn = async (email, password) => {
  try {
    const response = await fetch(`${API_BASE_URL}/sign-in`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password
      })
    });

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error during signin:", error);
    throw error;
  }
};

// Function to sign out
export const signOut = async () => {
  try {
    await fetch(`${API_BASE_URL}/sign-out`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });
    // Clear the stored token
    localStorage.removeItem('access_token');
  } catch (error) {
    console.error("Error during signout:", error);
    throw error;
  }
};