import React, { useState } from 'react';
import styles from './PersonalizeButton.module.css';

const PersonalizeButton = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handlePersonalize = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleApplySettings = () => {
    // In a real implementation, this would apply the personalization settings
    console.log('Applying personalization settings');
    setIsModalOpen(false);
  };

  return (
    <div className={styles.personalizeContainer}>
      <button
        onClick={handlePersonalize}
        className={styles.personalizeButton}
        title="Personalize Chapter Content"
      >
        🎯 Personalize
      </button>

      {isModalOpen && (
        <div className={styles.modalOverlay}>
          <div className={styles.modalContent}>
            <div className={styles.modalHeader}>
              <h3>Personalize Chapter Content</h3>
              <button
                onClick={handleCloseModal}
                className={styles.closeButton}
                aria-label="Close"
              >
                ×
              </button>
            </div>

            <div className={styles.modalBody}>
              <div className={styles.optionGroup}>
                <label>
                  <input
                    type="radio"
                    name="complexity"
                    value="beginner"
                    defaultChecked
                  />
                  Beginner-friendly explanations
                </label>
                <label>
                  <input
                    type="radio"
                    name="complexity"
                    value="intermediate"
                  />
                  Intermediate level
                </label>
                <label>
                  <input
                    type="radio"
                    name="complexity"
                    value="advanced"
                  />
                  Advanced technical details
                </label>
              </div>

              <div className={styles.optionGroup}>
                <label>
                  <input
                    type="checkbox"
                    defaultChecked
                  />
                  Include more examples
                </label>
                <label>
                  <input
                    type="checkbox"
                  />
                  Focus on mathematical details
                </label>
                <label>
                  <input
                    type="checkbox"
                  />
                  Emphasize practical applications
                </label>
              </div>
            </div>

            <div className={styles.modalFooter}>
              <button
                onClick={handleCloseModal}
                className={styles.cancelButton}
              >
                Cancel
              </button>
              <button
                onClick={handleApplySettings}
                className={styles.applyButton}
              >
                Apply Settings
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PersonalizeButton;