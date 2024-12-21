function Hero() {
  return (
    <div className="relative overflow-hidden bg-gradient-to-b from-primary-50 to-white py-24 sm:py-32">
      <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-10"></div>
      <div className="absolute -top-24 -left-24 w-96 h-96 bg-primary-200 rounded-full blur-3xl opacity-30"></div>
      <div className="absolute -bottom-24 -right-24 w-96 h-96 bg-primary-300 rounded-full blur-3xl opacity-30"></div>
      <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-3xl text-center">
          <div className="relative mb-8 p-2">
            <h1 className="font-display text-7xl sm:text-8xl font-bold tracking-tight">
              <span className="inline-block transform transition-transform duration-300">
                <span className="bg-gradient-to-r from-primary-600 via-primary-500 to-primary-400 
                               bg-clip-text text-transparent">Path</span>
              </span>
              <span className="inline-block transform transition-transform duration-300">
                <span className="bg-gradient-to-r from-primary-500 via-primary-400 to-primary-300 
                               bg-clip-text text-transparent">Finder</span>
              </span>
              <span className="relative inline-block ml-2 transform transition-transform duration-300">
                <span className="bg-gradient-to-r from-primary-400 to-primary-300 
                               bg-clip-text text-transparent">AI</span>
                <div className="absolute -top-1 -right-1 w-2 h-2 bg-primary-500 rounded-full"></div>
              </span>
            </h1>
            <div className="absolute -left-4 top-1/2 w-3 h-3 bg-primary-500/50 rounded-full"></div>
            <div className="absolute -right-4 top-1/2 w-3 h-3 bg-primary-500/50 rounded-full"></div>
            <div className="absolute left-1/4 -bottom-2 w-24 h-1 bg-gradient-to-r from-transparent via-primary-500/50 to-transparent rounded-full"></div>
          </div>
          <span className="block text-2xl sm:text-3xl text-surface-600 font-normal font-sans">
            Your Gateway to Tech Events
          </span>
          <p className="mt-6 text-lg leading-8 text-surface-600 font-sans max-w-xl mx-auto">
            Discover the latest tech events, hackathons, and conferences worldwide. 
            Powered by AI to bring you curated opportunities in the tech ecosystem.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <a
              href="https://twitter.com/Gungun__23"
              target="_blank"
              rel="noopener noreferrer"
              className="group flex items-center gap-2 px-6 py-3.5 text-base font-semibold 
                       text-white shadow-sm bg-primary-500 rounded-full
                       hover:bg-primary-600 focus-visible:outline 
                       focus-visible:outline-2 focus-visible:outline-offset-2 
                       focus-visible:outline-primary-600 transition-all duration-300"
            >
              <span>Follow our Bot</span>
              <svg 
                className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" 
                fill="currentColor" 
                viewBox="0 0 24 24"
              >
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
            </a>
          </div>
          <div className="mt-16 grid grid-cols-2 gap-8 md:grid-cols-3 lg:mt-24">
            {[
              ['10+', 'Active Events'],
              ['24/7', 'Updates'],
              ['Global', 'Coverage'],
            ].map(([stat, label]) => (
              <div key={label} className="mx-auto flex max-w-xs flex-col gap-y-2">
                <dt className="text-base leading-7 text-surface-600">{label}</dt>
                <dd className="font-display text-3xl font-semibold tracking-tight text-surface-900">
                  {stat}
                </dd>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero 