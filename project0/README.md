# My Fitness & Training Routine

## Project Overview
This project is a personal webpage focused on **fitness and training routines**. The website includes my workout plans, weekly schedule, and recovery strategies. It is designed to be visually appealing, responsive, and easy to navigate on both desktop and mobile devices.

The website consists of **four HTML pages**:
1. **Home (`index.html`)** – Introduction with a full-screen background image and overlay text.  
2. **Workout Plans (`workout.html`)** – Detailed strength and cardio exercises presented using lists and Bootstrap cards.  
3. **Weekly Schedule (`schedule.html`)** – A structured table showing workouts for each day of the week.  
4. **Recovery (`recovery.html`)** – Tips on rest, stretching, and injury prevention.

---

## Files in the Project

| File | Purpose |
|------|---------|
| `index.html` | Home page with background image and overlay text |
| `workout.html` | Workout plans with lists and Bootstrap cards |
| `schedule.html` | Weekly workout schedule table |
| `recovery.html` | Recovery and injury prevention page |
| `styles.scss` | SCSS source file containing all styling, variables, nesting, and inheritance |
| `styles.css` | Compiled CSS from SCSS, linked to all HTML pages |
| `fitness.jpg` | Background image used on the home page |
| `README.md` | This project documentation |

---

## How Requirements Are Met

1. **Four HTML pages with navigation**  
   - All pages are interlinked using a Bootstrap navbar that works on desktop and mobile.

2. **List, Table, and Image**  
   - **List:** `workout.html` uses unordered lists for strength and cardio exercises.  
   - **Table:** `schedule.html` contains a table showing the weekly workout plan.  
   - **Image:** `index.html` uses a full-screen background image.

3. **Stylesheet**  
   - All pages use a single stylesheet (`styles.css`) generated from SCSS (`styles.scss`).

4. **CSS properties and selectors**  
   - **Properties used:** `margin`, `padding`, `font-family`, `color`, `background-color`, `display`, `flex`, `text-align`, `font-size`, etc.  
   - **Selectors used:** element selectors (`body`, `h1`, `ul`), class selectors (`.overlay`, `.page-index`, `.card`), ID selectors (`#strength-head`, `#cardio-head`, `#yoga-head` ), nested selectors (`.page-index .overlay h1`), pseudo-class (`a:hover`).

5. **Mobile responsiveness**  
   - Media queries adjust the layout for screens smaller than 768px, including centering text and adjusting font sizes on workout cards.

6. **Bootstrap 4**  
   - Bootstrap 4 is used for the navbar, cards, and grid system.  
   - The workout page uses **two columns** in a row to display strength, cardio and mobility exercises side by side on larger screens.

7. **SCSS features**  
   - **Variables:** `$overlay-color`, `$white`, `$gold`, `$heading-font`, `$text-font`  
   - **Nesting:** Example `.page-index { .overlay { h1 { ... } } }`  
   - **Inheritance:** `.special-text` extends `.base-text`  

---

## How to View the Website
1. Open any of the HTML files (`index.html`, `workout.html`, `schedule.html`, `recovery.html`) in a modern web browser.  
2. Ensure `styles.css` and `fitness.jpg` are in the same directory as the HTML files.  
3. Resize the browser window or open on a mobile device to see the responsive design in action.

---

## Notes
- All pages are fully functional and meet the assignment requirements.  
- Bootstrap 4 scripts are included on all pages to ensure the navbar collapse works on mobile devices.  
- The SCSS file can be edited to adjust styling; changes must be compiled to `styles.css` to reflect on the website.  

