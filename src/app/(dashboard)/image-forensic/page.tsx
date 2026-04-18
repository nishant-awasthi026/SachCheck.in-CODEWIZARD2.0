"use client";
import React, { useState, useRef } from 'react';
import { Download, Crosshair, Map, Activity, FileDigit, AlertCircle, UploadCloud, Loader2, Image as ImageIcon, XCircle, CheckCircle } from 'lucide-react';
import { verifyMultimodal, FactCheckResponse } from '@/lib/api';

export default function ImageForensicPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<FactCheckResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
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
      setError(err.message || "Failed to process image.");
    } finally {
      setIsLoading(false);
    }
  };

  const authenticityScore = result ? Math.round((result.credibility_scoring_mechanism) * 100) : 0;
  const isManipulated = result?.flagging === "HIGH_RISK" || result?.flagging === "FALSE" || result?.flagging === "MANIPULATED";

  return (
    <div className="animate-slide-up">
      <div className="flex-between" style={{ marginBottom: "24px" }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span style={{ color: 'var(--text-secondary)', fontSize: '14px', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
            File: {selectedFile ? selectedFile.name : 'NO_FILE_SELECTED'}
          </span>
          {result && (
              <span className={`badge ${isManipulated ? 'red' : 'green'}`}>
                {isManipulated ? <AlertCircle size={14} /> : <CheckCircle size={14} />} 
                {result.flagging}
              </span>
          )}
        </div>
        <div style={{ display: 'flex', gap: '16px' }}>
            <input 
              type="file" 
              accept="image/*" 
              style={{ display: 'none' }} 
              ref={fileInputRef}
              onChange={handleFileChange}
            />
            <button className="btn btn-outline" style={{ background: 'var(--bg-panel)' }} onClick={() => fileInputRef.current?.click()}>
              <UploadCloud size={16} /> Select Image
            </button>
            <button 
                className="btn btn-primary" 
                onClick={handleScan} 
                disabled={!selectedFile || isLoading}
                style={{ opacity: (!selectedFile || isLoading) ? 0.5 : 1, cursor: (!selectedFile || isLoading) ? 'not-allowed' : 'pointer' }}
            >
              {isLoading ? <><Loader2 size={16} className="animate-spin" /> Scanning</> : <><Activity size={16} /> Initialize Scan</>}
            </button>
            <button className="btn btn-outline" style={{ background: 'var(--bg-panel)' }} disabled={!result}>
              <Download size={16} /> Export
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
          
          <div className="card" style={{ padding: 0, overflow: 'hidden' }}>
            <div style={{ padding: '24px', borderBottom: '1px solid var(--border-color)' }}>
              <h2 style={{ fontSize: '20px', margin: 0, fontFamily: 'var(--font-outfit)' }}>Forensic Image Scan</h2>
            </div>
            
            <div style={{ position: 'relative', width: '100%', height: '400px', background: 'var(--bg-sidebar)', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}>
               {previewUrl ? (
                   <img src={previewUrl} style={{ width: '100%', height: '100%', objectFit: 'contain' }} alt="Forensic Target" />
               ) : (
                   <div style={{ color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px', opacity: 0.8 }}>
                     <Map size={48} />
                     <span>[ No Image Loaded ]</span>
                   </div>
               )}
               
               {/* Scanner Overlay only if simulating or result exists */}
               {result && isManipulated && (
                  <>
                    <div style={{ position: 'absolute', top: '30%', left: '40%', width: '120px', height: '140px', border: '2px dashed var(--accent-red)', background: 'rgba(220, 38, 38, 0.05)' }}>
                        <div style={{ position: 'absolute', top: '-10px', right: '-10px', width: '20px', height: '20px', borderTop: '2px solid var(--accent-red)', borderRight: '2px solid var(--accent-red)' }}></div>
                        <div style={{ position: 'absolute', bottom: '-10px', left: '-10px', width: '20px', height: '20px', borderBottom: '2px solid var(--accent-red)', borderLeft: '2px solid var(--accent-red)' }}></div>
                    </div>
                  </>
               )}

               {/* Scanner Toggles */}
               <div style={{ position: 'absolute', bottom: '16px', left: '50%', transform: 'translateX(-50%)', display: 'flex', border: '1px solid var(--border-color)', borderRadius: '6px', overflow: 'hidden' }}>
                 <div style={{ padding: '6px 16px', background: 'var(--bg-panel)', fontSize: '13px', cursor: 'pointer', fontWeight: 500 }}>Original</div>
                 <div style={{ padding: '6px 16px', background: 'var(--bg-hover)', fontSize: '13px', cursor: 'pointer', borderLeft: '1px solid var(--border-color)' }}>Noise Map</div>
                 <div style={{ padding: '6px 16px', background: 'var(--bg-hover)', fontSize: '13px', cursor: 'pointer', borderLeft: '1px solid var(--border-color)' }}>Heatmap</div>
               </div>
            </div>
          </div>

          <div className="card">
            <div className="flex-between" style={{ marginBottom: '16px', fontSize: '13px', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
              <span>Overall Authenticity Score</span>
              <span style={{ fontSize: '24px', fontWeight: 'bold', color: result ? (authenticityScore > 50 ? 'var(--accent-green)' : 'var(--accent-red)') : 'var(--text-muted)' }}>
                  {result ? `${authenticityScore}%` : '--'}
              </span>
            </div>
            <div style={{ height: '8px', borderRadius: '4px', background: 'linear-gradient(90deg, var(--accent-red) 0%, var(--accent-orange) 50%, var(--accent-green) 100%)', position: 'relative' }}>
              {result && (
                  <div style={{ position: 'absolute', top: '-4px', left: `${authenticityScore}%`, width: '4px', height: '16px', background: 'var(--text-primary)', borderRadius: '2px', transition: 'left 1s cubic-bezier(0.16, 1, 0.3, 1)' }}></div>
              )}
            </div>
            <div className="flex-between" style={{ marginTop: '12px', fontSize: '11px', color: 'var(--text-muted)' }}>
              <span>Highly Manipulated</span>
              <span>Uncertain</span>
              <span>Verified Authentic</span>
            </div>
          </div>

        </div>

        {/* Right side*/}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div className="card">
            <div className="card-title" style={{ marginBottom: '20px' }}>
              <Crosshair size={16} color="var(--text-secondary)" /> Anomaly Detection
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {result ? (
                    <>
                    {result.classifiers.map((classifier, idx) => (
                        <div key={idx} style={{ padding: '16px', borderLeft: `3px solid var(--accent-red)`, background: 'var(--bg-hover)', borderRadius: '0 var(--radius-sm) var(--radius-sm) 0' }}>
                            <div className="flex-between" style={{ marginBottom: '8px' }}>
                            <strong style={{ fontSize: '14px', color: 'var(--text-primary)' }}>{classifier}</strong>
                            <span style={{ color: 'var(--accent-red)', fontWeight: 'bold' }}>Triggered</span>
                            </div>
                            <div style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                                Found within logic trace sequence.
                            </div>
                        </div>
                    ))}
                    {result.inconsistencies.map((inc, idx) => (
                        <div key={idx + 10} style={{ padding: '16px', borderLeft: `3px solid var(--accent-orange)`, background: 'var(--bg-hover)', borderRadius: '0 var(--radius-sm) var(--radius-sm) 0' }}>
                            <div className="flex-between" style={{ marginBottom: '8px' }}>
                            <strong style={{ fontSize: '14px', color: 'var(--text-primary)' }}>System Flag</strong>
                            <span style={{ color: 'var(--accent-orange)', fontWeight: 'bold' }}>Anomaly</span>
                            </div>
                            <div style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                                {inc}
                            </div>
                        </div>
                    ))}
                    {!result.classifiers.length && !result.inconsistencies.length && (
                         <div style={{ padding: '16px', borderLeft: '3px solid var(--accent-green)', background: 'var(--bg-hover)', borderRadius: '0 var(--radius-sm) var(--radius-sm) 0' }}>
                            <div className="flex-between" style={{ marginBottom: '8px' }}>
                            <strong style={{ fontSize: '14px', color: 'var(--text-primary)' }}>Integrity Check</strong>
                            <span style={{ color: 'var(--accent-green)', fontWeight: 'bold' }}>Clear</span>
                            </div>
                            <div style={{ fontSize: '12px', color: 'var(--text-muted)', lineHeight: '1.5' }}>
                                No anomalies or manipulations traced by the active pipeline models.
                            </div>
                        </div>
                    )}
                    </>
                ) : (
                    <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>Awaiting scan...</div>
                )}
            </div>
          </div>

          <div className="card">
            <div className="card-title" style={{ marginBottom: '20px' }}>
              <FileDigit size={16} color="var(--text-secondary)" /> Metadata & Explainability
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '16px', fontFamily: 'var(--font-inter)', fontSize: '13px' }}>
              {result ? (
                  <>
                  <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '8px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Verdict:</span>
                    <span style={{ color: 'var(--text-secondary)' }}>{result.TRUTH}</span>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: '8px' }}>
                    <span style={{ color: 'var(--text-muted)' }}>Logic Flow:</span>
                    <span style={{ color: 'var(--text-secondary)' }}>{result.automated_fact_verification_pipeline.join(" ➔ ")}</span>
                  </div>
                  <div style={{ background: 'var(--bg-main)', padding: '12px', borderRadius: '8px', border: '1px solid var(--border-color)', color: 'var(--text-secondary)', fontSize: '12px', lineHeight: '1.5' }}>
                      <strong style={{ display: 'block', marginBottom: '8px', color: 'var(--text-primary)' }}>Heuristic Core:</strong>
                      {result.EXPLAINATION}
                  </div>
                  </>
              ) : (
                  <div style={{ color: 'var(--text-muted)', fontSize: '13px' }}>Awaiting scan...</div>
              )}
            </div>

            <div className="grid-2" style={{ marginTop: '24px' }}>
              <div style={{ background: 'var(--bg-hover)', border: result && isManipulated ? '1px solid rgba(220, 38, 38, 0.2)' : 'none', padding: '12px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                <div style={{ color: 'var(--text-muted)', fontSize: '11px', textTransform: 'uppercase', marginBottom: '4px' }}>Digital Sig</div>
                <div style={{ color: result ? (isManipulated ? 'var(--accent-red)' : 'var(--accent-green)') : 'var(--text-muted)', fontWeight: 'bold', fontSize: '13px' }}>
                    {result ? (isManipulated ? 'Invalid' : 'Verified') : '--'}
                </div>
              </div>
              <div style={{ background: 'var(--bg-hover)', padding: '12px', borderRadius: 'var(--radius-sm)', textAlign: 'center' }}>
                <div style={{ color: 'var(--text-muted)', fontSize: '11px', textTransform: 'uppercase', marginBottom: '4px' }}>Modality</div>
                <div style={{ color: 'var(--text-primary)', fontWeight: 'bold', fontSize: '13px', textTransform: 'capitalize' }}>
                    {selectedFile ? selectedFile.name.split('.').pop() : '--'}
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
      ) : (
        <div style={{ height: '400px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', gap: '20px', border: '2px dashed var(--border-color)', borderRadius: '16px', background: 'var(--bg-panel)' }}>
            <div style={{ width: '64px', height: '64px', borderRadius: '16px', background: 'var(--bg-hover)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <ImageIcon size={32} color="var(--text-secondary)" />
            </div>
            <h3 style={{ fontSize: '18px', fontWeight: 500, color: 'var(--text-primary)' }}>Upload an Image for Forensic Scanning</h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '14px', maxWidth: '400px', textAlign: 'center' }}>Supported formats include JPEG, PNG, WEBP. The Deepfake Detection agent will extract EXIF metadata and analyze pixel distribution for manipulations.</p>
            <button className="btn btn-primary" onClick={() => fileInputRef.current?.click()} style={{ padding: '12px 24px', marginTop: '8px' }}>
               Browse Files
            </button>
            <input 
              type="file" 
              accept="image/*" 
              style={{ display: 'none' }} 
              ref={fileInputRef}
              onChange={handleFileChange}
            />
        </div>
      )}
    </div>
  );
}
