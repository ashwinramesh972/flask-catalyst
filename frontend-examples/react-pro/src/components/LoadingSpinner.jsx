import React from 'react';
import { CSpinner } from '@coreui/react';

const LoadingSpinner = ({ size = 'md', fullScreen = false }) => {
  const spinner = (
    <div className="d-flex justify-content-center align-items-center" style={{ minHeight: '200px' }}>
      <CSpinner color="primary" size={size} />
    </div>
  );

  if (fullScreen) {
    return (
      <div className="position-fixed top-0 start-0 w-100 h-100 d-flex justify-content-center align-items-center bg-white bg-opacity-75" style={{ zIndex: 9999 }}>
        {spinner}
      </div>
    );
  }

  return spinner;
};

export default LoadingSpinner;