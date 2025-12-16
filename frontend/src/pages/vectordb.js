import React from 'react';
import Layout from '@theme/Layout';
import VectorDBDisplay from '../components/VectorDBDisplay';

export default function VectorDBPage() {
  return (
    <Layout title="Vector Database Display" description="View and manage the vector database for the RAG system">
      <div style={{ padding: '2rem' }}>
        <div className="container">
          <h1>Vector Database Display</h1>
          <p>This page shows information about the vector database used in the RAG (Retrieval Augmented Generation) system.</p>
          <VectorDBDisplay />
        </div>
      </div>
    </Layout>
  );
}