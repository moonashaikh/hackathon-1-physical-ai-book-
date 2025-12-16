import React, { useState, useEffect } from 'react';
import chatbotAPIClient from '../services/chatbot_api';
import styles from './VectorDBDisplay.module.css';

const VectorDBDisplay = () => {
  const [dbInfo, setDbInfo] = useState(null);
  const [points, setPoints] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(0);
  const [itemsPerPage] = useState(10);

  // Fetch vector database info
  const fetchDbInfo = async () => {
    try {
      setLoading(true);
      const info = await chatbotAPIClient.getVectorDbInfo();
      setDbInfo(info);
      setError(null);
    } catch (err) {
      setError('Failed to fetch vector database info: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  // Fetch vector database points
  const fetchDbPoints = async (skip = 0) => {
    try {
      setLoading(true);
      const response = await chatbotAPIClient.getVectorDbPoints(skip, itemsPerPage);
      setPoints(response.points || []);
      setError(null);
    } catch (err) {
      setError('Failed to fetch vector database points: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDbInfo();
    fetchDbPoints(currentPage * itemsPerPage);
  }, [currentPage]);

  const handlePageChange = (newPage) => {
    if (newPage >= 0) {
      setCurrentPage(newPage);
      fetchDbPoints(newPage * itemsPerPage);
    }
  };

  const handleRefresh = () => {
    fetchDbInfo();
    fetchDbPoints(currentPage * itemsPerPage);
  };

  if (loading && !dbInfo) {
    return (
      <div className={styles.container}>
        <div className={styles.header}>
          <h2>Vector Database Information</h2>
          <button onClick={handleRefresh} className={styles.refreshButton}>
            Refresh
          </button>
        </div>
        <div className={styles.loading}>Loading vector database information...</div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h2>Vector Database Information</h2>
        <button onClick={handleRefresh} className={styles.refreshButton}>
          Refresh
        </button>
      </div>

      {error && (
        <div className={styles.error}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {/* Database Info Summary */}
      <div className={styles.infoCard}>
        <h3>Collection Information</h3>
        <div className={styles.infoGrid}>
          <div className={styles.infoItem}>
            <span className={styles.label}>Collection Name:</span>
            <span className={styles.value}>{dbInfo?.collection_name || 'N/A'}</span>
          </div>
          <div className={styles.infoItem}>
            <span className={styles.label}>Total Vectors:</span>
            <span className={styles.value}>{dbInfo?.vectors_count || 0}</span>
          </div>
          <div className={styles.infoItem}>
            <span className={styles.label}>Indexed Vectors:</span>
            <span className={styles.value}>{dbInfo?.indexed_vectors_count || 0}</span>
          </div>
          <div className={styles.infoItem}>
            <span className={styles.label}>Status:</span>
            <span className={`${styles.value} ${dbInfo?.error ? styles.errorStatus : styles.successStatus}`}>
              {dbInfo?.error ? 'Disconnected' : 'Connected'}
            </span>
          </div>
          {dbInfo?.config && (
            <>
              <div className={styles.infoItem}>
                <span className={styles.label}>Vector Size:</span>
                <span className={styles.value}>{dbInfo.config.vector_size || 'N/A'}</span>
              </div>
              <div className={styles.infoItem}>
                <span className={styles.label}>Distance:</span>
                <span className={styles.value}>{dbInfo.config.distance || 'N/A'}</span>
              </div>
            </>
          )}
        </div>
        {dbInfo?.error && (
          <div className={styles.connectionError}>
            <strong>Connection Error:</strong> {dbInfo.error}
          </div>
        )}
      </div>

      {/* Sample Data */}
      {dbInfo?.samples && dbInfo.samples.length > 0 && (
        <div className={styles.samplesCard}>
          <h3>Sample Vectors</h3>
          <div className={styles.samplesList}>
            {dbInfo.samples.map((sample, index) => (
              <div key={index} className={styles.sampleItem}>
                <div className={styles.sampleHeader}>
                  <strong>ID:</strong> {sample.id}
                </div>
                <div className={styles.sampleMetadata}>
                  <div><strong>Title:</strong> {sample.title}</div>
                  <div><strong>Chapter ID:</strong> {sample.chapter_id}</div>
                </div>
                <div className={styles.sampleContent}>
                  <strong>Content Preview:</strong> {sample.content_preview}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Points List */}
      <div className={styles.pointsCard}>
        <h3>Vector Database Points</h3>
        {loading ? (
          <div className={styles.loading}>Loading points...</div>
        ) : (
          <>
            <div className={styles.pointsList}>
              {points.length > 0 ? (
                points.map((point, index) => (
                  <div key={point.id || index} className={styles.pointItem}>
                    <div className={styles.pointHeader}>
                      <div><strong>ID:</strong> {point.id}</div>
                      {point.score && <div><strong>Score:</strong> {point.score.toFixed(4)}</div>}
                    </div>
                    <div className={styles.pointMetadata}>
                      <div><strong>Title:</strong> {point.title}</div>
                      <div><strong>Chapter ID:</strong> {point.chapter_id}</div>
                    </div>
                    <div className={styles.pointContent}>
                      <strong>Content Preview:</strong> {point.content_preview}
                    </div>
                  </div>
                ))
              ) : (
                <div className={styles.noData}>No points available in the database</div>
              )}
            </div>

            {/* Pagination */}
            <div className={styles.pagination}>
              <button
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={currentPage === 0}
                className={styles.pageButton}
              >
                Previous
              </button>
              <span className={styles.pageInfo}>
                Page {currentPage + 1}
              </span>
              <button
                onClick={() => handlePageChange(currentPage + 1)}
                className={styles.pageButton}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default VectorDBDisplay;