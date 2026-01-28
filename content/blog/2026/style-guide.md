---
title: Style Guide
date: 2026-01-28
description: A reference for the colors, typography, and design tokens used in this blog.
---

<style>
.swatch-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: var(--space-md);
  margin: var(--space-lg) 0;
}

.swatch {
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.swatch-color {
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.swatch-info {
  background: var(--bg-surface);
  padding: var(--space-sm);
  font-size: var(--text-sm);
}

.swatch-name {
  font-weight: 600;
  color: var(--text-primary);
}

.swatch-hex {
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.typography-sample {
  padding: var(--space-lg);
  background: var(--bg-surface);
  border-radius: var(--border-radius);
  margin: var(--space-md) 0;
}

.typography-sample h1 { font-size: 2rem; margin-bottom: var(--space-sm); }
.typography-sample h2 { font-size: 1.5rem; margin-bottom: var(--space-sm); }
.typography-sample h3 { font-size: 1.25rem; margin-bottom: var(--space-sm); }
.typography-sample p { margin-bottom: var(--space-sm); }
.typography-sample code {
  background: var(--bg-code);
  padding: 2px 6px;
  border-radius: var(--border-radius-sm);
  font-family: var(--font-mono);
  font-size: 0.9em;
}

.spacing-scale {
  margin: var(--space-lg) 0;
}

.spacing-block {
  background: var(--color-primary);
  margin-bottom: var(--space-sm);
  border-radius: 2px;
}
</style>

# Blog Style Guide

A reference for the colors, typography, and design tokens used in this blog.

---

## Color Palette

### Primary Colors

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #009988;">#009988</div>
    <div class="swatch-info">
      <div class="swatch-name">Primary</div>
      <div class="swatch-hex">Brand, sidebar, links</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #00bb88;">#00bb88</div>
    <div class="swatch-info">
      <div class="swatch-name">Primary Bright</div>
      <div class="swatch-hex">Hover states</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #dd8800;">#dd8800</div>
    <div class="swatch-info">
      <div class="swatch-name">Secondary</div>
      <div class="swatch-hex">Highlights, CTAs</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #eebb99;">#eebb99</div>
    <div class="swatch-info">
      <div class="swatch-name">Secondary Bright</div>
      <div class="swatch-hex">Soft highlights</div>
    </div>
  </div>
</div>

### Neutrals

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #333333; color: white;">#333333</div>
    <div class="swatch-info">
      <div class="swatch-name">Text Primary</div>
      <div class="swatch-hex">Main text</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #666666; color: white;">#666666</div>
    <div class="swatch-info">
      <div class="swatch-name">Text Secondary</div>
      <div class="swatch-hex">Meta info</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #999999; color: white;">#999999</div>
    <div class="swatch-info">
      <div class="swatch-name">Text Muted</div>
      <div class="swatch-hex">Placeholders</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #fafefd; color: #333; border: 1px solid #ddd;">#fafefd</div>
    <div class="swatch-info">
      <div class="swatch-name">Background</div>
      <div class="swatch-hex">Page bg</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #ffffff; color: #333; border: 1px solid #ddd;">#ffffff</div>
    <div class="swatch-info">
      <div class="swatch-name">Surface</div>
      <div class="swatch-hex">Cards, containers</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #f5f5f5; color: #333; border: 1px solid #ddd;">#f5f5f5</div>
    <div class="swatch-info">
      <div class="swatch-name">Code Background</div>
      <div class="swatch-hex">Code blocks</div>
    </div>
  </div>
</div>

### Link Colors

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #006699;">#006699</div>
    <div class="swatch-info">
      <div class="swatch-name">Link Default</div>
      <div class="swatch-hex">Standard links</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #dd8800;">#dd8800</div>
    <div class="swatch-info">
      <div class="swatch-name">Link Hover</div>
      <div class="swatch-hex">Hover state</div>
    </div>
  </div>
</div>

---

## Complementary Color Suggestions

These colors work well with your existing `#009988` primary and can be used for accents, data visualizations, or thematic variations.

### Teal/Green Analogous (Natural Feel)

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #006666;">#006666</div>
    <div class="swatch-info">
      <div class="swatch-name">Deep Teal</div>
      <div class="swatch-hex">Dark accents, footer</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #8FA998;">#8FA998</div>
    <div class="swatch-info">
      <div class="swatch-name">Sage Green</div>
      <div class="swatch-hex">Soft backgrounds</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #7FC5B4;">#7FC5B4</div>
    <div class="swatch-info">
      <div class="swatch-name">Seafoam</div>
      <div class="swatch-hex">Secondary buttons</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #2D5A45;">#2D5A45</div>
    <div class="swatch-info">
      <div class="swatch-name">Forest</div>
      <div class="swatch-hex">Dark mode accents</div>
    </div>
  </div>
</div>

### Warm Accent Colors (Complementary)

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #CC6633;">#CC6633</div>
    <div class="swatch-info">
      <div class="swatch-name">Burnt Orange</div>
      <div class="swatch-hex">Highlights, alerts</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #E6A833;">#E6A833</div>
    <div class="swatch-info">
      <div class="swatch-name">Golden Yellow</div>
      <div class="swatch-hex">Success, awards</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #E07B5B;">#E07B5B</div>
    <div class="swatch-info">
      <div class="swatch-name">Coral</div>
      <div class="swatch-hex">Notifications</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #F5C4A0;">#F5C4A0</div>
    <div class="swatch-info">
      <div class="swatch-name">Peach</div>
      <div class="swatch-hex">Soft backgrounds</div>
    </div>
  </div>
</div>

### Blue Accents (Trust/Professional)

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #006699;">#006699</div>
    <div class="swatch-info">
      <div class="swatch-name">Ocean Blue</div>
      <div class="swatch-hex">Links (existing)</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #5A7D8C;">#5A7D8C</div>
    <div class="swatch-info">
      <div class="swatch-name">Slate</div>
      <div class="swatch-hex">Muted accents</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #7AB8D9;">#7AB8D9</div>
    <div class="swatch-info">
      <div class="swatch-name">Sky</div>
      <div class="swatch-hex">Gentle highlights</div>
    </div>
  </div>
</div>

### Purple/Violet (Creative)

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #9B7BB8;">#9B7BB8</div>
    <div class="swatch-info">
      <div class="swatch-name">Lavender</div>
      <div class="swatch-hex">Thematic accents</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #5A3A6E;">#5A3A6E</div>
    <div class="swatch-info">
      <div class="swatch-name">Deep Plum</div>
      <div class="swatch-hex">Dark mode accents</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #D4C5E8;">#D4C5E8</div>
    <div class="swatch-info">
      <div class="swatch-name">Soft Lilac</div>
      <div class="swatch-hex">Background tints</div>
    </div>
  </div>
</div>

### Grays (Neutral Expansion)

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #2A2A2A; color: white;">#2A2A2A</div>
    <div class="swatch-info">
      <div class="swatch-name">Charcoal</div>
      <div class="swatch-hex">Dark mode text</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #8A8A8A; color: white;">#8A8A8A</div>
    <div class="swatch-info">
      <div class="swatch-name">Stone</div>
      <div class="swatch-hex">Muted text</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #9E9A95; color: white;">#9E9A95</div>
    <div class="swatch-info">
      <div class="swatch-name">Warm Gray</div>
      <div class="swatch-hex">Dividers, borders</div>
    </div>
  </div>
</div>

---

## Typography

### Font Families

| Role | Font | Fallback |
|------|------|----------|
| Headings | `IBM Plex Sans` | system-ui, sans-serif |
| Body | `IBM Plex Serif` | Georgia, serif |
| Code | `IBM Plex Mono` | monospace |
| Navigation | "Courier Prime Sans" | system-ui, sans-serif |

### Typography Scale

<div class="typography-sample">
  <h1 style="font-family: var(--font-heading);">Heading 1 — The Quick Brown Fox</h1>
  <h2 style="font-family: var(--font-heading);">Heading 2 — Pack my box with five dozen liquor jugs</h2>
  <h3 style="font-family: var(--font-heading);">Heading 3 — How vexingly quick daft zebras jump</h3>
  <p style="font-family: var(--font-body);">Body text — The quick brown fox jumps over the lazy dog. This is sample body text using IBM Plex Serif with a comfortable line-height of 1.6 for readability.</p>
  <p style="font-family: var(--font-body); font-size: var(--text-sm);">Small text — Metadata, captions, and timestamps use smaller text at 0.875rem.</p>
  <p><code>Inline code</code> uses IBM Plex Mono with a light gray background.</p>
</div>

### Font Sizes

| Variable | Rem | Pixels | Usage |
|----------|-----|--------|-------|
| `text-sm` | 0.875rem | 14px | Metadata, captions |
| `text-base` | 1rem | 16px | Body text |
| `text-lg` | 1.125rem | 18px | Lead paragraphs |
| `text-xl` | 1.25rem | 20px | Small headings |
| `text-2xl` | 1.5rem | 24px | Section headings |
| `text-3xl` | 2rem | 32px | Page titles |

---

## Spacing Scale

<div class="spacing-scale">
  <div class="spacing-block" style="width: 4px; height: var(--space-xs);"></div>
  <code>--space-xs</code> (4px)
  <div class="spacing-block" style="width: 8px; height: var(--space-sm);"></div>
  <code>--space-sm</code> (8px)
  <div class="spacing-block" style="width: 16px; height: var(--space-md);"></div>
  <code>--space-md</code> (16px)
  <div class="spacing-block" style="width: 24px; height: var(--space-lg);"></div>
  <code>--space-lg</code> (24px)
  <div class="spacing-block" style="width: 32px; height: var(--space-xl);"></div>
  <code>--space-xl</code> (32px)
  <div class="spacing-block" style="width: 48px; height: var(--space-2xl);"></div>
  <code>--space-2xl</code> (48px)
</div>

---

## Border Radius

| Variable | Pixels | Usage |
|----------|--------|-------|
| `--border-radius-sm` | 4px | Buttons, small elements |
| `--border-radius` | 8px | Cards, containers |
| `--border-radius-lg` | 12px | Modals, large containers |

<div style="display: flex; gap: 20px; margin: 20px 0;">
  <div style="width: 40px; height: 40px; background: #009988; border-radius: 4px;"></div>
  <div style="width: 40px; height: 40px; background: #009988; border-radius: 8px;"></div>
  <div style="width: 40px; height: 40px; background: #009988; border-radius: 12px;"></div>
</div>

---

## Shadows

| Variable | CSS | Usage |
|----------|-----|-------|
| `--shadow-sm` | `0 1px 3px rgba(0,0,0,0.08)` | Subtle depth |
| `--shadow-md` | `0 4px 12px rgba(0,0,0,0.1)` | Cards, dropdowns |
| `--shadow-lg` | `0 8px 24px rgba(0,0,0,0.12)` | Modals, popups |

<div style="display: flex; gap: 40px; margin: 20px 0;">
  <div style="width: 80px; height: 80px; background: white; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);"></div>
  <div style="width: 80px; height: 80px; background: white; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);"></div>
  <div style="width: 80px; height: 80px; background: white; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.12);"></div>
</div>

---

## Transitions

| Variable | CSS | Usage |
|----------|-----|-------|
| `--transition-fast` | `150ms ease` | Hover effects |
| `--transition-normal` | `250ms ease` | Animations |

---

## Layout

| Property | Value |
|----------|-------|
| Sidebar width | `60px` |
| Content max-width | `800px` |
| Container padding | `5vw` |

---

## Dark Mode Adjustments

When dark mode is active (`[data-theme="dark"]`):

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #1a1d1a; color: white;">#1a1d1a</div>
    <div class="swatch-info">
      <div class="swatch-name">Background</div>
      <div class="swatch-hex">Light: #fafefd</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #222522; color: white;">#222522</div>
    <div class="swatch-info">
      <div class="swatch-name">Surface</div>
      <div class="swatch-hex">Light: #ffffff</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #2a2d2a; color: white;">#2a2d2a</div>
    <div class="swatch-info">
      <div class="swatch-name">Code BG</div>
      <div class="swatch-hex">Light: #f5f5f5</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #e0e0e0; color: #333;">#e0e0e0</div>
    <div class="swatch-info">
      <div class="swatch-name">Text Primary</div>
      <div class="swatch-hex">Light: #333333</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #b0b0b0; color: #333;">#b0b0b0</div>
    <div class="swatch-info">
      <div class="swatch-name">Text Secondary</div>
      <div class="swatch-hex">Light: #666666</div>
    </div>
  </div>
</div>

---

## Data Visualization Colors

<div class="swatch-grid">
  <div class="swatch">
    <div class="swatch-color" style="background: #009988;">#009988</div>
    <div class="swatch-info">
      <div class="swatch-name">Flight Routes</div>
      <div class="swatch-hex">Map route lines</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #D96040;">#D96040</div>
    <div class="swatch-info">
      <div class="swatch-name">Visited Places</div>
      <div class="swatch-hex">Map markers</div>
    </div>
  </div>
  <div class="swatch">
    <div class="swatch-color" style="background: #dd8800;">#dd8800</div>
    <div class="swatch-info">
      <div class="swatch-name">Airports</div>
      <div class="swatch-hex">Endpoints</div>
    </div>
  </div>
</div>

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
