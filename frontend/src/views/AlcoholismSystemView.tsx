/**
 * AlcoholismSystemView - Dedicated view for the alcoholism causal system
 *
 * Now powered by MetadataDrivenSystemView for flexible focal node exploration.
 */

import React from 'react';
import { MetadataDrivenSystemView } from './MetadataDrivenSystemView';
import type { Category, NodeScale } from '../types/mechanism';

export const AlcoholismSystemView: React.FC = () => {
  return (
    <MetadataDrivenSystemView
      title="Alcoholism System Analysis"
      description="Explore causal pathways related to alcohol use disorder and liver disease"
      domainKeywords={[
        'alcohol',
        'ald',
        'liver',
        'drinking',
        'substance',
        'addiction',
        'hepatitis',
        'cirrhosis',
        'binge',
        'aud'
      ]}
      initialCategories={[
        'economic',
        'behavioral',
        'healthcare_access',
        'biological',
        'social_environment'
      ] as Category[]}
      initialScales={[1, 4, 5, 6, 7] as NodeScale[]} // Focus on policy → conditions → crisis
    />
  );
};

export default AlcoholismSystemView;
