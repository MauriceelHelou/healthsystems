/**
 * EvidenceModal - Modal displaying detailed evidence and citations for a mechanism
 */

import React from 'react';
import { Icon } from '../base/Icon';
import { Badge } from '../base/Badge';
import { EvidenceBadge } from './EvidenceBadge';
import type { Mechanism, Citation } from '../../types/mechanism';

interface EvidenceModalProps {
  mechanism: Mechanism;
  onClose: () => void;
}

export const EvidenceModal: React.FC<EvidenceModalProps> = ({ mechanism, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="flex min-h-full items-center justify-center p-4">
        <div className="relative bg-white rounded-xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Icon name="book-open" size="md" className="text-primary-600" />
              <h2 className="text-lg font-semibold text-gray-900">Evidence & Citations</h2>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <Icon name="x" size="md" className="text-gray-500" />
            </button>
          </div>

          {/* Content */}
          <div className="overflow-y-auto max-h-[calc(90vh-80px)] p-6 space-y-6">
            {/* Mechanism Info */}
            <div className="bg-gray-50 rounded-lg p-4 space-y-3">
              <h3 className="font-semibold text-gray-900">{mechanism.name}</h3>
              <div className="flex items-center gap-3 flex-wrap">
                <Badge color={mechanism.direction === 'positive' ? 'success' : 'error'} size="sm">
                  {mechanism.direction === 'positive' ? 'Positive (+)' : 'Negative (-)'}
                </Badge>
                {mechanism.evidence_quality && (
                  <EvidenceBadge quality={mechanism.evidence_quality} size="md" showLabel />
                )}
                {mechanism.n_studies && (
                  <Badge color="gray" size="sm">
                    {mechanism.n_studies} studies
                  </Badge>
                )}
              </div>
              {mechanism.description && (
                <p className="text-sm text-gray-700 leading-relaxed">{mechanism.description}</p>
              )}
            </div>

            {/* Mechanism Pathway */}
            {mechanism.mechanism_pathway && mechanism.mechanism_pathway.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3">Mechanism Pathway</h3>
                <div className="bg-blue-50 rounded-lg p-4">
                  <ol className="list-decimal list-inside space-y-2 text-sm text-gray-700">
                    {mechanism.mechanism_pathway.map((step, idx) => (
                      <li key={idx} className="leading-relaxed">{step}</li>
                    ))}
                  </ol>
                </div>
              </div>
            )}

            {/* Citations */}
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3">
                Citations ({mechanism.citations?.length || 0})
              </h3>
              {mechanism.citations && mechanism.citations.length > 0 ? (
                <div className="space-y-4">
                  {mechanism.citations.map((citation: Citation, idx: number) => (
                    <CitationCard key={citation.id || idx} citation={citation} isPrimary={idx === 0} />
                  ))}
                </div>
              ) : (
                <p className="text-sm text-gray-500 italic">No citations available.</p>
              )}
            </div>

            {/* Moderators */}
            {mechanism.moderators && mechanism.moderators.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3">Moderating Factors</h3>
                <div className="space-y-3">
                  {mechanism.moderators.map((mod, idx) => (
                    <div key={idx} className="border border-gray-200 rounded-lg p-3">
                      <div className="flex items-center gap-2 mb-2">
                        <Badge color="primary" size="sm">{mod.type}</Badge>
                      </div>
                      <p className="text-sm text-gray-700">{mod.description}</p>
                      {mod.effect && (
                        <p className="text-sm text-gray-600 mt-1">
                          <span className="font-medium">Effect:</span> {mod.effect}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// Citation Card Component
const CitationCard: React.FC<{ citation: Citation; isPrimary?: boolean }> = ({
  citation,
  isPrimary = false,
}) => {
  return (
    <div
      className={`border-2 rounded-lg p-4 space-y-2 ${
        isPrimary ? 'border-primary-300 bg-primary-50' : 'border-gray-200 bg-white'
      }`}
    >
      {isPrimary && (
        <Badge color="primary" size="sm">Primary Citation</Badge>
      )}
      <p className="font-semibold text-gray-900">
        {citation.authors} ({citation.year})
      </p>
      <p className="text-gray-900 font-medium leading-snug">{citation.title}</p>
      <p className="text-gray-600 italic text-sm">{citation.journal}</p>
      {citation.doi && (
        <p className="text-xs text-gray-500">DOI: {citation.doi}</p>
      )}
      {citation.url && (
        <a
          href={citation.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-primary-600 hover:text-primary-700 font-medium text-sm"
        >
          View Publication
          <Icon name="external-link" size="xs" />
        </a>
      )}
    </div>
  );
};

export default EvidenceModal;
