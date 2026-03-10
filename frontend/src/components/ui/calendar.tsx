import { useState } from 'react'
import {
  startOfMonth,
  endOfMonth,
  startOfWeek,
  endOfWeek,
  addDays,
  addMonths,
  subMonths,
  isSameMonth,
  isSameDay,
  isToday,
  format,
  type Locale,
} from 'date-fns'
import { ChevronLeftIcon, ChevronRightIcon } from 'lucide-react'
import { cn } from '@/lib/utils'

interface CalendarProps {
  mode?: 'single'
  selected?: Date
  defaultMonth?: Date
  locale?: Locale
  onSelect?: (date: Date | undefined) => void
  className?: string
}

function Calendar({
  selected,
  defaultMonth,
  locale,
  onSelect,
  className,
}: CalendarProps) {
  const [viewMonth, setViewMonth] = useState(defaultMonth ?? selected ?? new Date())

  const monthStart = startOfMonth(viewMonth)
  const monthEnd = endOfMonth(viewMonth)
  const calStart = startOfWeek(monthStart, { locale })
  const calEnd = endOfWeek(monthEnd, { locale })

  const weeks: Date[][] = []
  let day = calStart
  while (day <= calEnd) {
    const week: Date[] = []
    for (let i = 0; i < 7; i++) {
      week.push(day)
      day = addDays(day, 1)
    }
    weeks.push(week)
  }

  const weekdayLabels: string[] = []
  for (let i = 0; i < 7; i++) {
    weekdayLabels.push(format(addDays(calStart, i), 'EEEEEE', { locale }))
  }

  return (
    <div className={cn('p-3', className)}>
      {/* Header: nav + month label */}
      <div className="flex items-center justify-between mb-3">
        <button
          type="button"
          onClick={() => setViewMonth(subMonths(viewMonth, 1))}
          className="size-7 inline-flex items-center justify-center rounded-lg border border-border bg-transparent text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
        >
          <ChevronLeftIcon className="size-4" />
        </button>
        <span className="text-sm font-medium text-foreground capitalize">
          {format(viewMonth, 'LLLL yyyy', { locale })}
        </span>
        <button
          type="button"
          onClick={() => setViewMonth(addMonths(viewMonth, 1))}
          className="size-7 inline-flex items-center justify-center rounded-lg border border-border bg-transparent text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-colors"
        >
          <ChevronRightIcon className="size-4" />
        </button>
      </div>

      {/* Weekday headers */}
      <div className="grid grid-cols-7 mb-1">
        {weekdayLabels.map((label, i) => (
          <div key={i} className="text-center text-[11px] font-medium text-muted-foreground py-1">
            {label}
          </div>
        ))}
      </div>

      {/* Day grid */}
      <div className="grid grid-cols-7">
        {weeks.map((week, wi) =>
          week.map((d, di) => {
            const inMonth = isSameMonth(d, viewMonth)
            const isSelected = selected && isSameDay(d, selected)
            const today = isToday(d)

            return (
              <button
                key={`${wi}-${di}`}
                type="button"
                onClick={() => onSelect?.(d)}
                className={cn(
                  'size-8 inline-flex items-center justify-center rounded-lg text-sm transition-colors',
                  !inMonth && 'text-muted-foreground/40',
                  inMonth && !isSelected && 'text-foreground hover:bg-muted/60',
                  today && !isSelected && 'bg-accent text-accent-foreground font-medium',
                  isSelected && 'bg-primary text-primary-foreground font-semibold',
                )}
              >
                {d.getDate()}
              </button>
            )
          }),
        )}
      </div>
    </div>
  )
}

export { Calendar }
export type { CalendarProps }
