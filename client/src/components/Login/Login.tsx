import { useEffect, useState } from "react";
import { t, type Language } from "../../i18n/strings";
import "./Login.css";

interface LoginProps {
  language: Language;
  onLogin: (role: string, stationId: string, districtId: string) => void;
}

const ROLES = [
  "Station Officer",
  "SCRB Analyst",
  "District SP",
  "System Admin"
];

declare global {
  interface Window {
    catalyst: any;
  }
}

export function Login({ language, onLogin }: LoginProps) {
  const [role, setRole] = useState(ROLES[0]);
  const [stationId, setStationId] = useState("S-101");
  const [districtId, setDistrictId] = useState("D-10");
  
  const [showRoleSelector, setShowRoleSelector] = useState(false);
  const [authError, setAuthError] = useState("");

  useEffect(() => {
    // Attempt to mount Catalyst Embedded Authentication
    if (window.catalyst && window.catalyst.auth) {
      try {
        window.catalyst.auth.isUserAuthenticated().then((result: any) => {
           if (result) {
             // User is already logged in with Catalyst
             setShowRoleSelector(true);
           } else {
             // Show login frame
             window.catalyst.auth.signIn("catalyst-login");
           }
        }).catch((e: any) => {
            console.warn("Catalyst Auth check failed, showing login", e);
            window.catalyst.auth.signIn("catalyst-login");
        });
      } catch (err) {
        setAuthError("Failed to load Catalyst auth.");
      }
    }
  }, []);

  if (showRoleSelector) {
    return (
      <div className="login-container">
        <div className="login-box">
          <h2>{t(language, "loginTitle")}</h2>
          <p className="login-subtitle">Complete Profile Setup</p>
          
          <div className="form-group">
            <label>{t(language, "loginRoleLabel")}</label>
            <select value={role} onChange={(e) => setRole(e.target.value)}>
              {ROLES.map((r) => (
                <option key={r} value={r}>{r}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Station ID</label>
            <input 
              value={stationId} 
              onChange={(e) => setStationId(e.target.value)} 
              placeholder="e.g. S-101"
            />
          </div>

          <div className="form-group">
            <label>District ID</label>
            <input 
              value={districtId} 
              onChange={(e) => setDistrictId(e.target.value)} 
              placeholder="e.g. D-10"
            />
          </div>

          <button className="login-button" onClick={() => onLogin(role, stationId, districtId)}>
            {t(language, "loginButton")}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>{t(language, "loginTitle")}</h2>
        <p className="login-subtitle">Authenticate via Catalyst</p>
        
        {authError && <p style={{color: 'red'}}>{authError}</p>}
        
        {/* Catalyst Embedded Auth will mount in this div */}
        <div id="catalyst-login" style={{minHeight: '300px', display: 'flex', justifyContent: 'center', alignItems: 'center'}}>
           {!window.catalyst && <p>Local Dev Mode: Catalyst SDK not found.</p>}
        </div>
        
        {/* Dev Mode fallback button to bypass if Catalyst isn't loaded locally */}
        <button 
          className="login-button dev-override-btn" 
          style={{marginTop: '20px', background: 'transparent', border: '1px solid rgba(255,255,255,0.2)'}} 
          onClick={() => setShowRoleSelector(true)}
        >
          Dev Mode Bypass
        </button>
      </div>
    </div>
  );
}
