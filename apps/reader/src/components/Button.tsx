import { ComponentProps, forwardRef } from 'react'
import { IconType } from 'react-icons'

import { cn } from '../lib/utils'

import { Button as ShadcnButton } from './ui/button'

// Re-export shadcn-ui Button to maintain compatibility with existing code
export const Button = ShadcnButton

// Implement IconButton using shadcn-ui Button
interface IconButtonProps extends Omit<ComponentProps<typeof Button>, 'size'> {
  Icon: IconType
  size?: number
}

export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(
  ({ className, Icon, size = 16, ...props }, ref) => {
    return (
      <Button
        variant="ghost"
        size="icon"
        className={cn('h-6 w-6', className)}
        ref={ref}
        {...props}
      >
        <Icon size={size} />
      </Button>
    )
  },
)

IconButton.displayName = 'IconButton'
