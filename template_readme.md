# Course Template Documentation

## 🎓 Quick Start Guide

This template provides a complete framework for creating professional, accessible, and interactive online courses. It includes responsive design, accessibility features, progress tracking, and many other enhancements out of the box.

## 📁 Directory Structure

```
course_template/
├── index.html              # Main course homepage
├── lesson_template.html    # Template for individual lessons
├── course-config.json      # Course configuration and metadata
├── favicon.ico            # Course favicon (replace with your own)
├── styles/
│   └── main.css           # Consolidated CSS (mobile-first, responsive)
├── js/
│   ├── clipboard.js       # Copy code functionality
│   └── course-enhancements.js  # Interactive features
├── images/                # Store course images here
└── assets/               # Additional assets (PDFs, downloads, etc.)
```

## 🚀 Getting Started

### Step 1: Configure Your Course

1. Open `course-config.json`
2. Update all placeholder values marked with `[brackets]`
3. Customize colors, fonts, and features to match your brand
4. Define your course structure (modules and lessons)

### Step 2: Customize the Homepage

1. Open `index.html`
2. Replace all `[bracketed placeholders]` with your content
3. Update the course title, description, and objectives
4. Modify the module structure to match your course
5. Add or remove sections as needed

### Step 3: Create Your Lessons

1. Copy `lesson_template.html` for each lesson
2. Rename to match your naming convention (e.g., `lesson_01.html`)
3. Update content, code examples, and exercises
4. Link lessons correctly in navigation

### Step 4: Add Your Content

1. Place images in the `images/` directory
2. Add downloadable resources to `assets/`
3. Update the favicon.ico with your course logo
4. Write your lesson content using the provided structure

## 🎨 Customization

### CSS Variables

The template uses CSS variables for easy theming. Key variables in `main.css`:

```css
:root {
    --primary-color: rgb(59, 130, 246);
    --primary-hover: rgb(37, 99, 235);
    --secondary-color: rgb(248, 250, 252);
    --text-color: rgb(51, 65, 85);
    --border-color: rgb(226, 232, 240);
    /* ... and more */
}
```

### Dark Mode

Dark mode is automatically supported. The theme toggle button allows users to switch between light and dark modes, with preferences saved locally.

### Mobile Responsiveness

The template is mobile-first and fully responsive. Key breakpoints:
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 💡 Features

### Built-in Features

- ✅ **Responsive Design**: Works on all devices
- ✅ **Accessibility**: WCAG 2.1 AA compliant
- ✅ **Progress Tracking**: Automatic lesson progress saving
- ✅ **Code Highlighting**: Syntax highlighting ready
- ✅ **Copy Code Buttons**: One-click code copying
- ✅ **Search Functionality**: Client-side content search
- ✅ **Keyboard Shortcuts**: Navigation shortcuts (press ? to see them)
- ✅ **Print Friendly**: Optimized print styles
- ✅ **Theme Toggle**: Light/dark mode support
- ✅ **Smooth Scrolling**: Enhanced navigation experience
- ✅ **Interactive Quizzes**: Built-in quiz functionality
- ✅ **Breadcrumb Navigation**: Clear location indication
- ✅ **Mobile Menu**: Hamburger menu for mobile devices
- ✅ **SEO Ready**: Meta tags and structured data support
- ✅ **Sticky Table of Contents**: Always-visible navigation within lessons
- ✅ **Mermaid Diagram Support**: Create flowcharts and diagrams easily

### Interactive Elements

#### Sticky Table of Contents (NEW!)
The template now includes a sticky, collapsible table of contents that stays visible as users scroll:

```html
<details class="card" open style="position: sticky; top: 80px; z-index: 100; background: var(--card-bg, white); box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 2rem;">
    <summary style="cursor: pointer; font-weight: bold; padding: 0.5rem 1rem; user-select: none;">
        <h2 style="display: inline; margin: 0;">📑 In This Lesson</h2>
    </summary>
    <nav aria-label="Table of Contents" style="padding: 0 1rem 1rem 1rem;">
        <ol>
            <li><a href="#section1" class="toc-link">Section Name</a></li>
            <li><a href="#section2" class="toc-link">Section Name</a></li>
        </ol>
    </nav>
</details>
```

