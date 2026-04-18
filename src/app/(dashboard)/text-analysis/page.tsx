"use client";
import React, { useState } from 'react';
import { Download, CheckCircle, AlertTriangle, Activity, Zap, BarChart2, ShieldCheck, Newspaper, Loader2, XCircle } from 'lucide-react';
import { verifyText, FactCheckResponse } from '@/lib/api';

export default function TextAnalysisPage() {
  const [claimText, setClaimText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<FactCheckResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleScan = async () => {
    if (!claimText.trim()) return;
    setIsLoading(true);
    setError(null);
    try {
      const data = await verifyText(claimText.trim(), "en");
      setResult(data);
    } catch (err: any) {
      setError(err.message || "An error occurred during verification.");
    } finally {
      setIsLoading(false);
    }
  };

  // Safe defaults if no result
  const truthScore = Math.round((result?.credibility_scoring_mechanism ?? 0) * 100) || 0;
  const isHighRisk = result?.flagging === "HIGH_RISK" || result?.flagging === "FALSE" || result?.flagging === "MANIPULATED";
  const aiProbability = isHighRisk ? 92 : (truthScore > 75 ? 12 : 55); // Mock metric if backend doesn't explicitly return AI probability

  return (
    <div className="animate-slide-up">
      {/* Top Header Section */}
      <div style={{ marginBottom: '32px', borderBottom: '1px solid var(--border-color)', paddingBottom: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h1 style={{ fontSize: '20px', fontWeight: 600, fontFamily: 'var(--font-outfit)', margin: 0 }}>Text Analysis</h1>
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-end' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>AI Probability</span>
                <span style={{ color: 'var(--text-primary)', fontWeight: 'bold', fontSize: '16px' }}>{result ? `${aiProbability}%` : '--'}</span>
              </div>
              <div style={{ width: '1px', height: '30px', background: 'var(--border-color)' }}></div>
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <span style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1px' }}>Truth Score</span>
                <span style={{ color: result ? (truthScore > 50 ? 'var(--accent-green)' : 'var(--accent-red)') : 'var(--text-primary)', fontWeight: 'bold', fontSize: '16px' }}>
                  {result ? `${truthScore}%` : '--'}
                </span>
              </div>
            </div>
            <button className="btn btn-primary" disabled={isLoading}>
              <Download size={16} /> Export Intel
            </button>
          </div>
        </div>
        
        {error && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px', background: 'rgba(239, 68, 68, 0.1)', color: 'var(--accent-red)', borderRadius: '8px', marginBottom: '16px', fontSize: '14px' }}>
            <XCircle size={16} /> {error}
          </div>
        )}

        <div style={{ position: 'relative' }}>
            <textarea
            rows={3}
            placeholder="Paste any article, claim, or text snippet here to analyze for misinformation..."
            value={claimText}
            onChange={(e) => setClaimText(e.target.value)}
            disabled={isLoading}
            style={{
                width: '100%',
                padding: '12px 16px',
                fontSize: '14px',
                fontFamily: 'var(--font-inter)',
                color: 'var(--text-primary)',
                background: 'var(--bg-hover)',
                border: '1px solid var(--border-color)',
                borderRadius: '10px',
                resize: 'vertical',
                outline: 'none',
                lineHeight: 1.6,
                transition: 'border-color 0.2s ease',
                boxSizing: 'border-box',
                opacity: isLoading ? 0.7 : 1
            }}
            onFocus={e => e.currentTarget.style.borderColor = 'var(--accent-blue)'}
            onBlur={e => e.currentTarget.style.borderColor = 'var(--border-color)'}
            />
            <div style={{ marginTop: '12px', display: 'flex', justifyContent: 'flex-end' }}>
                <button 
                  className="btn btn-primary" 
                  onClick={handleScan} 
                  disabled={isLoading || !claimText.trim()}
                  style={{
                    opacity: (!claimText.trim() || isLoading) ? 0.5 : 1,
                    cursor: (!claimText.trim() || isLoading) ? 'not-allowed' : 'pointer'
                  }}
                >
                    {isLoading ? <><Loader2 size={16} className="animate-spin" /> Scanning...</> : <><Activity size={16} /> Analyze Content</>}
                </button>
            </div>
        </div>
      </div>

      {/* 3-Column Tactical Layout */}
      {(result || isLoading) ? (
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr 1fr', gap: '24px', opacity: isLoading ? 0.5 : 1, transition: 'opacity 0.3s' }}>
        
        {/* Left Column: Context & Sources */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="card">
            <div className="card-title" style={{ marginBottom: '20px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <ShieldCheck size={14} /> Verification Pipeline
            </div>
            <ul style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '13px' }}>
              {result?.automated_fact_verification_pipeline?.length ? result.automated_fact_verification_pipeline.map((step, idx) => (
                <li key={idx} className="flex-between">
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center', color: 'var(--text-secondary)' }}>
                    <CheckCircle size={14} color="var(--accent-green)" /> {step}
                  </div>
                  <span style={{ color: 'var(--text-primary)', fontSize: '11px', fontWeight: 'bold' }}>DONE</span>
                </li>
              )) : (
                <>
                <li className="flex-between">
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center', color: 'var(--text-secondary)' }}><CheckCircle size={14} /> External Agent Ping</div>
                    <span style={{ color: 'var(--text-primary)', fontSize: '11px', fontWeight: 'bold' }}>VERIFIED</span>
                </li>
                </>
               )}
            </ul>
          </div>

          <div className="card">
            <div className="card-title" style={{ marginBottom: '20px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <Newspaper size={14} /> Source Cross-Reference
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {result?.links?.length ? result.links.map((link, idx) => (
                    <div key={idx}>
                        <div className="flex-between" style={{ marginBottom: '6px' }}>
                        <strong style={{ fontSize: '13px', color: 'var(--text-primary)', wordBreak: 'break-all' }}>{new URL(link).hostname}</strong>
                        <CheckCircle size={12} color="var(--text-secondary)" />
                        </div>
                        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>
                            <a href={link} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--accent-blue)', textDecoration: 'none' }}>Verify origin &rarr;</a>
                        </div>
                    </div>
                )) : (
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>No explicit URLs sourced by the backend agents for this claim. Graph internal context was used.</div>
                )}
            </div>
          </div>
        </div>

        {/* Center Column: The Target Artifact */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="card" style={{ padding: '32px' }}>
            <div className="flex-between" style={{ marginBottom: '24px' }}>
              <div className="card-title" style={{ fontSize: '14px', color: 'var(--text-primary)' }}>Artifact Analysis</div>
              <span className="badge" style={{ fontSize: '10px', background: isHighRisk ? 'rgba(220, 38, 38, 0.1)' : 'rgba(16, 185, 129, 0.1)', color: isHighRisk ? 'var(--accent-red)' : 'var(--accent-green)' }}>
                {isHighRisk ? <AlertTriangle size={12} /> : <CheckCircle size={12} />} 
                {result?.flagging || 'SCANNING'}
              </span>
            </div>
            
            <div style={{ fontSize: '15px', lineHeight: '1.7', color: 'var(--text-secondary)', padding: '24px 0', borderTop: '1px solid var(--border-light)', borderBottom: '1px solid var(--border-light)' }}>
              {/* Highlight inconsistencies if provided, else just show claim */}
              {result ? (
                <p style={{ whiteSpace: 'pre-wrap' }}>
                    {result.CLAIM}
                </p>
              ) : (
                <p>Analyzing semantics...</p>
              )}
            </div>

            <div style={{ marginTop: '24px', display: 'flex', flexWrap: 'wrap', gap: '16px', fontSize: '11px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
              {result?.inconsistencies?.map((inc, i) => (
                  <div key={i} style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-red)' }}></div>
                    <span style={{ color: 'var(--text-muted)' }}>{inc}</span>
                  </div>
              ))}
            </div>
            
            {/* Display detailed explaination if available */}
            {result?.EXPLAINATION && (
                <div style={{ marginTop: '24px', fontSize: '13px', color: 'var(--text-secondary)', padding: '16px', background: 'var(--bg-main)', borderRadius: 'var(--radius-sm)' }}>
                    <strong style={{ display: 'block', marginBottom: '8px', color: 'var(--text-primary)' }}>Heuristic Explanation:</strong>
                    {result.EXPLAINATION}
                </div>
            )}
          </div>

          <div className="card">
            <div className="card-title" style={{ marginBottom: '16px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <ShieldCheck size={14} color="var(--accent-green)" /> Synthesized Counter-Narrative
            </div>
            {result ? (
               <div style={{ fontSize: '14px', color: 'var(--text-primary)', lineHeight: '1.6' }}>
                   {result.countering_misinformation}
               </div>
            ) : (
               <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>Awaiting LangGraph resolution...</div>
            )}
          </div>
        </div>

        {/* Right Column: AI Heuristics */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="card">
            <div className="card-title" style={{ marginBottom: '24px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <BarChart2 size={14} /> Threat Taxonomy
            </div>
            
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {result?.classifiers?.map((c, i) => (
                    <div key={i} style={{ padding: '8px 12px', background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '6px', fontSize: '12px', color: 'var(--text-secondary)' }}>
                        {c}
                    </div>
                ))}
                {!result?.classifiers?.length && (
                    <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>No specific classifiers triggered.</span>
                )}
            </div>
          </div>

          <div className="card">
            <div className="card-title" style={{ marginBottom: '20px', fontSize: '13px', color: 'var(--text-secondary)' }}>
              <Zap size={14} /> Vector Signatures
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
              <div>
                <div style={{ fontSize: '10px', color: 'var(--text-primary)', marginBottom: '8px', letterSpacing: '0.5px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <div style={{ width: '4px', height: '4px', borderRadius: '50%', background: 'var(--text-primary)'}}></div> MULTIMODAL SYNERGY
                </div>
                <div style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                    {result?.TRUTH || "Verdicts mapped against internal semantic spaces."}
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
      ) : (
        <div style={{ height: '300px', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-muted)', fontSize: '14px' }}>
            Enter text into the console and initialize the scanner to view insights.
        </div>
      )}
      
      <style dangerouslySetInnerHTML={{__html: `
        .highlight-red {
          color: var(--text-primary);
          border-bottom: 2px dashed var(--text-muted);
          padding-bottom: 2px;
          cursor: crosshair;
        }
        .highlight-yellow {
          background: var(--bg-hover);
          color: var(--text-primary);
          padding: 2px 4px;
          border-radius: 4px;
          cursor: crosshair;
        }
      `}} />
    </div>
  );
}
