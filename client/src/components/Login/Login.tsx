import { useState } from "react";
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

export function Login({ language, onLogin }: LoginProps) {
  const [role, setRole] = useState(ROLES[0]);
  const [stationId, setStationId] = useState("S-101");
  const [districtId, setDistrictId] = useState("D-10");

  return (
    <div className="login-container">
      <div className="login-box">
        <h2>{t(language, "loginTitle")}</h2>
        <p className="login-subtitle">Local Dev Mode</p>
        
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
