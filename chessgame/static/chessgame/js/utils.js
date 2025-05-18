// utils.js
export function getCSRFToken() {
  let csrfToken = null;

  // First, try to get the token from the cookie
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim();
    if (cookie.startsWith("csrftoken=")) {
      csrfToken = cookie.substring("csrftoken=".length, cookie.length);
      break;
    }
  }

  // If not found in cookie, look for it in the DOM
  if (!csrfToken) {
    const tokenElement = document.querySelector("[name=csrfmiddlewaretoken]");
    if (tokenElement) {
      csrfToken = tokenElement.value;
    }
  }

  return csrfToken;
}
