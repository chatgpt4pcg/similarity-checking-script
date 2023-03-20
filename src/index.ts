import { directoryWalk, replicateFolderStructure } from './file-utils';

import fs from 'fs'
import parseArgs from 'minimist'
import path from 'path'
import { recognize } from 'chatgpt4pcg';

const outputFolder = path.posix.resolve('./similarity/');
const dateTimeString = new Date().toISOString().replaceAll(':', '_')

async function main() {
  const args = parseArgs(process.argv.slice(2))
  const argv = process.platform === 'win32' ? args['_'] : args['s']
  if (argv === undefined) {
    throw Error('Insufficient parameters to work with.')
  }

  const sourceFolder = argv + '/'
  const sFolder = path.posix.resolve(sourceFolder)
  await directoryWalk(sFolder, processFile)
}

async function processFile(filePath: string, file: string) {
  const outputPath = filePath.replace(file, '').split('/').slice(2).join('/');

  if (file.indexOf('.png') === -1 && file.indexOf('.jpg') === -1 && file.indexOf('.jpeg') === -1) {
    return
  }

  await replicateFolderStructure(outputPath, outputFolder)

  const { text, confidence } = await recognize(path.posix.resolve(filePath))

  const logMessage = `${new Date()} - ${file} - ${text.trim()} - ${confidence}`
  console.log(logMessage)

  const similarityScore = `${file},${confidence}`
  const finalOutputPath = outputPath.split('/').slice(-3, -1).join('/')

  await fs.promises.writeFile(path.posix.join(outputFolder, finalOutputPath, file.split('.').slice(0, -1).join('.') + '.txt'), `${text.trim()}\n${confidence}`)
  await fs.promises.appendFile(path.posix.join(outputFolder, finalOutputPath, `_log_${dateTimeString}.txt`), logMessage + '\n')
  await fs.promises.appendFile(path.posix.join(outputFolder, finalOutputPath, `_result_${dateTimeString}.csv`), similarityScore + '\n')
}

main()