import React from 'react';
import Layout from '@theme/Layout';
import SignupForm from '../components/SignupForm';

function SignupPage() {
  return (
    <Layout title="Sign Up" description="Create your account">
      <div style={{ padding: '2rem' }}>
        <div className="container">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <SignupForm />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default SignupPage;