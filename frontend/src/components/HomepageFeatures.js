import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Physical AI',
    // Svg: require('../../static/img/robot-arm.svg').default, // Placeholder for actual SVG
    description: (
      <>
        Learn about the fundamentals of Physical AI and how it bridges the gap between perception and action in robotics.
      </>
    ),
  },
  {
    title: 'Humanoid Robotics',
    // Svg: require('../../static/img/humanoid-robot.svg').default, // Placeholder for actual SVG
    description: (
      <>
        Explore the principles of humanoid robotics, from kinematics to control systems.
      </>
    ),
  },
  {
    title: 'RAG-Powered Learning',
    // Svg: require('../../static/img/ai-chatbot.svg').default, // Placeholder for actual SVG
    description: (
      <>
        Interact with our AI-powered textbook through our integrated RAG chatbot for personalized learning experiences.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}