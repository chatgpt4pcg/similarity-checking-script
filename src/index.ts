import Tesseract from 'tesseract.js';
import fs from 'fs'
import parseArgs from 'minimist'

const outputFolder = './output/';
const dateTimeString = new Date().toISOString()

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const sourceFolder = args['s'] + '/'
  const targetCharacter = args['t'].toUpperCase()

  await recognize(sourceFolder, targetCharacter)
}

async function recognize(sourceFolder: string, targetCharacter: string) {
  const files = await fs.promises.readdir(sourceFolder);
  for (const file of files) {
    const { data: { text, confidence } } = await Tesseract.recognize(
      sourceFolder + file,
      'eng',
      { logger: () => { } }
    )

    if (!fs.existsSync(outputFolder)) {
      fs.mkdirSync(outputFolder);
    }

    const characterOutputFolder = outputFolder + targetCharacter + '/'

    if (!fs.existsSync(characterOutputFolder)) {
      fs.mkdirSync(characterOutputFolder);
    }

    const outputFileName = file.split('.').slice(0, -1).join('.')
    const logMessage = `${new Date()} - ${outputFileName} - ${text.trim()} - ${confidence}`
    const similarityScore = `${outputFileName},${score(targetCharacter, text.trim(), confidence)}`

    console.log(logMessage)

    await fs.promises.writeFile(characterOutputFolder + outputFileName + '.txt', `${text.trim()}\n${confidence}`)
    await fs.promises.appendFile(characterOutputFolder + `_log_${dateTimeString}.txt`, logMessage + '\n')
    await fs.promises.appendFile(characterOutputFolder + `_result_${dateTimeString}.csv`, similarityScore + '\n')
  }
}

function score(targetCharacter: string, predictedText: string, confidence: number) {
  if (predictedText === targetCharacter) {
    return confidence / 100
  }

  return 0
}

main()