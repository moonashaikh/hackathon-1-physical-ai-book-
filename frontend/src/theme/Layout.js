import React from 'react';
import OriginalLayout from '@theme-original/Layout';
import DocEnhancements from '../components/DocEnhancements';
import Chatbot from '../components/Chatbot';
import { useLocation } from '@docusaurus/router';


export default function Layout(props) {
  const location = useLocation();
  const isDocPage = location.pathname.includes('/docs/');

  return (
    <>
      <OriginalLayout {...props} />
      {isDocPage && <DocEnhancements />}
      <Chatbot />
    </>
  );
}