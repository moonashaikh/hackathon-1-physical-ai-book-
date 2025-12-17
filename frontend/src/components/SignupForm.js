import React, { useState } from 'react';
import Link from '@docusaurus/Link';
import styles from './AuthForm.module.css';
import { signUpWithBackground } from '../services/auth_client';

const SignupForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    softwareBackground: '',
    hardwareBackground: '',
    primaryInterest: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Prepare background data for Better Auth
      const backgroundData = {
        software_background: formData.softwareBackground,
        hardware_background: formData.hardwareBackground,
        primary_interest: formData.primaryInterest
      };

      const result = await signUpWithBackground(
        formData.email,
        formData.password,
        backgroundData
      );

      if (result && result.session) {
        // Store the token in localStorage (for compatibility with existing code)
        localStorage.setItem('access_token', result.session.token);
        // Redirect to textbook intro page after successful signup
        window.location.href = '/docs/intro';
      } else {
        setError(result?.error?.message || 'Signup failed');
      }
    } catch (err) {
      setError(err?.error?.message || 'An error occurred during signup');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.authContainer}>
      <div className={styles.authForm}>
        <h2>Create Account</h2>
        {error && <div className={styles.errorMessage}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div className={styles.formGroup}>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="softwareBackground">Software Background:</label>
            <select
              id="softwareBackground"
              name="softwareBackground"
              value={formData.softwareBackground}
              onChange={handleChange}
              required
            >
              <option value="">Select your software background</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="hardwareBackground">Hardware Background:</label>
            <select
              id="hardwareBackground"
              name="hardwareBackground"
              value={formData.hardwareBackground}
              onChange={handleChange}
              required
            >
              <option value="">Select your hardware background</option>
              <option value="none">None</option>
              <option value="basic electronics">Basic Electronics</option>
              <option value="robotics">Robotics</option>
              <option value="embedded systems">Embedded Systems</option>
            </select>
          </div>

          <div className={styles.formGroup}>
            <label htmlFor="primaryInterest">Primary Interest:</label>
            <select
              id="primaryInterest"
              name="primaryInterest"
              value={formData.primaryInterest}
              onChange={handleChange}
              required
            >
              <option value="">Select your primary interest</option>
              <option value="AI">AI</option>
              <option value="Robotics">Robotics</option>
              <option value="Web">Web</option>
              <option value="Hardware">Hardware</option>
              <option value="Mixed">Mixed</option>
            </select>
          </div>

          <button type="submit" disabled={loading} className={styles.submitButton}>
            {loading ? 'Creating Account...' : 'Sign Up'}
          </button>
        </form>

        <div className={styles.authLinks}>
          <p>Already have an account? <Link to="/signin">Sign in</Link></p>
        </div>
      </div>
    </div>
  );
};

export default SignupForm;