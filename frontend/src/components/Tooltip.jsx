export function Tooltip({ children, content }) {
  return (
    <div className="group relative inline-block">
      {children}
      <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-3 py-1.5 
                    text-sm text-white bg-surface-900 rounded-lg opacity-0 
                    invisible group-hover:opacity-100 group-hover:visible
                    transition-all duration-200 whitespace-nowrap">
        {content}
        <div className="absolute top-full left-1/2 -translate-x-1/2 -mt-2 
                      border-4 border-transparent border-t-surface-900"></div>
      </div>
    </div>
  );
} 