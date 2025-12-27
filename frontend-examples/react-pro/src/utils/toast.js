import toast from 'react-hot-toast';

const successToast = (message) => {
  toast.success(message, {
    duration: 4000,
    position: 'top-right',
  });
};

const errorToast = (message) => {
  toast.error(message || "An error occurred", {
    duration: 5000,
    position: 'top-right',
  });
};

const loadingToast = (message) => {
  return toast.loading(message, {
    position: 'top-right',
  });
};

// Optional: update a loading toast
export const updateToast = (toastId, type, message) => {
  toast.dismiss(toastId);
  if (type === 'success') toast.success(message);
  if (type === 'error') toast.error(message);
};

export { successToast, errorToast, loadingToast };