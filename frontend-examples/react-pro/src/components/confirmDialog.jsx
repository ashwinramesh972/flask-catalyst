import Swal from 'sweetalert2';

const confirmDialog = (title, text, onConfirm) => {
  Swal.fire({
    title: title || 'Are you sure?',
    text: text || "This action cannot be undone!",
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Yes, do it!'
  }).then((result) => {
    if (result.isConfirmed) {
      onConfirm();
    }
  });
};

export default confirmDialog;