# Farm Animation Components

Reusable animation components for both marketing pages and farm game.

## Components

### Basic Elements

- **Crop.tsx** - Growing crop animation with stages (corn, wheat, carrot)
- **Tractor.tsx** - Animated tractor moving across the screen
- **FlyingBug.tsx** - Flying insects (bee, butterfly, bird) with bounce physics

### Scenes

- **Cornfield.tsx** - Full cornfield scene with multiple crops and optional tractor
- **GrowingCropScene.tsx** - Card-sized scene showing growing crops with flying bugs
- **IsometricTownScene.tsx** - Isometric farm buildings (house, barn, silo)
- **SustainableFarmScene.tsx** - Solar panel, wind turbine, and animals

## Usage

```tsx
import { Cornfield, GrowingCropScene } from '@/components/animations';

// Full background
<Cornfield rows={5} cols={12} withTractor={true} />

// Card scene
<GrowingCropScene />
```

## Design Philosophy

These components are designed to be:

1. **Reusable** - Work in both marketing pages and farm game
2. **Performant** - Simple animations using CSS transitions and setInterval
3. **Themeable** - Support light and dark modes
4. **Composable** - Can be combined to create complex scenes

## Future Improvements

- Add more crop types (tomato, pumpkin, lettuce)
- Create weather effects (rain, sun, clouds)
- Add animal animations (chicken, cow, sheep)
- Implement seasonal themes
- Add sound effects (optional)
