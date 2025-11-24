import { useEffect, useRef } from 'react'

type MayCallable<T> = T | (() => T)
type Maybe<T> = T | undefined | null
type Options = boolean | EventListenerOptions

// Implemented using union types for a single function signature
export function useEventListener<K extends keyof WindowEventMap>(
  targetOrType: K | MayCallable<Maybe<EventTarget>>,
  listenerOrType: ((this: any, e: WindowEventMap[K]) => void) | keyof any,
  optionsOrListener?: Options | ((e: any) => void),
  maybeOptions?: Options,
): void {
  let target: MayCallable<Maybe<EventTarget>>
  let type: string
  let listener: (e: any) => void
  let options: Options | undefined

  if (typeof targetOrType === 'string') {
    // For window events
    type = targetOrType as string
    listener = listenerOrType as (e: any) => void
    options = optionsOrListener as Options | undefined
    target = globalThis
  } else {
    // For target-specified events
    target = targetOrType
    type = listenerOrType as string
    listener = optionsOrListener as (e: any) => void
    options = maybeOptions
  }

  const listenerRef = useRef(listener)
  listenerRef.current = listener

  useEffect(() => {
    const _listener = (e: any) => listenerRef.current(e)
    const _target = typeof target === 'function' ? target() : target

    // Execute only if _target is not null or undefined and has addEventListener method
    if (_target && typeof _target.addEventListener === 'function') {
      _target.addEventListener(type, _listener, options)

      return () => {
        if (_target && typeof _target.removeEventListener === 'function') {
          _target.removeEventListener(type, _listener, options)
        }
      }
    }

    return undefined
  }, [options, target, type])
}
