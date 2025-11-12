# Tilly AI - Avatar Integration Guide

## Overview

Tilly AI includes a customizable avatar system that displays an AI companion character in the web interface. The avatar appears in chat messages and on the welcome screen, providing a friendly, personalized experience.

## Current Implementation

### Default Avatar

The default avatar is an SVG image featuring:
- Purple and blue gradient background (Tilly's brand colors)
- Friendly smiling face
- Heart decoration symbolizing empathy and care
- Location: `static/images/avatar.svg`

### Avatar Display Locations

1. **Welcome Screen**: Large avatar (120x120px) on the main greeting page
2. **Chat Messages**: Smaller avatar (40x40px) next to each Tilly response
3. **Typing Indicator**: Avatar shown while Tilly is generating a response

## Customizing the Avatar

### Option 1: Replace the SVG File

Replace `static/images/avatar.svg` with your own SVG or image file:

```bash
# Using SVG (recommended for scalability)
cp your-avatar.svg static/images/avatar.svg

# Using PNG or JPG
cp your-avatar.png static/images/avatar.png
# Then update references in templates/index.html and static/js/app.js
```

### Option 2: Create Your Own SVG Avatar

Edit `static/images/avatar.svg` to customize the appearance:

```svg
<svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
  <!-- Customize colors, shapes, and features here -->
  <circle cx="100" cy="100" r="100" fill="url(#grad1)"/>
  <!-- Add your custom design elements -->
</svg>
```

### Option 3: Use an Animated Avatar

For a more dynamic experience, you can use:

- **Animated GIF**: Simple animated avatar
- **CSS Animations**: Add CSS animations to the avatar container
- **Lottie Animations**: Use Lottie for complex vector animations

Example CSS animation:

```css
.message-avatar img {
    animation: gentle-pulse 3s ease-in-out infinite;
}

@keyframes gentle-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}
```

## Open Source AI Girlfriend Avatars

### Recommended Resources

Here are popular open-source avatar projects you can integrate:

1. **VRoid Studio Models**
   - License: Various (check individual models)
   - Website: https://vroid.com/
   - Export as PNG/SVG for 2D use
   - Free to use with attribution

2. **Open Peeps**
   - License: CC0 (Public Domain)
   - Website: https://www.openpeeps.com/
   - Hand-drawn illustration library
   - Fully customizable

3. **Avataaars**
   - License: Free for commercial use
   - GitHub: https://github.com/fangpenlin/avataaars
   - Sketch library for avatars
   - Mix and match features

4. **DiceBear Avatars**
   - License: MIT
   - Website: https://www.dicebear.com/
   - API-based avatar generation
   - Multiple styles available

5. **Notion-style Avatars**
   - License: MIT
   - Various libraries available
   - Simple, clean design
   - Easy to customize

### Integration Example: DiceBear

```javascript
// In static/js/app.js, modify the avatar creation:
const avatarUrl = `https://api.dicebear.com/7.x/avataaars/svg?seed=tilly&backgroundColor=9b59b6`;

const avatarImg = document.createElement('img');
avatarImg.src = avatarUrl;
avatarImg.alt = 'Tilly';
```

### Integration Example: Local Custom Avatar

```html
<!-- Download from open source project -->
<!-- Place in static/images/avatar-character.png -->

<!-- In templates/index.html -->
<img src="/static/images/avatar-character.png" alt="Tilly Avatar">
```

## Avatar Animations

### CSS-Based Animations

Add these to `static/css/style.css`:

```css
/* Floating animation */
.avatar-large img {
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

/* Speaking indicator (when responding) */
.message.tilly .message-avatar img {
    animation: speaking 0.5s ease-in-out infinite;
}

@keyframes speaking {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}
```

### JavaScript-Based Animations

```javascript
// Add to static/js/app.js

// Make avatar "react" to user emotions
function animateAvatarForMood(mood) {
    const avatar = document.querySelector('.avatar-large img');
    
    switch(mood) {
        case 'positive':
            avatar.style.filter = 'brightness(1.2)';
            break;
        case 'vulnerable':
            avatar.style.filter = 'saturate(0.8)';
            break;
        // Add more cases
    }
}
```

## Advanced: 3D Avatar Integration

For a more immersive experience, consider:

### Three.js Integration

```html
<!-- Add to templates/index.html -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

<div id="avatar-3d-container"></div>
```

```javascript
// Initialize 3D avatar
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ alpha: true });

// Load 3D model (VRM, GLB, etc.)
const loader = new THREE.GLTFLoader();
loader.load('/static/models/avatar.glb', (gltf) => {
    scene.add(gltf.scene);
});
```

### Ready Player Me Integration

```javascript
// Use Ready Player Me for customizable 3D avatars
const avatarUrl = 'https://models.readyplayer.me/YOUR_AVATAR_ID.glb';

// Load and display in the interface
```

## Avatar Personality Matching

Match avatar expressions to Tilly's responses:

```javascript
// In static/js/app.js
function getAvatarForIntent(intent, mood) {
    const avatars = {
        'crisis': '/static/images/avatar-caring.svg',
        'wellness': '/static/images/avatar-supportive.svg',
        'chat': '/static/images/avatar-happy.svg',
    };
    
    return avatars[intent] || '/static/images/avatar.svg';
}
```

## Accessibility Considerations

### Alt Text

Always provide descriptive alt text:

```html
<img src="/static/images/avatar.svg" 
     alt="Tilly, a friendly AI companion with a warm smile">
```

### Reduced Motion

Respect user preferences:

```css
@media (prefers-reduced-motion: reduce) {
    .avatar-large img {
        animation: none;
    }
}
```

### Screen Reader Support

```html
<div class="message-avatar" role="img" aria-label="Tilly's avatar">
    <img src="/static/images/avatar.svg" alt="">
</div>
```

## License Compliance

When using open-source avatars:

1. **Check the license** - Ensure commercial use is allowed
2. **Provide attribution** - Credit the creator if required
3. **Follow terms** - Respect any usage restrictions
4. **Document sources** - Keep track of where assets came from

Example attribution in footer:

```html
<footer>
    <p>Avatar created by [Artist Name] - Licensed under [License]</p>
</footer>
```

## Resources

- **Character Design Tools**: Blender, VRoid Studio, Character Creator
- **2D Art**: Procreate, Krita, GIMP
- **Animation**: After Effects, Spine, DragonBones
- **3D Models**: Sketchfab, TurboSquid, CGTrader

## Community Avatars

We're building a collection of community-created Tilly avatars:

- Submit yours to the repository
- Check the `static/images/community-avatars/` directory
- Share on our Discord/Forum

## Future Enhancements

Planned features:

- [ ] Multiple avatar options selectable by users
- [ ] Mood-based avatar expressions
- [ ] Voice-synced lip animations
- [ ] Custom avatar upload for users
- [ ] AR/VR avatar integration
- [ ] Animated emotions (happy, sad, thinking, etc.)

---

For questions or contributions, see [CONTRIBUTING.md](../CONTRIBUTING.md)
