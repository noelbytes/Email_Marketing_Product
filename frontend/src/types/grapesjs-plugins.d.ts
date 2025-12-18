declare module 'grapesjs-preset-newsletter' {
  import type { Editor } from 'grapesjs'
  const plugin: (editor: Editor, opts?: Record<string, unknown>) => void
  export default plugin
}

declare module 'grapesjs-blocks-basic' {
  import type { Editor } from 'grapesjs'
  const plugin: (editor: Editor, opts?: Record<string, unknown>) => void
  export default plugin
}
