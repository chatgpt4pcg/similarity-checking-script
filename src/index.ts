import Tesseract from 'tesseract.js';
import fs from 'fs'
import parseArgs from 'minimist'
import path from 'path'

const outputFolder = path.posix.resolve('./similarity/');
const dateTimeString = new Date().toISOString()

async function main() {
  const args = parseArgs(process.argv.slice(2))
  if (args['s'] === undefined) {
    throw Error('Insufficient parameters to work with.')
  }

  const sourceFolder = args['s'] + '/'
  const sFolder = path.posix.resolve(sourceFolder)
  await processFolder(sFolder)
}

async function processFolder(sourceFolder: string) {
  const files = await fs.promises.readdir(sourceFolder);
  for (const file of files) {
    const fPath = path.posix.join(sourceFolder, file)
    const stats = await fs.promises.stat(fPath)

    if (stats.isDirectory()) {
      const nextFolder = path.posix.join(sourceFolder, file)
      processFolder(nextFolder)
    } else {
      recognize(fPath, file)
    }
  }
}

async function recognize(filePath: string, file: string) {
  const outputPath = filePath.replace(file, '').split('/').slice(2).join('/');

  if (file.indexOf('.png') === -1 && file.indexOf('.jpg') === -1 && file.indexOf('.jpeg') === -1) {
    return
  }

  if (!fs.existsSync(outputFolder)) {
    fs.mkdirSync(outputFolder);
  }

  outputPath.split('/').slice(-3, -1).reduce((acc, curr) => {
    const folder = path.posix.join(acc, curr)
    if (!fs.existsSync(folder)) {
      fs.mkdirSync(folder);
    }
    return folder
  }, outputFolder)


  const { data: { text, confidence } } = await Tesseract.recognize(
    path.posix.resolve(filePath),
    'eng',
    { logger: () => { } }
  )

  const targetCharacter = outputPath.split('/').slice(-2)[0]

  const logMessage = `${new Date()} - ${file} - ${text.trim()} - ${confidence}`
  console.log(logMessage)

  const similarityScore = `${file},${score(targetCharacter, text.trim(), confidence)}`
  const finalOutputPath = outputPath.split('/').slice(-3, -1).join('/')

  await fs.promises.writeFile(path.posix.join(outputFolder, finalOutputPath, file.split('.').slice(0, -1).join('.') + '.txt'), `${text.trim()}\n${confidence}`)
  await fs.promises.appendFile(path.posix.join(outputFolder, finalOutputPath, `_log_${dateTimeString}.txt`), logMessage + '\n')
  await fs.promises.appendFile(path.posix.join(outputFolder, finalOutputPath, `_result_${dateTimeString}.csv`), similarityScore + '\n')
}

function score(targetCharacter: string, predictedText: string, confidence: number) {
  if (predictedText === targetCharacter) {
    return confidence / 100
  }

  return 0
}

main()