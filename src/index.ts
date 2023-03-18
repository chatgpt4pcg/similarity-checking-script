import Tesseract from 'tesseract.js';
import fs from 'fs'

const testFolder = './test_images/';
const outputFolder = './output/';

fs.readdirSync(testFolder).forEach(file => {
  Tesseract.recognize(
    testFolder + file,
    'eng',
    { logger: () => { } }
  ).then(({ data: { text, confidence } }) => {
    if (!fs.existsSync(outputFolder)) {
      fs.mkdirSync(outputFolder);
    }
    const outputFileName = file.split('.').slice(0, -1).join('.')
    console.log(`${new Date()} - ${outputFileName} - ${text.trim()} - ${confidence}`)
    fs.writeFileSync(outputFolder + outputFileName + '.txt', `${text.trim()}\n${confidence}`)
  })
})