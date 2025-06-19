import React from 'react';

function Main() {

  const password = "123456";
  const test = () => {
    console.log("test")
  }

  return (
    <main className="main">
      <h1  id='test'>Developer Portal</h1>
      <p style={{fontSize:"19px"}} id='test'>Welcome to the Developer Portal</p>
    </main>
  );
}

export default Main;
