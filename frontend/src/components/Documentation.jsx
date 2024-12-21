import { Link } from 'react-router-dom';

function Documentation() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-primary-50 py-16">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          {/* Introduction */}
          <section className="mb-16">
            <h1 className="font-display text-4xl font-bold text-surface-900 mb-6">
              How PathFinder AI Works
            </h1>
            <p className="text-lg text-surface-600 mb-8">
              PathFinder AI is an intelligent system that discovers, processes, and delivers tech events 
              using a combination of web crawling, AI processing, and automated social media integration.
            </p>

            {/* System Flow Diagram */}
            <div className="bg-white rounded-xl p-8 shadow-sm ring-1 ring-surface-200">
              <h2 className="font-display text-2xl font-semibold text-surface-900 mb-6">
                System Flow Diagram
              </h2>
              <div className="relative">
                <img 
                  src="/diagram.png" 
                  alt="PathFinder AI System Architecture" 
                  className="w-full rounded-lg"
                />
              </div>
              
              
            </div>
          </section>

          {/* Architecture Overview */}
          <section className="mb-16">
            <h2 className="font-display text-2xl font-semibold text-surface-900 mb-4">
              System Architecture
            </h2>
            <div className="bg-white rounded-xl p-6 shadow-sm ring-1 ring-surface-200">
              <h3 className="font-display text-xl text-primary-600 mb-4">Core Components</h3>
              <div className="space-y-4">
                <div className="flex gap-4 items-start">
                  <div className="w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
                            d="M20 12V8a2 2 0 00-2-2h-8L8 4H4a2 2 0 00-2 2v12a2 2 0 002 2h16a2 2 0 002-2v-4m0 0l-4-4m4 4l-4 4m4-4H10" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="font-medium text-surface-900 mb-1">Smart Crawler</h4>
                    <p className="text-surface-600">
                      Intelligently discovers tech events using advanced search algorithms and handles both 
                      static and JavaScript-rendered content using Playwright.
                    </p>
                  </div>
                </div>

                <div className="flex gap-4 items-start">
                  <div className="w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
                            d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="font-medium text-surface-900 mb-1">AI Processor</h4>
                    <p className="text-surface-600">
                      Uses LLaMA 3.1 to analyze and extract structured information from raw HTML content, 
                      with smart chunking and deduplication.
                    </p>
                  </div>
                </div>

                <div className="flex gap-4 items-start">
                  <div className="w-8 h-8 rounded-lg bg-primary-100 flex items-center justify-center flex-shrink-0">
                    <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
                            d="M8 9l3 3-3 3m5 0h3M5 20h14a2 2 0 002-2V6a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h4 className="font-medium text-surface-900 mb-1">Social Integration</h4>
                    <p className="text-surface-600">
                      Automatically formats and shares events on X (Twitter) with engaging content and 
                      relevant hashtags.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </section>

     
          

          {/* Technical Details */}
          <section className="mb-16">
            <h2 className="font-display text-2xl font-semibold text-surface-900 mb-4">
              Technical Implementation
            </h2>
            <div className="space-y-8">
              {/* Crawler Section */}
              <div className="bg-white rounded-xl p-6 shadow-sm ring-1 ring-surface-200">
                <h3 className="font-display text-xl text-primary-600 mb-4">Smart Crawling System</h3>
                <ul className="list-disc list-inside space-y-2 text-surface-600 ml-4">
                  <li>Intelligent search query generation based on current dates and trends</li>
                  <li>Handles both static and dynamic (JavaScript) content using Playwright</li>
                  <li>Smart filtering to avoid duplicate content and irrelevant pages</li>
                  <li>Asynchronous processing for improved performance</li>
                  <li>Rate limiting and respectful crawling practices</li>
                </ul>
              </div>

              {/* Processor Section */}
              <div className="bg-white rounded-xl p-6 shadow-sm ring-1 ring-surface-200">
                <h3 className="font-display text-xl text-primary-600 mb-4">AI Processing Pipeline</h3>
                <ul className="list-disc list-inside space-y-2 text-surface-600 ml-4">
                  <li>Smart text chunking for optimal AI processing</li>
                  <li>Two-stage analysis: initial relevance check followed by detailed extraction</li>
                  <li>Advanced deduplication using LLM-based similarity detection</li>
                  <li>Structured data extraction with consistent schema</li>
                  <li>Date normalization and validation</li>
                </ul>
              </div>

              {/* Social Integration Section */}
              <div className="bg-white rounded-xl p-6 shadow-sm ring-1 ring-surface-200">
                <h3 className="font-display text-xl text-primary-600 mb-4">Social Media Integration</h3>
                <ul className="list-disc list-inside space-y-2 text-surface-600 ml-4">
                  <li>Automated tweet generation with engaging format</li>
                  <li>Smart hashtag selection based on event type and tech stack</li>
                  <li>Rate-limited posting to comply with platform guidelines</li>
                  <li>Error handling and retry mechanisms</li>
                  <li>Analytics tracking for engagement</li>
                </ul>
              </div>
            </div>
          </section>

          {/* Future Improvements */}
          <section className="mb-16">
            <h2 className="font-display text-2xl font-semibold text-surface-900 mb-4">
              Future Improvements
            </h2>
            <div className="bg-white rounded-xl p-6 shadow-sm ring-1 ring-surface-200">
              <ul className="list-disc list-inside space-y-2 text-surface-600 ml-4">
                <li>Enhanced event categorization using machine learning</li>
                <li>Real-time updates and notifications</li>
                <li>Integration with more social media platforms</li>
                <li>Personalized event recommendations</li>
                <li>Advanced search and filtering capabilities</li>
              </ul>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}

export default Documentation 