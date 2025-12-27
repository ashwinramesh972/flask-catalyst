import { useState, useEffect } from 'react';
import api from '../services/api';
import { successToast, errorToast } from './toast';

export const useFetch = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get(url, options);
        setData(response.data);
        successToast("Data loaded");
      } catch (err) {
        const msg = err.response?.data?.message || 'Failed to load data';
        setError(msg);
        errorToast(msg);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]);

  return { data, loading, error, refetch: () => fetchData() };
};