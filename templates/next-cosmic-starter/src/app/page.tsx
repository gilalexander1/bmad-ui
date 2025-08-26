'use client'

export default function Page() {
  return (
    <main className="p-6 md:p-10 space-y-6">
      <header className="glass p-6 border border-matrix-green/30">
        <h1 className="text-3xl md:text-4xl font-bold text-gradient">Cosmic Starter</h1>
        <p className="mt-2 text-sm text-gray-300 font-mono">
          Reusable BMAD theme • matrix.green • glass • glow
        </p>
      </header>

      <section className="grid md:grid-cols-2 gap-6">
        <div className="glass p-6">
          <h2 className="font-mono text-matrix-green text-sm">Utilities</h2>
          <div className="mt-3 flex flex-wrap gap-2">
            <span className="matrix-text">matrix-text</span>
            <span className="text-gradient">text-gradient</span>
            <span className="cosmic-glow px-2 py-1">cosmic-glow</span>
            <span className="cosmic-pulse px-2 py-1">cosmic-pulse</span>
          </div>
        </div>

        <div className="glass p-6">
          <h2 className="font-mono text-matrix-green text-sm">Form</h2>
          <input className="form-input w-full mt-3" placeholder="Type here" />
          <div className="mt-4">
            <div className="progress-bar" style={{ width: '60%' }} />
          </div>
        </div>
      </section>

      <div className="glass p-6 flex items-center justify-between">
        <span className="font-mono text-gray-300">Status: READY</span>
        <button className="glass-button text-matrix-green font-mono px-4 py-2">Launch</button>
      </div>
    </main>
  )
}

