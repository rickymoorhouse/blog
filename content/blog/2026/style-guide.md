# Blog Style Guide

A reference for the colors, typography, and design tokens used in this blog.

---

## Color Palette

### Primary Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Primary | `#009988` | Brand color, links, accents, sidebar |
| Primary Bright | `#00bb88` | Hover states, active links |
| Secondary | `#dd8800` | Highlights, call-to-actions |
| Secondary Bright | `#eebb99` | Subtle highlights |

### Neutrals

| Color | Hex | Usage |
|-------|-----|-------|
| Text Primary | `#333333` | Main body text, headings |
| Text Secondary | `#666666` | Meta info, captions |
| Text Muted | `#999999` | Placeholders, timestamps |
| Background | `#fafefd` | Page background |
| Surface | `#ffffff` | Cards, containers |
| Code Background | `#f5f5f5` | Code blocks |

### Link Colors

| State | Hex |
|-------|-----|
| Default | `#006699` |
| Hover | `#dd8800` |

---

## Typography

### Font Families

| Role | Font | Fallback |
|------|------|----------|
| Headings | IBM Plex Sans | system-ui, sans-serif |
| Body | IBM Plex Serif | Georgia, serif |
| Code | IBM Plex Mono | monospace |
| Navigation | "Courier Prime Sans" | system-ui, sans-serif |

### Font Sizes

| Size | Rem | Usage |
|------|-----|-------|
| text-sm | 0.875rem | Metadata, captions |
| text-base | 1rem | Body text |
| text-lg | 1.125rem | Lead paragraphs |
| text-xl | 1.25rem | Small headings |
| text-2xl | 1.5rem | Section headings |
| text-3xl | 2rem | Page titles |

### Line Height
- Body text: 1.6
- Headings: 1.3

---

## Complementary Color Suggestions

These colors work well with your existing `#009988` primary and can be used for accents, data visualizations, or thematic variations.

### Teal/Green Analogous (Natural Feel)

| Color | Hex | Use Case |
|-------|-----|---------|
| Deep Teal | `#006666` | Darker accents, footer |
| Sage Green | `#8FA998` | Soft backgrounds, cards |
| Seafoam | `#7FC5B4` | Secondary buttons |
| Forest | `#2D5A45` | Dark mode accents |

### Warm Accent Colors (Complementary)

| Color | Hex | Use Case |
|-------|-----|---------|
| Burnt Orange | `#CC6633` | Highlights, alerts |
| Golden Yellow | `#E6A833` | Success states, awards |
| Coral | `#E07B5B` | Notifications, errors |
| Peach | `#F5C4A0` | Soft backgrounds |

### Blue Accents (Trust/Professional)

| Color | Hex | Use Case |
|-------|-----|---------|
| Ocean Blue | `#006699` | Already used for links |
| Slate | `#5A7D8C` | Muted accents |
| Sky | `#7AB8D9` | Gentle highlights |

### Purple/Violet (Creative)

| Color | Hex | Use Case |
|-------|-----|---------|
| Lavender | `#9B7BB8` | Thematic accents |
| Deep Plum | `#5A3A6E` | Dark mode accents |
| Soft Lilac | `#D4C5E8` | Background tints |

### Grays (Neutral Expansion)

| Color | Hex | Use Case |
|-------|-----|---------|
| Charcoal | `#2A2A2A` | Dark mode text |
| Stone | `#8A8A8A` | Muted text |
| Warm Gray | `#9E9A95` | Dividers, borders |

---

## Color Combinations

### Light Mode
- **Primary + White**: Clean, professional
- **Primary + Sage Green**: Natural, calm
- **Secondary + Light Gray**: Warm, approachable

### Dark Mode
- **Primary + Deep Teal**: Sophisticated
- **Forest + Charcoal**: Elegant, readable
- **Lavender + Dark Surface**: Creative accent

### Data Visualization
- **Route Lines**: `#009988` (primary)
- **Visited Places**: `#D96040` (tertiary)
- **Airports**: `#dd8800` (secondary)
- **Backgrounds**: `#f5f5f5` to `#ffffff`

---

## Spacing Scale

| Variable | Rem | Pixels |
|----------|-----|--------|
| --space-xs | 0.25rem | 4px |
| --space-sm | 0.5rem | 8px |
| --space-md | 1rem | 16px |
| --space-lg | 1.5rem | 24px |
| --space-xl | 2rem | 32px |
| --space-2xl | 3rem | 48px |

---

## Border Radius

| Variable | Pixels | Usage |
|----------|--------|-------|
| --border-radius-sm | 4px | Buttons, small elements |
| --border-radius | 8px | Cards, containers |
| --border-radius-lg | 12px | Modals, large containers |

---

## Shadows

| Variable | Value | Usage |
|----------|-------|-------|
| --shadow-sm | 0 1px 3px rgba(0,0,0,0.08) | Subtle depth |
| --shadow-md | 0 4px 12px rgba(0,0,0,0.1) | Cards, dropdowns |
| --shadow-lg | 0 8px 24px rgba(0,0,0,0.12) | Modals, popups |

---

## Transitions

| Variable | Value | Usage |
|----------|-------|-------|
| --transition-fast | 150ms ease | Hover effects |
| --transition-normal | 250ms ease | Animations |

---

## Layout

| Property | Value |
|----------|-------|
| Sidebar width | 60px |
| Content max-width | 800px |
| Container padding | 5vw |

---

## Dark Mode Adjustments

When dark mode is active:

| Property | Light | Dark |
|----------|-------|------|
| Background | `#fafefd` | `#1a1d1a` |
| Surface | `#ffffff` | `#222522` |
| Code bg | `#f5f5f5` | `#2a2d2a` |
| Text primary | `#333333` | `#e0e0e0` |
| Text secondary | `#666666` | `#b0b0b0` |

---

## Usage Examples

### Button
```css
.btn-primary {
  background: var(--color-primary);
  color: white;
  border-radius: var(--border-radius-sm);
  padding: var(--space-sm) var(--space-md);
  transition: background var(--transition-fast);
}

.btn-primary:hover {
  background: var(--color-primary-bright);
}
```

### Card
```css
.card {
  background: var(--bg-surface);
  border-radius: var(--border-radius);
  padding: var(--space-lg);
  box-shadow: var(--shadow-sm);
}
```

### Link
```css
a {
  color: var(--link-color);
  transition: color var(--transition-fast);
}

a:hover {
  color: var(--link-hover);
}
```
