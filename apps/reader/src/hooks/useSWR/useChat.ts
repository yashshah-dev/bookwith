import useSWR from 'swr'

import { components } from '../../lib/openapi-schema/schema'

import { fetcher } from './fetcher'

/**
 * SWR hook to get chat list associated with user ID
 * @param userId User ID (does not fetch if null)
 */
export const useGetUserChats = (userId: string | null) => {
  const { data, error, isValidating, mutate } = useSWR<
    components['schemas']['ChatsResponse']
  >(
    // Only fetch when userId is not null
    userId
      ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/chats/user/${userId}`
      : null,
    fetcher,
  )

  return {
    chats: data,
    error,
    isLoading: isValidating,
    mutateChats: mutate,
  }
}

/**
 * SWR hook to get message list associated with chat ID
 * @param chatId Chat ID (does not fetch if null)
 */
export const useGetChatMessages = (chatId: string | null) => {
  const { data, error, isValidating, mutate } = useSWR<
    components['schemas']['MessageListResponse']
  >(
    chatId
      ? `${process.env.NEXT_PUBLIC_API_BASE_URL}/messages/${chatId}`
      : null,
    fetcher,
  )

  return {
    messages: data?.messages || [],
    error,
    isLoading: isValidating,
    mutateMessages: mutate,
  }
}
