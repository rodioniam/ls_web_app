# Love Score 💕

Video demonstration [here](LoveScore_demo.gif) or try it your-self [here](https://web-production-55a72.up.railway.app)!

## About

This project was born from a small daily habit I share with my girlfriend —
throughout the day we like to ask each other "how much do you love me today?".
Since we also have a cat, we started giving everyone a score: *"You get 4 points,
but the cat gets 6 - you were a little mean today, and he was very sweet"*.

This playful scoring ritual inspired me to build a web app around it.

## What it does

Allocator lets you distribute 10 points between two custom-named cards — they can
represent anyone or anything. Once you've split the points, you can apply bonus
and penalty modifiers to each card (e.g. *+0.5 for being kind today*, 
*−0.8 for scratching the couch*) and see the final score at the end of the day.

## Tech Stack

- **Python / Django** - backend framework
- **HTMX** - dynamic interactions without writing JavaScript
- **CSS** - style and animations
- **SQLite** - database
- **Whitenoise** - static files serving in production

## Features

- Custom card names set before each session
- Real-time point distribution with live counter
- Bonus/penalty modifier system with additive effects
- Session reset functionality
- Pixel art inspired UI

## Author

Built by [Rodion](https://github.com/rodioniam) as a portfolio project while learning Django.