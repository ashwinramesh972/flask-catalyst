import axios from "axios";

const BASE_URL = import.meta.env.VITE_APP_BASE_URL || "http://localhost:5000/api";

let showSessionExpiredModal = () => {};

export const setSessionExpiredModalHandler = (handler) => {
  showSessionExpiredModal = handler;
};

const cleanUrl = (baseUrl, endpoint) => {
  const cleanedBaseUrl = baseUrl.replace(/\/$/, '');
  const cleanedEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  return `${cleanedBaseUrl}${cleanedEndpoint}`;
};

const getAuthToken = () => localStorage.getItem('access_token');

const axiosInstance = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
});

axiosInstance.interceptors.request.use(config => {
  const token = getAuthToken();
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  // CRITICAL FIX: Remove Content-Type for methods that don't have body
  if (['get', 'delete', 'head', 'options'].includes(config.method.toLowerCase())) {
    delete config.headers['Content-Type'];
  }

  return config;
}, error => {
  return Promise.reject(error);
});

const handleApiError = (error) => {
  if (error?.response?.data?.error === "Signature has expired" || 
      error?.response?.data?.error === "Token has been revoked") {
    showSessionExpiredModal();
  }
  throw error;
};

export const getRequest = async (endpoint, config = {}) => {
  try {
    const url = cleanUrl(BASE_URL, endpoint);
    const response = await axiosInstance.get(url, config);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export const postRequest = async (endpoint, data = {}, config = {}) => {
  try {
    const url = cleanUrl(BASE_URL, endpoint);
    const response = await axiosInstance.post(url, data, config);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export const putRequest = async (endpoint, data = {}, config = {}) => {
  try {
    const url = cleanUrl(BASE_URL, endpoint);
    const response = await axiosInstance.put(url, data, config);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};

export const deleteRequest = async (endpoint, config = {}) => {
  try {
    const url = cleanUrl(BASE_URL, endpoint);
    const response = await axiosInstance.delete(url, config);
    return response.data;
  } catch (error) {
    handleApiError(error);
  }
};