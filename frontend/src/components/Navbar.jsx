import { Link } from 'react-router-dom'

function Navbar() {
  return (
    <nav className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-surface-200">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          <Link to="/" className="flex items-center">
            {/* Logo/Icon */}
            <div className="flex items-center">
              <svg 
                className="w-10 h-10 text-primary-500" 
                viewBox="0 0 40 40" 
                fill="none"
              >
                {/* Compass/Pathfinder shape */}
                <circle cx="20" cy="20" r="16" className="stroke-current" strokeWidth="2"/>
                <circle cx="20" cy="20" r="2" className="fill-current"/>
                <path 
                  d="M20 8 L20 12 M20 28 L20 32 M32 20 L28 20 M12 20 L8 20" 
                  stroke="currentColor" 
                  strokeWidth="2" 
                  strokeLinecap="round"
                />
                {/* AI circuit paths */}
                <path 
                  d="M20 20 L28 12 M20 20 L12 28" 
                  className="stroke-current" 
                  strokeWidth="2"
                  strokeLinecap="round"
                />
                <circle cx="28" cy="12" r="2" className="fill-current"/>
                <circle cx="12" cy="28" r="2" className="fill-current"/>
              </svg>
            </div>

            {/* Text */}
            <span className="font-display text-xl font-medium text-surface-900">
              PathFinder AI
            </span>
          </Link>

          <div className="flex items-center gap-6">
            <Link 
              to="/docs" 
              className="text-surface-600 hover:text-primary-500 transition-colors duration-300"
            >
              Documentation
            </Link>
            <a 
              href="https://twitter.com/Gungun__23" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center space-x-2 px-4 py-2 rounded-lg
                       bg-surface-50 hover:bg-surface-100 
                       text-surface-600 hover:text-primary-500 
                       ring-1 ring-surface-200 hover:ring-primary-200
                       transition-all duration-300"
            >
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/>
              </svg>
              <span>Follow our Bot</span>
            </a>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 