---
name: frontend-skill
description: Build responsive pages, reusable components, layouts, and styling for modern web applications.
---

# Frontend Development Skill

## Instructions

1. **Page Structure**
   - Semantic HTML structure
   - Clear separation of sections
   - Accessible markup (ARIA where needed)

2. **Components**
   - Reusable and composable components
   - Props-driven configuration
   - Minimal side effects
   - Clear responsibility per component

3. **Layout**
   - Responsive layouts using Flexbox/Grid
   - Mobile-first approach
   - Consistent spacing and alignment
   - Scalable layout patterns

4. **Styling**
   - Clean, maintainable CSS (or Tailwind/utility classes)
   - Consistent color, typography, and spacing
   - Dark/light theme readiness
   - Avoid inline styles unless necessary

5. **Interactions**
   - Basic UI states (hover, focus, active, disabled)
   - Smooth transitions and animations
   - Keyboard and screen-reader support

## Best Practices
- Prefer reusable components over page-specific code
- Keep components small and focused
- Follow design consistency across pages
- Optimize for performance and accessibility
- Ensure responsiveness on all screen sizes

## Example Structure
```html
<main class="page-container">
  <header class="page-header">
    <h1 class="page-title">Page Title</h1>
  </header>

  <section class="content-grid">
    <article class="card">
      <h2 class="card-title">Component Title</h2>
      <p class="card-text">Component content goes here.</p>
      <button class="primary-button">Action</button>
    </article>
  </section>
</main>