**Features:**
- Stays visible while scrolling (sticky positioning)
- Collapsible to save screen space
- Opens by default but users can minimize it
- Accessible with proper ARIA labels
- Mobile-friendly design

#### Mermaid Diagrams
Create flowcharts, diagrams, and visual aids using Mermaid syntax:

```html
<div class="mermaid">
    graph TD
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]
    style A fill:#667eea,stroke:#333,stroke-width:2px,color:#fff
</div>
```

**Required in `<head>`:**
```html
<script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ 
        startOnLoad: true,
        theme: 'default',
        themeVariables: {
            primaryColor: '#f0f0f0',
            primaryTextColor: '#333',
            primaryBorderColor: '#667eea'
        }
    });
</script>
```

#### Card Styles

**Basic Card:**
```html
<div class="card">
    <h4>Title</h4>
    <p>Content</p>
</div>
```

**Success/Tip Card (Green):**
```html
<div class="card" style="background: #e8f5e9; border-left: 4px solid #4CAF50;">
    <h4>✅ Title</h4>
    <p>Content</p>
</div>
```

**Warning Card (Yellow):**
```html
<div class="card" style="background-color: #fff3cd; border-left: 4px solid #ffc107;">
    <h4>⚠️ Title</h4>
    <p>Content</p>
</div>
```

**Feature Card (Purple Gradient):**
```html
<div class="card" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
    <h3>💡 Title</h3>
    <p style="color: white;">Content</p>
</div>
```

**Info Card (Blue):**
```html
<div class="card" style="background: #e3f2fd; border-left: 4px solid #2196F3;">
    <h4>💡 Title</h4>
    <p>Content</p>
</div>
```

#### Code Blocks
```html
<pre><code class="language-python">
# Your code here
print("Hello, World!")
</code></pre>
```

#### Exercise Cards
```html
<div class="card" style="background: #e3f2fd; border-left: 4px solid #2196F3;">
    <h3>🏋️ Exercise Title</h3>
    <p>Exercise instructions...</p>
</div>
```

#### Quiz Questions
```html
<div class="quiz-container">
    <div class="quiz-question">
        <p>Your question here?</p>
        <div class="quiz-options">
            <button class="quiz-option" data-correct="true">Correct answer</button>
            <button class="quiz-option" data-correct="false">Wrong answer</button>
        </div>
    </div>
</div>
```

## 🔧 JavaScript Features

### Progress Tracking
- Automatically saves user progress
- Tracks visited lessons
- Saves scroll position
- Shows completion percentage

### Search Functionality
- Real-time content search
- Highlights matching text
- Navigates to results

### Keyboard Shortcuts
- `/` - Focus search
- `←` / `→` - Previous/Next lesson
- `H` - Go home
- `ESC` - Close search/modals
- `?` - Show shortcuts help

## 📝 Content Guidelines

### Lesson Structure

Each lesson should include:

1. **Learning Objectives**: Clear, measurable goals with estimated time
2. **Sticky Table of Contents**: Easy navigation within the lesson
3. **Introduction**: Context and importance
4. **Core Content**: Main teaching material with visual aids
5. **Examples**: Practical demonstrations with diagrams
6. **Exercises**: Hands-on practice
7. **Summary**: Key takeaways
8. **Resources**: Additional learning materials
9. **Navigation**: Previous/Home/Next links

### Writing Tips

- **Use clear, concise language** appropriate for your audience
- **Break content into digestible sections** (6-10 main sections ideal)
- **Include plenty of examples** with real-world analogies
- **Use visual aids liberally** (Mermaid diagrams, tables, cards)
- **Provide exercises with solutions** using collapsible details
- **Add emoji section markers** for visual interest and scannability
- **Use consistent formatting** across all lessons
- **Write as an instructor** with friendly, encouraging tone
- **Bold key terms** and important points
- **Use blockquotes** for important insights or quotes

### Section ID Conventions

Use clear, descriptive IDs for sections:
- `#introduction` or `#intro`
- `#core-concepts` or `#fundamentals`
- `#examples` or `#demonstrations`
- `#hands-on` or `#project`
- `#best-practices` or `#tips`
- `#summary` or `#wrap-up`

## 🚢 Deployment

### Static Hosting

This template creates static HTML files that can be hosted anywhere:

