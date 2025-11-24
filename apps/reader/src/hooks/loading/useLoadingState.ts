import { useAtomValue } from 'jotai'

import { isGlobalLoadingAtom, loadingTasksAtom } from '../../store/loading'

/**
 * Hook for managing basic loading state
 */
export function useLoadingState(getCurrentTaskId: () => string | null) {
  const tasks = useAtomValue(loadingTasksAtom)
  const isGlobalLoading = useAtomValue(isGlobalLoadingAtom)

  // Whether this hook instance is loading
  const currentTaskId = getCurrentTaskId()
  const isLoading = currentTaskId ? tasks.has(currentTaskId) : false

  return {
    tasks,
    isGlobalLoading,
    isLoading,
  }
}
