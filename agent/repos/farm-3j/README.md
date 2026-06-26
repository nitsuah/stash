# Farm 3J - Interactive Farm Website

_Automatically synced with your [v0.dev](https://v0.dev) deployments_

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/austin-hardys-projects/v0-farm-contact-website)
[![Built with v0](https://img.shields.io/badge/Built%20with-v0.dev-black?style=for-the-badge)](https://v0.dev/chat/projects/9OcXcTTsfCh)

## Overview

Farm 3J is an interactive farm website featuring:

- **Animated Homepage**: Dynamic farm scene with weather effects, day/night cycle, animated crops, trees, mountains, and wildlife
- **Farm Tycoon Game**: Isometric farm simulation with resource management, animal care, and building placement
- **Responsive Design**: Optimized for mobile and desktop with adaptive layouts
- **Dark Mode**: Theme toggle integrated into the animated sun

## Features

### Homepage Animations

- Rain cycles with storm clouds and lightning
- Growing crops with tractor harvesting
- Moving clouds and flying birds
- Dense forest with trees and bushes
- Mountain ranges with depth
- Interactive sun theme toggle

### Farm Tycoon Game (`/farm`)

- Grid-based isometric rendering
- Animal management (cows, chickens, pigs, sheep)
- Resource production and economy
- Building placement (fences, troughs)
- Day/night cycle
- Tutorial system and keyboard shortcuts

See `docs/FARM-TYCOON-PHASE1-SUMMARY.md` for complete game documentation.

## Tech Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS v4
- **State Management**: React Context + useReducer
- **Animation**: CSS + requestAnimationFrame

This repository will stay in sync with your deployed chats on [v0.dev](https://v0.dev).
Any changes you make to your deployed app will be automatically pushed to this repository from [v0.dev](https://v0.dev).

## Deployment

Your project is live at:

**[https://vercel.com/austin-hardys-projects/v0-farm-contact-website](https://vercel.com/austin-hardys-projects/v0-farm-contact-website)**

## Build your app

Continue building your app on:

**[https://v0.dev/chat/projects/9OcXcTTsfCh](https://v0.dev/chat/projects/9OcXcTTsfCh)**

## Contact Form Delivery

The About page contact modal now submits to `POST /api/contact` with server-side validation.

- `FARM_CONTACT_WEBHOOK_URL` (optional): when set, submissions are forwarded to this webhook.
- If the webhook is not configured, submissions are still accepted and logged server-side (`delivery: local-log`) so the UI keeps a validated success/error flow in non-production setups.

## How It Works

1. Create and modify your project using [v0.dev](https://v0.dev)
2. Deploy your chats from the v0 interface
3. Changes are automatically pushed to this repository
4. Vercel deploys the latest version from this repository

## Community Standards

Shared community policies are centralized in https://github.com/nitsuah/.github:

- Contributing: https://github.com/nitsuah/.github/blob/main/CONTRIBUTING.md
- Code of Conduct: https://github.com/nitsuah/.github/blob/main/CODE_OF_CONDUCT.md
- Security: https://github.com/nitsuah/.github/blob/main/SECURITY.md

## Repository Index

### Root Files
- [[repos/farm-3j/CHANGELOG.md|CHANGELOG.md]]
- [[repos/farm-3j/FEATURES.md|FEATURES.md]]
- [[repos/farm-3j/METRICS.md|METRICS.md]]
- [[repos/farm-3j/ROADMAP.md|ROADMAP.md]]
- [[repos/farm-3j/TASKS.md|TASKS.md]]

### Documentation
- [[repos/farm-3j/docs/FARM-RTS-NORTH-STAR.md|FARM-RTS-NORTH-STAR.md]]
- [[repos/farm-3j/docs/FARM-RTS-TODO.md|FARM-RTS-TODO.md]]
- [[repos/farm-3j/docs/Farm_RTS_Game_Manual.md|Farm_RTS_Game_Manual.md]]
- [[repos/farm-3j/docs/INSTRUCTIONS.md|INSTRUCTIONS.md]]