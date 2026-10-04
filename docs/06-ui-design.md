# Chapter 6: User Interface & Experience Design

## 6.1 Theme & Design System
The dashboard UI follows modern data-dense dark theme principles tailored for transit command centers and urban analytics:
- **Background Foundation**: Deep Slate Navy (`#080c14`, `#0f172a`) providing high contrast for analytical elements.
- **Surface & Cards**: Glassmorphism cards (`rgba(18, 25, 43, 0.85)`) with subtle hairline borders (`rgba(255, 255, 255, 0.08)`).
- **Transit Accent Palette**:
  - *Electric Cyan (`#00d2ff`)*: Primary brand and radar diagnostics.
  - *Sky Blue (`#38bdf8`)*: Routes and punctuality.
  - *Transit Amber (`#f59e0b`)*: Peak frequency and operational warnings.
  - *Alert Red (`#ef4444`)*: Bottlenecks and severe overcrowding.
  - *Emerald Green (`#10b981`)*: Digital payment adoption and healthy statuses.
  - *Purple / Indigo (`#a855f7`, `#6366f1`)*: Demographics and secondary corridors.

## 6.2 Typography & Hierarchy
- **Primary Headings**: Google Fonts `Outfit` (700/800 bold weights, geometric modern flair).
- **Body & Numerical Readouts**: Google Fonts `Plus Jakarta Sans` (optimized for readability on high-density data displays).

## 6.3 Responsive Breakpoints
- **Desktop (>= 1200px)**: 4-column KPI grid, 2-column chart grid, 6-column filter bar.
- **Tablet (768px - 1024px)**: 2-column KPI grid, 1-column chart grid, stacked filters.
- **Mobile (< 768px)**: 1-column single stacked layout, horizontal scrolling data tables, full-width touch-friendly buttons.
