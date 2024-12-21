function Hero() {
  return (
    <div className="relative overflow-hidden bg-transparent py-24 sm:py-32">
      <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center [mask-image:linear-gradient(180deg,white,rgba(255,255,255,0))]"></div>
      <div className="relative mx-auto max-w-7xl px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h1 className="text-4xl font-bold tracking-tight sm:text-6xl bg-clip-text text-transparent bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 pb-2">
            PathFinder AI
          </h1>
          <p className="mt-6 text-lg leading-8 text-gray-300">
            Discover the latest tech events, hackathons, and conferences worldwide. 
            Powered by AI to bring you curated opportunities in the tech ecosystem.
          </p>
          <div className="mt-10 flex items-center justify-center gap-x-6">
            <a
              href="https://twitter.com/Gungun__23"
              target="_blank"
              rel="noopener noreferrer"
              className="rounded-full px-6 py-3 text-sm font-semibold text-white shadow-sm 
                       bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 
                       hover:to-purple-700 focus-visible:outline focus-visible:outline-2 
                       focus-visible:outline-offset-2 focus-visible:outline-blue-600
                       transition-all duration-300 ease-in-out hover:scale-105"
            >
              Follow our Bot
            </a>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Hero 