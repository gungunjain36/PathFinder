function EventCard({ event }) {
  const capitalizeFirstLetter = (string) => {
    return string.charAt(0).toUpperCase() + string.slice(1);
  };

  const Badge = ({ type }) => (
    <span className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap
      ${type === 'hackathon' ? 'bg-blue-500/10 text-blue-400 ring-1 ring-blue-400/30' :
        type === 'conference' ? 'bg-purple-500/10 text-purple-400 ring-1 ring-purple-400/30' :
        'bg-gray-500/10 text-gray-400 ring-1 ring-gray-400/30'}`}
    >
      {capitalizeFirstLetter(type)}
    </span>
  );

  const InfoItem = ({ icon, text, color = "blue" }) => (
    <div className="flex items-center gap-2 text-sm text-gray-400">
      <span className={`text-${color}-400 flex-shrink-0`}>{icon}</span>
      <span className="truncate">{text}</span>
    </div>
  );

  const TechBadge = ({ tech }) => (
    <span className="px-2 py-1 bg-gray-800/50 text-gray-300 rounded-md text-xs ring-1 ring-gray-700">
      {capitalizeFirstLetter(tech)}
    </span>
  );

  const ActionButton = ({ href, primary, children }) => (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium
        transition-all duration-300 hover:scale-[1.02] flex-1 justify-center
        ${primary 
          ? 'bg-blue-500/20 text-blue-400 ring-1 ring-blue-500/30 hover:bg-blue-500/30' 
          : 'bg-gray-800/50 text-gray-400 ring-1 ring-gray-700 hover:bg-gray-700/50'}`}
    >
      {children}
    </a>
  );

  return (
    <div className="group bg-gray-900/50 backdrop-blur-sm rounded-xl overflow-hidden
                    ring-1 ring-gray-800 hover:ring-gray-700
                    transition-all duration-300 h-full flex flex-col">
      <div className="p-5 flex flex-col flex-grow">
        {/* Header Section */}
        <div className="mb-4">
          <div className="flex justify-between items-start gap-4 mb-2">
            <h2 className="text-lg font-medium text-gray-200 group-hover:text-blue-400 
                         transition-colors duration-300 line-clamp-1">
              {event.title}
            </h2>
            <Badge type={event.event_type} />
          </div>
          <p className="text-sm text-gray-400 line-clamp-2 min-h-[40px]">
            {event.description}
          </p>
        </div>

        {/* Info Section */}
        <div className="space-y-2.5 mb-4">
          <InfoItem 
            icon={<CalendarIcon />}
            text={`${event.date.start} - ${event.date.end}`}
          />
          <InfoItem 
            icon={<LocationIcon />}
            text={capitalizeFirstLetter(event.mode)}
            color="purple"
          />
          {event.prizes.total_pool !== "unknown" && (
            <InfoItem 
              icon={<PrizeIcon />}
              text={`Prize: ${event.prizes.total_pool}`}
              color="green"
            />
          )}
        </div>

        {/* Tech Stack Section */}
        <div className="flex-grow">
          <div className="flex flex-wrap gap-1.5">
            {event.tech_stack.slice(0, 3).map((tech, index) => (
              <TechBadge key={index} tech={tech} />
            ))}
            {event.tech_stack.length > 3 && (
              <span className="text-xs text-gray-500 self-center">
                +{event.tech_stack.length - 3}
              </span>
            )}
          </div>
        </div>

        {/* Actions Section */}
        <div className="flex gap-2 mt-4 pt-4 border-t border-gray-800">
          {event.registration.url !== "unknown" ? (
            <ActionButton href={event.registration.url} primary>
              <span>Register</span>
              <ArrowIcon />
            </ActionButton>
          ) : (
            <ActionButton href={event.source_url}>
              <LinkIcon />
              <span>View Source</span>
            </ActionButton>
          )}
        </div>
      </div>
    </div>
  )
}

// Icons Components
const CalendarIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
          d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
  </svg>
);

const LocationIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
          d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
          d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
  </svg>
);

const PrizeIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
          d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);

const ArrowIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
          d="M13 7l5 5m0 0l-5 5m5-5H6" />
  </svg>
);

const LinkIcon = () => (
  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" 
          d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
  </svg>
);

export default EventCard