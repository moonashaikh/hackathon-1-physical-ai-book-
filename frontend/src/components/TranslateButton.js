import React, { useState } from 'react';
import styles from './TranslateButton.module.css';

const TranslateButton = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [selectedLanguage, setSelectedLanguage] = useState('ur');

  const handleTranslate = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleApplyTranslation = () => {
    // In a real implementation, this would trigger the translation process
    console.log(`Translating to ${selectedLanguage}`);
    setIsModalOpen(false);
  };

  return (
    <div className={styles.translateContainer}>
      <button
        onClick={handleTranslate}
        className={styles.translateButton}
        title="Translate Chapter to Urdu"
      >
        🌐 Urdu
      </button>

      {isModalOpen && (
        <div className={styles.modalOverlay}>
          <div className={styles.modalContent}>
            <div className={styles.modalHeader}>
              <h3>Translate Chapter</h3>
              <button
                onClick={handleCloseModal}
                className={styles.closeButton}
                aria-label="Close"
              >
                ×
              </button>
            </div>

            <div className={styles.modalBody}>
              <div className={styles.languageSelector}>
                <label>Select Language:</label>
                <select
                  value={selectedLanguage}
                  onChange={(e) => setSelectedLanguage(e.target.value)}
                  className={styles.languageDropdown}
                >
                  <option value="ur">Urdu</option>
                  <option value="es">Spanish</option>
                  <option value="fr">French</option>
                  <option value="de">German</option>
                  <option value="zh">Chinese</option>
                </select>
              </div>

              <div className={styles.translationOptions}>
                <p>Translation options:</p>
                <label>
                  <input
                    type="checkbox"
                    defaultChecked
                  />
                  Translate main content
                </label>
                <label>
                  <input
                    type="checkbox"
                    defaultChecked
                  />
                  Translate code comments
                </label>
                <label>
                  <input
                    type="checkbox"
                  />
                  Translate technical terms (glossary)
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
                onClick={handleApplyTranslation}
                className={styles.translateButton}
              >
                Translate
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default TranslateButton;