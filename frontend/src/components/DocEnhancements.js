import React, { useEffect } from 'react';
import { useLocation } from '@docusaurus/router';
import TranslateButton from './TranslateButton';
import PersonalizeButton from './PersonalizeButton';

const DocEnhancements = () => {
  const location = useLocation();

  // Only show on doc pages
  const isDocPage = location.pathname.includes('/docs/');

  if (!isDocPage) {
    return null;
  }

  return (
    <div style={{
      position: 'sticky',
      top: '20px',
      display: 'flex',
      gap: '12px',
      marginBottom: '20px',
      justifyContent: 'flex-end'
    }}>
      <PersonalizeButton />
      <TranslateButton />
    </div>
  );
};

export default DocEnhancements;