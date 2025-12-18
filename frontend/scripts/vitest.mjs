import { spawn } from 'node:child_process'
import path from 'node:path'

const args = process.argv.slice(2).filter((arg) => arg !== '--runInBand')
const vitestBin = process.platform === 'win32' ? 'vitest.cmd' : 'vitest'
const vitestPath = path.resolve('node_modules', '.bin', vitestBin)

const child = spawn(vitestPath, args, { stdio: 'inherit' })
child.on('exit', (code) => process.exit(code ?? 1))

