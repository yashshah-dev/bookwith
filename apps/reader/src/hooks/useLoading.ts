import { useRef } from 'react'

import {
  useLoadingState,
  useProgressManager,
  useTaskManager,
  UseTaskManagerOptions,
} from './loading'

export type UseLoadingOptions = UseTaskManagerOptions

/**
 * Integrated hook for managing loading state
 * Maintains traditional API for backward compatibility
 */
export function useLoading(options?: UseLoadingOptions) {
  const currentTaskIdRef = useRef<string | null>(null)

  const getCurrentTaskId = () => currentTaskIdRef.current
  const setCurrentTaskId = (id: string | null) => {
    currentTaskIdRef.current = id
  }

  const { isLoading, isGlobalLoading } = useLoadingState(getCurrentTaskId)
  const { updateProgress, updateSubTasks } =
    useProgressManager(getCurrentTaskId)
  const { startLoading, stopLoading } = useTaskManager(
    setCurrentTaskId,
    getCurrentTaskId,
    options,
  )

  return {
    startLoading,
    updateProgress,
    updateSubTasks,
    stopLoading,
    isLoading,
    isGlobalLoading,
  }
}
