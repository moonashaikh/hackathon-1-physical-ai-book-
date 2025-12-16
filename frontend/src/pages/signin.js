import React from 'react';
import Layout from '@theme/Layout';
import SigninForm from '../components/SigninForm';

function SigninPage() {
  return (
    <Layout title="Sign In" description="Sign in to your account">
      <div style={{ padding: '2rem' }}>
        <div className="container">
          <div className="row">
            <div className="col col--6 col--offset-3">
              <SigninForm />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default SigninPage;