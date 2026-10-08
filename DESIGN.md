---
name: High-Visibility Accessibility System
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#3c494d'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f1f1f1'
  outline: '#6c797d'
  outline-variant: '#bbc9cd'
  surface-tint: '#00687a'
  primary: '#00687a'
  on-primary: '#ffffff'
  primary-container: '#0cc0df'
  on-primary-container: '#004a57'
  inverse-primary: '#41d7f7'
  secondary: '#6f5d00'
  on-secondary: '#ffffff'
  secondary-container: '#fed800'
  on-secondary-container: '#705e00'
  tertiary: '#5e5e5e'
  on-tertiary: '#ffffff'
  tertiary-container: '#b0afaf'
  on-tertiary-container: '#424242'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#abedff'
  primary-fixed-dim: '#41d7f7'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#ffe165'
  secondary-fixed-dim: '#e7c400'
  on-secondary-fixed: '#221b00'
  on-secondary-fixed-variant: '#544600'
  tertiary-fixed: '#e4e2e2'
  tertiary-fixed-dim: '#c8c6c6'
  on-tertiary-fixed: '#1b1c1c'
  on-tertiary-fixed-variant: '#464747'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
typography:
  display-hero:
    fontFamily: Plus Jakarta Sans
    fontSize: 160px
    fontWeight: '800'
    lineHeight: 160px
    letterSpacing: -0.04em
  display-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 120px
    fontWeight: '700'
    lineHeight: 120px
    letterSpacing: -0.02em
  headline-curr:
    fontFamily: Plus Jakarta Sans
    fontSize: 64px
    fontWeight: '700'
    lineHeight: 80px
  headline-next:
    fontFamily: Plus Jakarta Sans
    fontSize: 48px
    fontWeight: '600'
    lineHeight: 56px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '500'
    lineHeight: 40px
  label-caps:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-padding: 48px
  gutter-lg: 32px
  row-gap: 24px
  section-margin: 64px
---

## Brand & Style
This design system is engineered for the APAE (Association of Parents and Friends of the Exceptional) Call Display Panel. The primary objective is absolute legibility and functional clarity for individuals with varying degrees of cognitive and visual abilities. 

The style is **High-Contrast Minimalism**. It eschews decorative flourishes in favor of raw utility and structural order. By utilizing a reduced color palette and massive typographic scales, the UI ensures that critical information—such as queue numbers and room designations—is perceivable from across a large waiting area. The emotional response is one of reliability, inclusion, and calm efficiency.

## Colors
The palette is rooted in high-visibility functionalism.
- **Primary Cyan (#0CC0DF):** Used for "Success" states and active calls to provide a modern, high-contrast signal that stands out clearly against the neutral background.
- **Secondary Yellow (#FFD900):** Reserved for high-attention alerts, priority highlights, or current active ticket segments requiring immediate focus without the harshness of red.
- **Dark Grey (#555555):** Used for secondary information and structural boundaries to maintain contrast without the harshness of pure black in large blocks.
- **Light Background (#F4F4F4):** A soft neutral that reduces screen glare while maintaining a clean, modern aesthetic.
- **Text:** All critical call data must use `on-background` or high-contrast black (#000000) against white or high-visibility backgrounds to exceed WCAG AAA accessibility standards.

## Typography
We use **Plus Jakarta Sans** for its modern, geometric clarity and open counters, which prevent character blurring at a distance. 

The scale is intentionally oversized. The `display-hero` token is used exclusively for the current ticket number being called. `headline-curr` is used for the destination (e.g., "SALA 04"). All text must prioritize heavy weights (600-800) to ensure the stroke width is visible even in bright or poorly lit environments.

## Layout & Spacing
The layout follows a **Fixed Grid** model optimized for landscape TV displays (16:9). 
- **Main Stage:** Occupies 70% of the screen width, housing the current call.
- **Sidebar/History:** Occupies 30% of the screen, showing the last 3-4 called numbers.
- **Bottom Ticker:** A dedicated horizontal strip for institutional news or instructions.

Spacing is generous to prevent "visual crowding." High-contrast boundaries are created through 4px solid borders using the Dark Grey or Primary Cyan tokens rather than soft shadows.

## Elevation & Depth
In alignment with the minimalist and high-contrast requirements, this system uses **Low-Contrast Outlines** and **Tonal Layering** instead of shadows. 
- **Active Surface:** The current ticket container uses a pure white background with a thick (8px) Primary Cyan border.
- **Secondary Surface:** History items use a subtle 1px border or flat Light Background fills.
- **Zero Shadows:** Shadows are disabled to maintain the "flat" high-contrast look, ensuring shapes remain crisp and edges are clearly defined for users with visual impairments.

## Shapes
A "Rounded" (0.5rem) corner strategy is applied to all primary containers. This softens the "institutional" feel of the APAE environment while maintaining a structured, modern professional look. Large call-out boxes for ticket numbers use `rounded-xl` (1.5rem) to distinguish them as the most important interactive elements on the display.

## Components
### Call Card (Main)
The central component. Features a White background, 8px Cyan left-accent border, and the `display-hero` typography. The label "SENHA" (Ticket) appears in `label-caps` above the number.

### History List
Vertical list on the right. Each item is separated by a 2px `neutral_color_hex` divider. Uses `headline-next` for ticket numbers and `body-lg` for room names.

### Status Badge
Small pill-shaped containers used for priority types (e.g., "Idoso", "PCD"). Uses the Secondary Yellow background with Black text for maximum visibility.

### Notification Banner
A full-width bar at the bottom or top of the screen. Uses Primary Cyan background with White text for general announcements, or Secondary Yellow with Black text for urgent alerts.

### Destination Indicator
Large, bold text blocks that pair a room icon with a room number. The icon and text should share the same color (Dark Grey) to maintain a singular visual unit.