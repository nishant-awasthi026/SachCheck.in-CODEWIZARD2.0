"use client";
import React, { useState, useRef } from 'react';
import { AlertCircle, Mic, Activity, Flag, FileAudio, UploadCloud, Loader2, XCircle, CheckCircle } from 'lucide-react';
import { verifyMultimodal, FactCheckResponse } from '@/lib/api';

export default function AudioSignalPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<FactCheckResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setResult(null);
      setError(null);
    }
  };

  const handleScan = async () => {
    if (!selectedFile) return;
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await verifyMultimodal(selectedFile, "en");
      setResult(data);
    } catch (err: any) {
      setError(err.message || "Failed to process audio.");
    } finally {
      setIsLoading(false);
    }
  };

  const highRisk = result?.flagging === "HIGH_RISK" || result?.flagging === "FALSE" || result?.flagging === "MANIPULATED";
  const authScore = result ? Math.round(result.credibility_scoring_mechanism * 100) : 0;
  const fakeScore = result ? 100 - authScore : 0;

  return (
    <div className="animate-slide-up">
      <div className="flex-between" style={{ marginBottom: "24px" }}>
        <div style={{ color: 'var(--text-secondary)', fontSize: '14px', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <FileAudio size={16} /> File: {selectedFile ? selectedFile.name : 'NO_FILE_SELECTED'}
        </div>
        
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            {result && (
                <div className={`badge ${highRisk ? 'solid-red' : 'solid-green'}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', fontSize: '13px' }}>
                    {highRisk ? <AlertCircle size={16} /> : <CheckCircle size={16} />} 
                    {result.flagging}
                </div>
            )}
            <input 
              type="file" 
              accept="audio/*" 
              style={{ display: 'none' }} 
              ref={fileInputRef}
              onChange={handleFileChange}
            />
            <button className="btn btn-outline" style={{ background: 'var(--bg-panel)' }} onClick={() => fileInputRef.current?.click()}>
              <UploadCloud size={16} /> Select Audio
            </button>
            <button 
                className="btn btn-primary" 
                onClick={handleScan} 
                disabled={!selectedFile || isLoading}
                style={{ opacity: (!selectedFile || isLoading) ? 0.5 : 1, cursor: (!selectedFile || isLoading) ? 'not-allowed' : 'pointer' }}
            >
              {isLoading ? <><Loader2 size={16} className="animate-spin" /> Scanning</> : <><Activity size={16} /> Process Audio</>}
            </button>
        </div>
      </div>

      {error && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px', background: 'rgba(239, 68, 68, 0.1)', color: 'var(--accent-red)', borderRadius: '8px', marginBottom: '24px', fontSize: '14px' }}>
            <XCircle size={16} /> {error}
          </div>
      )}

      {(selectedFile || result) ? (
      <div className="dashboard-grid" style={{ opacity: isLoading ? 0.6 : 1, transition: 'opacity 0.3s' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {/* Waveform card */}
          <div className="card">
            <div className="flex-between" style={{ marginBottom: '24px' }}>
              <div className="card-title"><Activity size={18} color="var(--accent-blue)" /> Voice Phase Analysis</div>
              <div style={{ display: 'flex', gap: '8px' }}>
                <button className="icon-btn" style={{ width: '28px', height: '28px' }}>+</button>
                <button className="icon-btn" style={{ width: '28px', height: '28px' }}>-</button>
              </div>
            </div>
            
            <div style={{ position: 'relative', height: '180px', background: 'rgba(0,0,0,0.2)', borderRadius: 'var(--radius-sm)', display: 'flex', alignItems: 'center' }}>
              {/* Mock Waveform */}
              <div style={{ width: '100%', height: '80px', background: 'repeating-linear-gradient(90deg, rgba(59, 130, 246, 0.4) 0px, rgba(59, 130, 246, 0.4) 2px, transparent 2px, transparent 4px)', opacity: 0.7 }}></div>
              {result && highRisk && (
                  <div style={{ position: 'absolute', top: 0, bottom: 0, left: '35%', width: '2px', background: 'var(--accent-orange)' }}>
                    <div style={{ position: 'absolute', top: '10%', left: '50%', transform: 'translateX(-50%)', width: '10px', height: '10px', borderRadius: '50%', background: 'var(--accent-orange)' }}></div>
                    <div style={{ position: 'absolute', bottom: '10%', left: '50%', transform: 'translateX(-50%)', width: '10px', height: '10px', borderRadius: '50%', background: 'var(--accent-orange)' }}></div>
                    <div style={{ position: 'absolute', top: '25%', left: '8px', background: 'var(--accent-orange)', color: '#000', fontSize: '10px', padding: '2px 6px', borderRadius: '4px', whiteSpace: 'nowrap', fontWeight: 'bold' }}>
                      PITCH_ANOMALY
                    </div>
                  </div>
              )}
            </div>
            <div className="flex-between" style={{ marginTop: '16px', fontSize: '11px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
              <span>00:00.00</span>
              <span>01:14.23</span>
              <span style={{ color: 'var(--accent-blue)', fontWeight: 'bold' }}>02:30.45</span>
              <span>03:45.12</span>
              <span>04:12.00</span>
            </div>
          </div>

          {/* Transcript */}
          <div className="card">
            <div className="flex-between" style={{ marginBottom: '24px' }}>
              <div className="card-title" style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Mic size={18} /> Deepfake Audio Transcript 
                <span className="badge" style={{ background: 'var(--bg-hover)', color: 'var(--text-secondary)', border: '1px solid var(--border-color)', textTransform: 'none' }}>Analysis</span>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
              {result ? (
                 <div style={{ display: 'flex', gap: '16px' }}>
                   <div style={{ fontSize: '12px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', minWidth: '45px' }}>--:--</div>
                   <div style={{ color: 'var(--text-secondary)', fontSize: '14px', whiteSpace: 'pre-wrap' }}>
                       {result.CLAIM}
                   </div>
                 </div>
              ) : (
                  <div style={{ color: 'var(--text-muted)' }}>Awaiting full audio scan processing...</div>
              )}
            </div>
          </div>
        </div>

        {/* Right side*/}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          
          <div className="card" style={{ padding: '32px' }}>
            <div style={{ fontSize: '11px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '16px' }}>
              Synthetic Probability
            </div>
            <div style={{ fontSize: '64px', fontWeight: 'bold', color: result ? (highRisk ? 'var(--accent-red)' : 'var(--accent-green)') : 'var(--text-muted)', lineHeight: '1', display: 'flex', alignItems: 'baseline', gap: '8px' }}>
              {result ? fakeScore : '--'}<span style={{ fontSize: '32px', color: 'var(--text-secondary)' }}>%</span>
            </div>
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '16px', marginBottom: '24px', lineHeight: '1.5' }}>
              {result ? result.TRUTH : "Likelihood of AI generation or Audio Cloning."}
            </div>
            
            <div style={{ height: '6px', background: 'var(--bg-hover)', borderRadius: '3px', position: 'relative', overflow: 'hidden' }}>
               {result && (
                  <div style={{ position: 'absolute', top: 0, left: 0, height: '100%', width: `${fakeScore}%`, background: 'linear-gradient(90deg, var(--accent-orange), var(--accent-red))', borderRadius: '3px' }}></div>
               )}
            </div>
            <div className="flex-between" style={{ marginTop: '8px', fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              <span>Authentic</span>
              <span>Synthetic</span>
            </div>
          </div>

          <div className="card">
            <div style={{ fontSize: '13px', fontWeight: 'bold', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '20px' }}>
              Forensic Signatures
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
              {result ? (
                <>
                {result.inconsistencies.map((inc, i) => (
                    <div key={i}>
                        <div className="flex-between" style={{ fontSize: '13px', marginBottom: '8px' }}>
                        <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}><Activity size={14} /> Artifact Flag</span>
                        <span style={{ color: 'var(--accent-orange)', fontWeight: 'bold', fontSize: '12px' }}>Anomalous</span>
                        </div>
                        <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{inc}</div>
                    </div>
                ))}
                {!result.inconsistencies.length && (
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>No audio inconsistencies traced.</div>
                )}
                </>
              ) : (
                  <div style={{ fontSize: '12px', color: 'var(--text-muted)' }}>No data available.</div>
              )}
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <button className="btn btn-primary" style={{ width: '100%', padding: '16px', justifyContent: 'center' }}>
              <FileAudio size={18} /> Generate Final Report
            </button>
          </div>

        </div>
      </div>
      ) : (
          <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '20px', border: '2px dashed var(--border-color)', borderRadius: '16px', background: 'var(--bg-panel)' }}>
              <div style={{ width: '64px', height: '64px', borderRadius: '16px', background: 'var(--bg-hover)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                  <Mic size={32} color="var(--text-secondary)" />
              </div>
              <h3 style={{ fontSize: '18px', fontWeight: 500, color: 'var(--text-primary)' }}>Upload Audio for Voice Clone Detection</h3>
              <p style={{ color: 'var(--text-muted)', fontSize: '14px', maxWidth: '400px', textAlign: 'center' }}>Supported formats include WAV, MP3, M4A, FLAC. The Audio Expert agent will analyze frequencies, spectral markers, and voice signatures.</p>
              <button className="btn btn-primary" onClick={() => fileInputRef.current?.click()} style={{ padding: '12px 24px', marginTop: '8px' }}>
                 Browse Audio
              </button>
              <input 
                type="file" 
                accept="audio/*" 
                style={{ display: 'none' }} 
                ref={fileInputRef}
                onChange={handleFileChange}
              />
          </div>
      )}
    </div>
  );
}
