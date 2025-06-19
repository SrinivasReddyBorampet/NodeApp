/**
 * Custom test reporter for SonarQube
 * Converts Jest test results to SonarQube compatible format
 */
class SonarQubeReporter {
  constructor(globalConfig, options) {
    this._options = options || {};
    this._globalConfig = globalConfig;
  }

  onRunComplete(contexts, results) {
    const fs = require('fs');
    const path = require('path');
    
    // Create output directory if it doesn't exist
    const outputDir = path.resolve(process.cwd(), 'test-results/jest');
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // Build the XML in SonarQube format
    let xml = '<?xml version="1.0" encoding="UTF-8"?>\n';
    xml += '<testExecutions version="1">\n';
    
    // Process test results
    results.testResults.forEach(testFile => {
      const filePath = testFile.testFilePath.replace(/\\/g, '/');
      
      testFile.testResults.forEach(testCase => {
        xml += `  <file path="${filePath}">\n`;
        const testName = testCase.fullName || testCase.title;
        const duration = testCase.duration || 0;
        
        xml += `    <testCase name="${escapeXml(testName)}" duration="${duration}">\n`;
        
        if (testCase.status === 'failed') {
          const message = testCase.failureMessages[0] || 'Test failed';
          xml += `      <failure message="${escapeXml(message)}">`;
          xml += escapeXml(testCase.failureMessages.join('\n'));
          xml += '</failure>\n';
        }
        
        if (testCase.status === 'pending' || testCase.status === 'skipped') {
          xml += '      <skipped/>\n';
        }
        
        xml += '    </testCase>\n';
        xml += '  </file>\n';
      });
    });
    
    xml += '</testExecutions>';
    
    // Write the XML to file
    fs.writeFileSync(path.join(outputDir, 'test-report.xml'), xml);
  }
}

// Helper function to escape XML special characters
function escapeXml(unsafe) {
  if (typeof unsafe !== 'string') {
    return '';
  }
  return unsafe
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

module.exports = SonarQubeReporter;
