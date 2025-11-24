import { useRef } from 'react'

import { LONG_PRESS } from '../constants/audio'

interface LongPressOptions {
  interval?: number
}

interface LongPressHandlers {
  onPointerDown: () => void
  onPointerUp: () => void
  onPointerLeave: () => void
}

/**
 * Custom hook to handle long press operations
 * @param action Function to execute
 * @param options Option settings
 * @returns Event handlers
 */
export const useLongPress = (
  action: () => void,
  options: LongPressOptions = {},
): LongPressHandlers => {
  const timer = useRef<NodeJS.Timeout | null>(null)
  const { interval = LONG_PRESS.DEFAULT_INTERVAL } = options

  const start = () => {
    // Execute once initially
    action()
    // Continue executing at intervals
    timer.current = setInterval(action, interval)
  }

  const stop = () => {
    if (timer.current) {
      clearInterval(timer.current)
      timer.current = null
    }
  }

  return {
    onPointerDown: start,
    onPointerUp: stop,
    onPointerLeave: stop,
  }
}
