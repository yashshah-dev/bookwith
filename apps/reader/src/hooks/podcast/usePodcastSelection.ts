import { useEffect, useState } from 'react'

import { PodcastResponse } from '../../types/podcast'
import { findPodcastByStatus } from '../../utils/podcast'

interface UsePodcastSelectionParams {
  podcasts: PodcastResponse[]
  bookId?: string
}

interface UsePodcastSelectionReturn {
  selectedPodcast: PodcastResponse | null
  setSelectedPodcast: (podcast: PodcastResponse | null) => void
}

/**
 * Custom hook to manage automatic podcast selection logic
 * Priority: Completed > Processing > Failed
 */
export const usePodcastSelection = ({
  podcasts,
  bookId,
}: UsePodcastSelectionParams): UsePodcastSelectionReturn => {
  const [selectedPodcast, setSelectedPodcast] =
    useState<PodcastResponse | null>(null)

  // Reset selectedPodcast when book changes
  useEffect(() => {
    setSelectedPodcast(null)
  }, [bookId])

  // Automatically select the first available podcast
  useEffect(() => {
    if (
      podcasts.length > 0 &&
      (!selectedPodcast || selectedPodcast.book_id !== bookId)
    ) {
      // Prioritize completed podcasts
      const completedPodcast = findPodcastByStatus(podcasts, 'COMPLETED')
      if (completedPodcast && completedPodcast.audio_url) {
        setSelectedPodcast(completedPodcast)
        return
      }

      // Select processing podcast if available
      const processingPodcast = findPodcastByStatus(podcasts, 'PROCESSING')
      if (processingPodcast) {
        setSelectedPodcast(processingPodcast)
        return
      }

      // Select failed podcast if available
      const failedPodcast = findPodcastByStatus(podcasts, 'FAILED')
      if (failedPodcast) {
        setSelectedPodcast(failedPodcast)
        return
      }
    }
  }, [podcasts, selectedPodcast, bookId])

  return {
    selectedPodcast,
    setSelectedPodcast,
  }
}
