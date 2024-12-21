import { useEffect, useState } from 'react'
import EventCard from './components/EventCard'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import Filter from './components/Filter'
import Documentation from './components/Documentation'
import { Routes, Route } from 'react-router-dom'

function App() {
  const [events, setEvents] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedType, setSelectedType] = useState('all')

  useEffect(() => {
    const fetchEvents = async () => {
      try {
        const response = await fetch('http://localhost:8000/results')
        const data = await response.json()
        if (data.status === 'success') {
          setEvents(data.data)
        }
        setLoading(false)
      } catch (error) {
        console.error('Error fetching events:', error)
        setLoading(false)
      }
    }

    fetchEvents()
  }, [])

  // Get unique event types
  const eventTypes = [...new Set(events.map(event => event.event_type))]

  // Filter events based on selected type
  const filteredEvents = selectedType === 'all' 
    ? events 
    : events.filter(event => event.event_type === selectedType)

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-2 border-primary-500 border-t-transparent"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-white to-primary-50">
      <Navbar />
      <Routes>
        <Route path="/" element={
          <>
            <Hero />
            <main className="container mx-auto px-4 py-16">
              <Filter 
                selectedType={selectedType} 
                setSelectedType={setSelectedType}
                types={eventTypes}
              />
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {filteredEvents.map((event, index) => (
                  <EventCard key={index} event={event} />
                ))}
              </div>
            </main>
          </>
        } />
        <Route path="/docs" element={<Documentation />} />
      
      </Routes>
    </div>
  )
}

export default App
