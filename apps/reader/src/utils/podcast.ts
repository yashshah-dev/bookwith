import { SPEED_OPTIONS } from '../constants/audio'
import { PODCAST_ERROR_KEYS } from '../constants/podcast'
import { PodcastResponse, PodcastStatus } from '../types/podcast'

/**
 * Format time in MM:SS format
 */
export const formatTime = (time: number): string => {
  if (isNaN(time)) return '0:00'
  const minutes = Math.floor(time / 60)
  const seconds = Math.floor(time % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
}

/**
 * Get the label for the specified value from playback speed options
 */
export const getSpeedLabel = (playbackRate: number): string => {
  const option = SPEED_OPTIONS.find((opt) => opt.value === playbackRate)
  return option?.label || '1x'
}

/**
 * Format volume as percentage
 */
export const formatVolumePercentage = (volume: number): string => {
  return `${Math.round(volume * 100)}%`
}

/**
 * Seek to audio position
 */
export const seekAudio = (
  audioElement: HTMLAudioElement,
  delta: number,
  duration: number,
  onTimeUpdate: (time: number) => void,
): void => {
  const newTime = Math.min(
    Math.max(0, audioElement.currentTime + delta),
    duration,
  )
  audioElement.currentTime = newTime
  onTimeUpdate(newTime)
}

/**
 * Get podcast with specified status from array
 */
export const findPodcastByStatus = (
  podcasts: PodcastResponse[],
  status: PodcastStatus,
): PodcastResponse | undefined => {
  return podcasts.find((p) => p.status === status)
}

/**
 * Get error message key based on error type
 */
export const getPodcastErrorKey = (error: unknown): string => {
  if (error instanceof Error) {
    if (error.message.includes('network')) {
      return PODCAST_ERROR_KEYS.NETWORK_ERROR
    }
    if (error.message.includes('audio') || error.message.includes('play')) {
      return PODCAST_ERROR_KEYS.PLAYBACK_FAILED
    }
    if (error.message.includes('generation')) {
      return PODCAST_ERROR_KEYS.GENERATION_FAILED
    }
  }
  return PODCAST_ERROR_KEYS.UNKNOWN_ERROR
}
