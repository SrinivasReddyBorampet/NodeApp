import React from 'react';

function Footer() {
  return (
    <footer className="footer">
      <p style={{fontSize:"12px"}}>&copy; {new Date().getFullYear()} Wipro. All rights reserved.</p>
    </footer>
  );
}

export default Footer;
