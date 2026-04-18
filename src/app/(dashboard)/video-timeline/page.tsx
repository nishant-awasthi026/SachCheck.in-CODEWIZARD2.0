"use client";
import React, { useState, useRef } from 'react';
import { Video, Clock, AlertTriangle, CheckCircle, Search, UploadCloud, Loader2, XCircle, Activity, LayoutTemplate, ShieldCheck } from 'lucide-react';
import { verifyMultimodal, FactCheckResponse } from '@/lib/api';

export default function VideoTimelinePage() {
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
      setError(err.message || "Failed to process video.");
    } finally {
      setIsLoading(false);
    }
  };

  const isHighRisk = result?.flagging === "HIGH_RISK" || result?.flagging === "FALSE" || result?.flagging === "MANIPULATED";

  return (
    <div className="animate-slide-up">
      {/* Top Header Section */}
      <div className="flex-between" style={{ marginBottom: "32px", borderBottom: '1px solid var(--border-color)', paddingBottom: '24px' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontSize: '13px', color: 'var(--text-primary)', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <div className={isLoading ? "pulsing-dot" : ""} style={{ background: isLoading ? 'var(--accent-blue)' : 'var(--text-muted)' }}></div> 
              {isLoading ? 'Video processing active' : 'Video Sync Service'}
            </span>
          </div>
          <div style={{ fontSize: '13px', color: 'var(--text-muted)' }}>
              Target: {selectedFile ? selectedFile.name : 'NO_FILE_SELECTED'}
          </div>
        </div>
        
        <div className="header-right" style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          {result && (
              <span className={`badge ${isHighRisk ? 'solid-red' : 'solid-green'}`} style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '8px 16px', fontSize: '13px' }}>
                  {isHighRisk ? <AlertTriangle size={16} /> : <CheckCircle size={16} />} 
                  {result.flagging}
              </span>
          )}
          <input 
            type="file" 
            accept="video/*" 
            style={{ display: 'none' }} 
            ref={fileInputRef}
            onChange={handleFileChange}
          />
          <button className="btn btn-outline" style={{ height: '100%', background: 'var(--bg-panel)' }} onClick={() => fileInputRef.current?.click()}>
            <UploadCloud size={16} /> Select Video
          </button>
          <button 
              className="btn btn-primary" 
              onClick={handleScan} 
              disabled={!selectedFile || isLoading}
              style={{ opacity: (!selectedFile || isLoading) ? 0.5 : 1, cursor: (!selectedFile || isLoading) ? 'not-allowed' : 'pointer' }}
          >
            {isLoading ? <><Loader2 size={16} className="animate-spin" /> Analyzing</> : <><Search size={16} /> Scan Narrative</>}
          </button>
        </div>
      </div>

      {error && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '12px', background: 'rgba(239, 68, 68, 0.1)', color: 'var(--accent-red)', borderRadius: '8px', marginBottom: '24px', fontSize: '14px' }}>
            <XCircle size={16} /> {error}
          </div>
      )}

      {(selectedFile || result) ? (
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 2fr) minmax(0, 1fr)', gap: '24px', opacity: isLoading ? 0.6 : 1, transition: 'opacity 0.3s' }}>
        {/* Left col */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div className="card">
              <div className="flex-between" style={{ marginBottom: '20px' }}>
                <div className="card-title" style={{ fontSize: '15px' }}>
                  <Video size={16} /> Frame & Audio Extraction
                </div>
              </div>
              
              <div style={{ padding: '60px 40px', textAlign: 'center', background: 'var(--bg-sidebar)', borderRadius: 'var(--radius-md)', border: '1px solid var(--border-color)', position: 'relative', overflow: 'hidden' }}>
                 {isLoading ? (
                     <>
                     <Loader2 size={32} color="var(--accent-blue)" className="animate-spin" style={{ margin: '0 auto 16px' }} />
                     <h3 style={{ fontSize: '16px', marginBottom: '8px' }}>Timeline Extraction In Progress</h3>
                     <p style={{ color: 'var(--text-secondary)', fontSize: '13px', maxWidth: '400px', margin: '0 auto' }}>
                       Deepfake heuristics and visual-audio sync analysis are currently scanning the video frames.
                     </p>
                     </>
                 ) : result ? (
                     <>
                     <LayoutTemplate size={48} color={isHighRisk ? "var(--accent-orange)" : "var(--accent-green)"} style={{ margin: '0 auto 16px', opacity: 0.8 }} />
                     <h3 style={{ fontSize: '18px', color: 'var(--text-primary)', marginBottom: '8px' }}>Extraction Complete</h3>
                     <div style={{ color: 'var(--text-secondary)', fontSize: '14px', maxWidth: '500px', margin: '0 auto' }}>
                         {result.CLAIM}
                     </div>
                     {isHighRisk && (
                        <div style={{ marginTop: '24px', display: 'flex', gap: '16px', justifyContent: 'center' }}>
                            <div style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--accent-red)', padding: '6px 12px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>LIP-SYNC ANOMALY DETECTED</div>
                            <div style={{ background: 'rgba(245, 158, 11, 0.1)', color: 'var(--accent-orange)', padding: '6px 12px', borderRadius: '4px', fontSize: '12px', fontWeight: 'bold' }}>FRAME GLITCH OR SPATIAL DRIFT</div>
                        </div>
                     )}
                     </>
                 ) : (
                     <div style={{ opacity: 0.5 }}>
                        <Clock size={32} color="var(--text-muted)" style={{ margin: '0 auto 16px' }} />
                        <h3 style={{ fontSize: '16px', color: 'var(--text-muted)' }}>Awaiting Scan Initialization</h3>
                     </div>
                 )}
              </div>
            </div>

            <div className="card">
                <div className="card-title" style={{ marginBottom: '20px', fontSize: '15px' }}>
                  <ShieldCheck size={16} color="var(--accent-green)" /> AI Counter-Narrative
                </div>
                {result ? (
                    <div style={{ lineHeight: '1.6', color: 'var(--text-primary)', fontSize: '14px' }}>
                        {result.countering_misinformation}
                    </div>
                ) : (
                    <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>Awaiting pipeline execution...</div>
                )}
            </div>
        </div>

        {/* Right col */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div className="card">
                 <div className="card-title" style={{ marginBottom: '20px', fontSize: '15px' }}>
                   <Activity size={16} /> Expert Agent Flags
                </div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    {result ? (
                        <>
                        {result.classifiers.map((classifier, idx) => (
                            <div key={idx} style={{ padding: '12px', background: 'var(--bg-hover)', borderLeft: '3px solid var(--accent-red)', borderRadius: '0 8px 8px 0' }}>
                                <div style={{ fontSize: '13px', fontWeight: 'bold', color: 'var(--text-primary)' }}>{classifier}</div>
                            </div>
                        ))}
                        {result.inconsistencies.map((inc, idx) => (
                            <div key={idx + 20} style={{ padding: '12px', background: 'var(--bg-hover)', borderLeft: '3px solid var(--accent-orange)', borderRadius: '0 8px 8px 0' }}>
                                <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>{inc}</div>
                            </div>
                        ))}
                        {!result.inconsistencies.length && !result.classifiers.length && (
                            <div style={{ padding: '12px', background: 'var(--bg-hover)', borderLeft: '3px solid var(--accent-green)', borderRadius: '0 8px 8px 0' }}>
                                <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>No anomalies found across extracted frames.</div>
                            </div>
                        )}
                        </>
                    ) : (
                        <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>--</div>
                    )}
                </div>
            </div>

            <div className="card">
                <div className="card-title" style={{ marginBottom: '20px', fontSize: '15px' }}>
                   System Trace
                </div>
                {result ? (
                    <div style={{ fontSize: '13px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                        {result.automated_fact_verification_pipeline.map((step, idx) => (
                            <div key={idx} style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                                <div style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'var(--accent-blue)' }}></div>
                                {step}
                            </div>
                        ))}
                        <div style={{ marginTop: '16px', padding: '12px', background: 'var(--bg-main)', borderRadius: '6px', fontSize: '12px' }}>
                            <strong style={{ color: 'var(--text-primary)' }}>Verdict:</strong> {result.TRUTH}
                        </div>
                    </div>
                ) : (
                    <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>--</div>
                )}
            </div>
        </div>
      </div>
      ) : (
          <div style={{ height: '300px', display: 'flex', flexDirection: 'column', gap: '16px', alignItems: 'center', justifyContent: 'center', border: '2px dashed var(--border-color)', borderRadius: '12px', background: 'var(--bg-hover)' }}>
              <Video size={32} color="var(--text-muted)" />
              <div style={{ color: 'var(--text-secondary)', fontSize: '14px' }}>Load a video to perform spatial-temporal checks</div>
              <button className="btn btn-outline" onClick={() => fileInputRef.current?.click()} style={{ background: 'var(--bg-panel)' }}>
                 Browse Videos
              </button>
              <input 
                type="file" 
                accept="video/*" 
                style={{ display: 'none' }} 
                ref={fileInputRef}
                onChange={handleFileChange}
              />
          </div>
      )}
    </div>
  );
}