- **GitHub Pages**: Free hosting for GitHub repositories
- **Netlify**: Easy deployment with drag-and-drop
- **Vercel**: Fast global CDN
- **AWS S3**: Scalable static hosting
- **Any web server**: Apache, Nginx, etc.

### Deployment Steps

1. Complete all content creation
2. Test locally in a web browser
3. Verify all links work correctly
4. Check responsive design on multiple devices
5. Test all interactive features (TOC, quizzes, code copying)
6. Verify Mermaid diagrams render correctly
7. Deploy to your chosen hosting service

## 🛠️ Troubleshooting

### Common Issues

**Issue**: JavaScript features not working
- **Solution**: Ensure JS files are properly linked and no console errors

**Issue**: Styles not applying
- **Solution**: Check that `main.css` is linked correctly

**Issue**: Images not showing
- **Solution**: Verify image paths are correct (relative to HTML file)

**Issue**: Mobile menu not working
- **Solution**: Ensure mobile-menu-toggle ID matches in HTML and JS

**Issue**: Mermaid diagrams not rendering
- **Solution**: Check that Mermaid script is in `<head>` and syntax is correct

**Issue**: Sticky TOC not sticking
- **Solution**: Verify `position: sticky` and `top: 80px` styles are present

**Issue**: TOC links not working
- **Solution**: Ensure section IDs match exactly (case-sensitive)

## 📚 Advanced Customization

### Adding New Features

1. **New JS functionality**: Add to `course-enhancements.js`
2. **Custom styles**: Add to end of `main.css` or create `custom.css`
3. **New components**: Create reusable HTML snippets
4. **Third-party libraries**: Add via CDN or local files

### Sticky TOC Customization

Adjust the sticky position:
```css
top: 80px;  /* Change this value based on your nav height */
```

Change TOC styling:
```css
background: var(--card-bg, white);  /* Background color */
box-shadow: 0 2px 8px rgba(0,0,0,0.1);  /* Shadow effect */
```

### Integration Options

- **Analytics**: Add Google Analytics or similar
- **Comments**: Integrate Disqus or similar
- **Video**: Embed YouTube/Vimeo players
- **Forms**: Add contact or feedback forms
- **Social Sharing**: Add social media buttons

## 🤝 Support

### Getting Help

1. Check this documentation first
2. Review the example files
3. Search for similar course implementations
4. Ask in web development forums

### Contributing

If you improve this template:
1. Document your changes
2. Test thoroughly
3. Share with the community

## 📄 License

This template is provided as-is for educational purposes. Feel free to modify and use for your own courses.

## ✨ Tips for Success

1. **Plan your content structure** before starting
2. **Keep lessons focused** on single topics (45-60 minutes each)
3. **Use the sticky TOC** for longer lessons (makes navigation easier)
4. **Add visual aids** with Mermaid diagrams for complex concepts
5. **Test on multiple devices** before deployment
6. **Get feedback** from early users
7. **Iterate and improve** based on usage data
8. **Keep accessibility in mind** for all users
9. **Maintain consistency** across all lessons
10. **Update regularly** with new content

### Best Practices for Sticky TOC

- **Keep TOC concise**: 6-10 items ideal
- **Use descriptive labels**: Help users know what to expect
- **Update section IDs**: Ensure they match TOC links exactly
- **Test scrolling**: Verify TOC doesn't overlap content
- **Consider mobile**: TOC should work well on small screens

### Best Practices for Mermaid Diagrams

- **Keep diagrams simple**: Don't overcrowd with too many nodes
- **Use consistent styling**: Apply colors and styles that match your theme
- **Add descriptive labels**: Make diagram purpose clear
- **Test rendering**: Some syntax variations may cause issues
- **Provide alt text**: Use figure captions for accessibility

---

## 🎉 Ready to Create Your Course!

You now have everything you need to create a professional online course with:
- ✅ Sticky navigation within lessons
- ✅ Visual diagrams and flowcharts
- ✅ Color-coded information cards
- ✅ Mobile-responsive design
- ✅ Accessibility features
- ✅ Interactive elements

Remember:

- Start with the configuration
- Build your content incrementally
- Use the sticky TOC for better navigation
- Add visual aids with Mermaid diagrams
- Test frequently
- Deploy when ready

Good luck with your course! 🚀
