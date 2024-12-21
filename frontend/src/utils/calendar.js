export function createGoogleCalendarUrl(event) {
  // Format dates for Google Calendar URL
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toISOString().replace(/-|:|\.\d\d\d/g, '');
  };

  // Create start and end dates
  const startDate = formatDate(event.date.start);
  const endDate = formatDate(event.date.end);

  // Build calendar URL with event details
  const calendarUrl = new URL('https://calendar.google.com/calendar/render');
  calendarUrl.searchParams.append('action', 'TEMPLATE');
  calendarUrl.searchParams.append('text', event.title);
  calendarUrl.searchParams.append('details', 
    `${event.description}\n\n` +
    `Event Type: ${event.event_type}\n` +
    `Mode: ${event.mode}\n` +
    `Tech Stack: ${event.tech_stack.join(', ')}\n\n` +
    `Prize Pool: ${event.prizes.total_pool}\n` +
    `Source: ${event.source_url}`
  );
  calendarUrl.searchParams.append('dates', `${startDate}/${endDate}`);
  calendarUrl.searchParams.append('location', event.mode);

  return calendarUrl.toString();
} 