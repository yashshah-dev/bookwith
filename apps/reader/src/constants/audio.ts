interface SpeedOption {
  value: number
  label: string
}

// Audio control related constants
export const AUDIO_CONTROLS = {
  SKIP_SECONDS: 10, // Seconds to skip
  VOLUME_STEP: 0.1, // Volume adjustment step
  DEFAULT_VOLUME: 1.0, // Default volume
  MIN_VOLUME: 0, // Minimum volume
  MAX_VOLUME: 1, // Maximum volume
} as const

// Long press related constants
export const LONG_PRESS = {
  DEFAULT_INTERVAL: 200, // Interval during long press (milliseconds)
  INITIAL_DELAY: 500, // Delay for long press detection (milliseconds)
} as const

// Playback speed options
export const SPEED_OPTIONS: SpeedOption[] = [
  { value: 0.5, label: '0.5x' },
  { value: 0.75, label: '0.75x' },
  { value: 1, label: '1x' },
  { value: 1.25, label: '1.25x' },
  { value: 1.5, label: '1.5x' },
  { value: 2, label: '2x' },
]

// Audio-related key constants
export const AUDIO_EVENTS = {
  TIME_UPDATE: 'timeupdate',
  LOADED_METADATA: 'loadedmetadata',
  ENDED: 'ended',
  LOAD_START: 'loadstart',
  CAN_PLAY: 'canplay',
  ERROR: 'error',
} as const

// Volume slider related constants
export const VOLUME_SLIDER = {
  MIN: 0,
  MAX: 1,
  STEP: 0.01,
} as const

// Audio file related constants
export const AUDIO_FILE = {
  PRELOAD: 'metadata' as const,
  CROSSORIGIN: 'anonymous' as const,
}
