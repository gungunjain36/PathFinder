function Filter({ selectedType, setSelectedType, types }) {
  return (
    <div className="mb-12 flex justify-center">
      <div className="relative inline-block">
        <select
          value={selectedType}
          onChange={(e) => setSelectedType(e.target.value)}
          className="appearance-none bg-white text-surface-600 px-6 py-3 pr-12 rounded-full
                   ring-1 ring-surface-200 focus:ring-primary-500 focus:outline-none
                   cursor-pointer transition-all duration-300 font-medium
                   hover:bg-surface-50"
        >
          <option value="all">All Events</option>
          {types.map((type) => (
            <option key={type} value={type}>
              {type.charAt(0).toUpperCase() + type.slice(1)}s
            </option>
          ))}
        </select>
        <div className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-surface-400">
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7" />
          </svg>
        </div>
      </div>
    </div>
  )
}

export default Filter 