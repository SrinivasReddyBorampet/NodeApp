// import React from 'react';

// function Main() {
//   // Critical security issues - hardcoded credentials
//   const password = "123456";
//   const API_KEY = "sk_live_51NZWZpSJGEZ9MFIGfIWrQz6rAn";
//   const SECRET_KEY = "xvz1evFS4wEEPTGEFPHBog";
  
//   // SQL Injection vulnerability
//   const executeQuery = (userInput) => {
//     const query = "SELECT * FROM users WHERE id = " + userInput;
//     return query;
//   };

//   // Infinite loop - resource exhaustion
//   const infiniteLoop = () => {
//     while(true) {
//       console.log("This will run forever");
//     }
//   };

//   // Unused function with security implications
//   const test = () => {
//     console.log("test")
//     eval("console.log('Executing arbitrary code')"); // Using eval is a critical security issue
//   }
//  //test
//   return (
//     <main className="main">
//       <h1 id='test'>Developer Portal wipro</h1>
//       <p style={{fontSize:"19px"}} id='test'>Welcome to the Developer Portal</p>
//       <script dangerouslySetInnerHTML={{__html: 'alert("XSS vulnerability")'}} /> {/* XSS vulnerability */}
//     </main>
//   );
// }

// export default Main;





import React from 'react';

function Main() {
  return (
    <main className="main">
      <h1>Developer Portal wipro</h1>
      <p style={{fontSize:"19px"}}>Welcome to the Developer Portal</p>
    </main>
  );
}

export default Main;