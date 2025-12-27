import React, { useState, useEffect } from 'react';
import {
  CCard,
  CCardBody,
  CCardHeader,
  CButton,
  CForm,
  CFormInput,
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CTableDataCell,
  CSpinner,
  CAlert,
  CFormLabel,
} from '@coreui/react';
import { getRequest, postRequest } from '../../../services/apiServices';
import { successToast, errorToast } from '../../../utils/toast';
import LoadingSpinner from '../../../components/LoadingSpinner';
import confirmDialog from '../../../components/confirmDialog';
import { formatDateTime } from '../../../utils/formatters';

const UtilsDemoPage = () => {
  const [users, setUsers] = useState([]);
  const [pagination, setPagination] = useState({});
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(false);
  const [email, setEmail] = useState('');
  const [file, setFile] = useState(null);
  const [uploadedUrl, setUploadedUrl] = useState('');
  const [rateLimitClicks, setRateLimitClicks] = useState(0);

  const fetchDemo = async (page = 1) => {
    setLoading(true);
    try {
      const res = await getRequest(`/demo/utils-demo?page=${page}&per_page=10`);
      setUsers(res.data.paginated_users.items);
      setPagination(res.data.paginated_users.pagination);
      setCurrentPage(page);
      successToast(`Page ${page} loaded successfully!`);
    } catch (err) {
      errorToast("Failed to load users");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDemo(1);
  }, []);

  const sendTestEmail = async () => {
    if (!email) return errorToast("Please enter an email address");
    setLoading(true);
    try {
      await postRequest('/demo/utils-demo', { email });
      successToast(`Test email sent to ${email}! Check your inbox.`);
      setEmail('');
    } catch (err) {
      errorToast("Email failed — check your .env MAIL settings");
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async () => {
    if (!file) return errorToast("Please select a file");
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    try {
      const res = await postRequest('/demo/utils-demo', formData);
      setUploadedUrl(res.data.uploaded_file_url);
      successToast("File uploaded successfully!");
    } catch (err) {
      errorToast("File upload failed");
    } finally {
      setLoading(false);
    }
  };

  const triggerRateLimit = async () => {
    setRateLimitClicks(prev => prev + 1);
    try {
      await getRequest('/demo/utils-demo');
    } catch (err) {
      if (err.response?.status === 429) {
        errorToast("Rate limit hit! Wait 1 minute.");
      }
    }
  };

  const testConfirm = () => {
    confirmDialog(
      "Confirm Action",
      "This is just a demo — nothing will be deleted.",
      () => successToast("Confirmed! (demo only)")
    );
  };

  return (
    <div className="p-4">
      {loading && <LoadingSpinner fullScreen />}

      <CCard className="mb-4">
        <CCardHeader>
          <h2>flask-catalyst — Ultimate Utils Demo</h2>
          <p>All backend + frontend utilities in one page</p>
        </CCardHeader>
        <CCardBody>
          {/* Paginated Users */}
          <h5>Pagination + Protected Route</h5>
          {users.length > 0 ? (
            <>
              <CTable hover responsive>
                <CTableHead>
                  <CTableRow>
                    <CTableHeaderCell>ID</CTableHeaderCell>
                    <CTableHeaderCell>Username</CTableHeaderCell>
                    <CTableHeaderCell>Email</CTableHeaderCell>
                    <CTableHeaderCell>Role</CTableHeaderCell>
                    <CTableHeaderCell>Created</CTableHeaderCell>
                  </CTableRow>
                </CTableHead>
                <CTableBody>
                  {users.map(user => (
                    <CTableRow key={user.id}>
                      <CTableDataCell>{user.id}</CTableDataCell>
                      <CTableDataCell>{user.username}</CTableDataCell>
                      <CTableDataCell>{user.email}</CTableDataCell>
                      <CTableDataCell>{user.role}</CTableDataCell>
                      <CTableDataCell>{formatDateTime(user.created_at)}</CTableDataCell>
                    </CTableRow>
                  ))}
                </CTableBody>
              </CTable>

              {/* Pagination Controls */}
              <div className="d-flex justify-content-between align-items-center mt-4">
                <div>
                  Page {pagination.page} of {pagination.pages} ({pagination.total} total users)
                </div>
                <div>
                  <CButton
                    disabled={!pagination.has_prev}
                    onClick={() => fetchDemo(pagination.prev_page)}
                    color="secondary"
                    className="me-2"
                  >
                    Previous
                  </CButton>

                  {[...Array(pagination.pages)].map((_, i) => (
                    <CButton
                      key={i + 1}
                      onClick={() => fetchDemo(i + 1)}
                      color={i + 1 === pagination.page ? "primary" : "light"}
                      className="me-1"
                    >
                      {i + 1}
                    </CButton>
                  ))}

                  <CButton
                    disabled={!pagination.has_next}
                    onClick={() => fetchDemo(pagination.next_page)}
                    color="secondary"
                    className="ms-2"
                  >
                    Next
                  </CButton>
                </div>
              </div>
            </>
          ) : (
            <p>No users loaded yet — click below</p>
          )}

          <hr />

          {/* File Upload */}
          <h5>File Upload</h5>
          <CFormInput type="file" onChange={(e) => setFile(e.target.files[0])} className="mb-2" />
          <CButton onClick={handleFileUpload} color="success">
            Upload File
          </CButton>
          {uploadedUrl && (
            <div className="mt-3">
              <strong>Uploaded:</strong>
              <img src={uploadedUrl} alt="uploaded" style={{ maxWidth: '400px', marginTop: '10px' }} />
              <p><small>{uploadedUrl}</small></p>
            </div>
          )}

          <hr />

          {/* Email Test */}
          <h5>Email Test</h5>
          <CAlert color="warning" className="mb-3">
            <strong>Important:</strong> Make sure your <code>.env</code> file has correct MAIL_USERNAME, MAIL_PASSWORD, and MAIL_DEFAULT_SENDER (Gmail app password recommended).
          </CAlert>
          <CFormLabel>Enter your email to receive a test message</CFormLabel>
          <CFormInput
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="you@example.com"
            className="mb-2"
          />
          <CButton onClick={sendTestEmail} color="info">
            Send Test Email
          </CButton>

          <hr />

          {/* Rate Limit Test */}
          <h5>Rate Limit Test</h5>
          <CButton onClick={triggerRateLimit} color="warning">
            Click me fast (limited to 5/min)
          </CButton>
          <p className="mt-2">Clicked {rateLimitClicks} times</p>

          <hr />

          {/* Confirm Dialog Test */}
          <h5>Confirm Dialog Test</h5>
          <CButton onClick={testConfirm} color="danger">
            Trigger Confirm Dialog
          </CButton>

          <hr />

          <CAlert color="success">
            <strong>flask-catalyst v2.0 is complete!</strong><br />
            All utils working: pagination, file upload, email, toast, spinner, confirm dialog, protected route, formatters, rate limiting, logging.
          </CAlert>
        </CCardBody>
      </CCard>
    </div>
  );
};

export default UtilsDemoPage;