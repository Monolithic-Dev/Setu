import './ConnectivityBanner.css';

interface ConnectivityBannerProps {
  isVisible: boolean;
}

export function ConnectivityBanner({ isVisible }: ConnectivityBannerProps) {
  if (!isVisible) return null;

  return (
    <div className="connectivity-banner">
      Unable to reach the server — retrying…
    </div>
  );
}
