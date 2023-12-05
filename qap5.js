/* 
Title: QAP 5 - JavaScript
Author: Brenda Armstrong SD10
Date: Dec 5, 2023
*/

const fs = require('fs');

// Create an array of JSON data
const jsonData = [
  { id: 1, name: 'Brenda Armstrong', age: 44 },
  { id: 2, name: 'Stephan Bendiksen', age: 43 },
  { id: 3, name: 'Josie Bendiksen', age: 5 },
  { id: 4, name: 'Ellie Bendiksen', age: 5 },
  { id: 5, name: 'Magnus the Cat', age: 1 },
  { id: 6, name: 'Ragnar the Cat', age: 1},
];

// Convert the array to JSON string
const jsonString = JSON.stringify(jsonData, null, 2);

// Write the JSON data to a file
const filePath = 'data.json';
fs.writeFileSync(filePath, jsonString, 'utf-8');
console.log('File created successfully:', filePath);

// Read the JSON data from the file
const readFileContent = fs.readFileSync(filePath, 'utf-8');
const readJsonData = JSON.parse(readFileContent);

// Iterate through the array using forEach() and display fields to the console
readJsonData.forEach(record => {
  console.log(`ID: ${record.id}, Name: ${record.name}, Age: ${record.age}`);
});
