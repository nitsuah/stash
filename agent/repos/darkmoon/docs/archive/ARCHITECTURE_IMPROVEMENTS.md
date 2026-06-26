# Architecture Improvements - Quick Reference

**Purpose:** Actionable improvements for code organization and architecture  
**Related:** [L7_ENGINEERING_REVIEW.md](./L7_ENGINEERING_REVIEW.md), [TECH_DEBT.md](./TECH_DEBT.md)

---

## File Organization Recommendations

### Current Structure (Issues)

```bash
src/
├── components/         # Mixed concerns (200+ line files)
│   ├── GameManager.ts  # ✅ Good
│   ├── SoundManager.ts # ❌ 621 lines
│   ├── ChatBox.tsx     # ❌ Has inline profanity logic
│   └── characters/     # ✅ Good separation
├── pages/
│   ├── Solo.tsx        # ❌ 1002 lines (biggest issue)
│   ├── Lobby.tsx       # ⚠️ Possibly deprecated
│   └── Home.tsx        # ⚠️ Commented imports
└── lib/
    └── constants/      # ⚠️ Only profanity, needs expansion
```

### Recommended Structure

```bash
src/
├── components/
│   ├── game/           # NEW: Game-specific components
│   │   ├── GameUI.tsx
│   │   ├── GameHUD.tsx
│   │   └── PauseMenu.tsx
│   ├── ui/             # NEW: Reusable UI components
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── Modal/
│   │   └── Input/
│   ├── characters/     # KEEP: Already well-organized
│   └── mobile/         # NEW: Mobile controls
│       ├── MobileJoystick/
│       └── MobileButton/
├── pages/
│   ├── Solo/           # REFACTOR: Break into folder
│   │   ├── index.tsx
│   │   ├── hooks/
│   │   ├── components/
│   │   └── config/
│   ├── Home/           # OPTIONAL: Organize if grows
│   └── App.tsx
├── lib/
│   ├── audio/          # NEW: Extract from SoundManager
│   │   ├── SoundManager.ts
│   │   ├── ProceduralMusic.ts
│   │   ├── SoundEffects.ts
│   │   └── AudioContext.ts
│   ├── utils/          # NEW: Shared utilities
│   │   ├── logger.ts
│   │   ├── validation.ts
│   │   └── profanity.ts
│   ├── hooks/          # NEW: Shared hooks
│   │   ├── useSocket.ts
│   │   ├── useGameState.ts
│   │   └── useOrientation.ts
│   └── constants/
│       ├── game.ts
│       ├── physics.ts
│       └── ui.ts
└── types/              # KEEP: Good
```

---

## Hook Extraction Patterns

### Pattern: Complex useFrame Logic

**Before (PlayerCharacter.tsx - 300 lines in useFrame):**

```typescript
useFrame((state, delta) => {
  // Movement logic (50 lines)
  // Camera logic (50 lines)
  // Collision logic (100 lines)
  // Tag detection (50 lines)
  // Jetpack physics (50 lines)
});
```

**After (Modular hooks):**

```typescript
// hooks/usePlayerMovement.ts
export const usePlayerMovement = (
  meshRef: RefObject<Group>,
  keysPressedRef: RefObject<KeyMap>,
  isPaused: boolean
) => {
  const velocity = useRef(new Vector3());

  useFrame((state, delta) => {
    if (isPaused) return;

    // Only movement logic here (50 lines)
  });

  return { velocity };
};

// hooks/usePlayerCamera.ts
export const usePlayerCamera = (
  meshRef: RefObject<Group>,
  mouseControls: MouseControls
) => {
  useFrame((state, delta) => {
    // Only camera logic here (50 lines)
  });
};

// PlayerCharacter.tsx (now clean)
export const PlayerCharacter = (props) => {
  const meshRef = useRef<Group>(null);

  usePlayerMovement(meshRef, keysPressedRef, isPaused);
  usePlayerCamera(meshRef, mouseControls);
  usePlayerCollision(meshRef, collisionSystem);
  usePlayerTagging(meshRef, gameManager, playerIsIt);
  useJetpack(meshRef, keysPressedRef);

  return <SpacemanModel ref={meshRef} />;
};
```

---

### Pattern: Complex State Management

**Before (Solo.tsx - 20+ useState):**

```typescript
const [clients, setClients] = useState({});
const [socketClient, setSocketClient] = useState(null);
const [gameState, setGameState] = useState("idle");
const [playerIsIt, setPlayerIsIt] = useState(false);
const [bot1IsIt, setBot1IsIt] = useState(false);
const [bot2IsIt, setBot2IsIt] = useState(false);
// ... 15 more useState calls
```

**After (Custom hook):**

```typescript
// hooks/useSoloGame.ts
export const useSoloGame = () => {
  const [state, dispatch] = useReducer(gameReducer, initialState);

  const startGame = useCallback(() => {
    dispatch({ type: "START_GAME" });
  }, []);

  const tagPlayer = useCallback((tagger, tagged) => {
    dispatch({ type: "TAG_PLAYER", payload: { tagger, tagged } });
  }, []);

  return {
    gameState: state,
    actions: { startGame, tagPlayer },
  };
};

// Solo/index.tsx (now clean)
export default function Solo() {
  const { gameState, actions } = useSoloGame();
  const socket = useSocketConnection();
  const bots = useGameBots(gameState);

  return (
    <SoloScene gameState={gameState} bots={bots} onTag={actions.tagPlayer} />
  );
}
```

---

## Shared Utility Patterns

### Logger Utility

**Implementation:**

```typescript
// lib/utils/logger.ts
type LogLevel = "debug" | "info" | "warn" | "error";

interface Logger {
  debug: (...args: unknown[]) => void;
  info: (...args: unknown[]) => void;
  warn: (...args: unknown[]) => void;
  error: (...args: unknown[]) => void;
}

export const createLogger = (namespace: string): Logger => {
  const isDev = import.meta.env?.DEV || process.env?.NODE_ENV !== "production";

  const log = (level: LogLevel, ...args: unknown[]) => {
    const timestamp = new Date().toISOString().split("T")[1].slice(0, -1);
    const prefix = `[${namespace} ${timestamp}]`;

    switch (level) {
      case "debug":
        isDev && console.log(prefix, ...args);
        break;
      case "info":
        console.log(prefix, ...args);
        break;
      case "warn":
        console.warn(prefix, ...args);
        break;
      case "error":
        console.error(prefix, ...args);
        break;
    }
  };

  return {
    debug: (...args) => log("debug", ...args),
    info: (...args) => log("info", ...args),
    warn: (...args) => log("warn", ...args),
    error: (...args) => log("error", ...args),
  };
};

// Usage in components
const log = createLogger("GameManager");
log.debug("Game started", gameState);
log.error("Failed to tag player", error);
```

---

### Socket Connection Hook

**Implementation:**

```typescript
// lib/hooks/useSocket.ts
export const useSocketConnection = (options?: SocketOptions) => {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const serverUrl =
      import.meta.env.VITE_SOCKET_SERVER_URL || window.location.origin;

    const newSocket = io(serverUrl, {
      transports: ["websocket"],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
      ...options,
    });

    newSocket.on("connect", () => {
      setIsConnected(true);
      setError(null);
    });

    newSocket.on("disconnect", () => {
      setIsConnected(false);
    });

    newSocket.on("connect_error", (err) => {
      setError(err);
    });

    setSocket(newSocket);

    return () => {
      newSocket.disconnect();
    };
  }, []);

  return { socket, isConnected, error };
};

// Usage
const { socket, isConnected, error } = useSocketConnection();

if (!isConnected) return <ConnectingScreen />;
if (error) return <ErrorScreen error={error} />;
```

---

## Component Composition Patterns

### Before: Monolithic Component

```typescript
// Solo.tsx (1000 lines)
export default function Solo() {
  // 20+ useState
  // 10+ useEffect
  // 500+ lines of JSX

  return (
    <div>
      {/* Tutorial */}
      {/* Help Modal */}
      {/* Game UI */}
      {/* Canvas with 10+ children */}
      {/* Chat */}
      {/* Mobile Controls */}
      {/* Utility Menu */}
    </div>
  );
}
```

### After: Composed Components

```typescript
// Solo/index.tsx (150 lines)
export default function Solo() {
  const game = useSoloGame();
  const socket = useSocketConnection();

  return (
    <GameLayout>
      <TutorialOverlay show={game.showTutorial} />
      <HelpModal isOpen={game.showHelp} />

      <SoloScene
        gameState={game.state}
        socket={socket}
        onTag={game.actions.tagPlayer}
      />

      <SoloHUD gameState={game.state} onPause={game.actions.pause} />

      <ChatBox socket={socket} messages={game.messages} />

      <MobileControls onMove={game.actions.move} onJump={game.actions.jump} />

      <UtilityMenu />
    </GameLayout>
  );
}

// Solo/components/SoloScene.tsx (200 lines)
export const SoloScene = ({ gameState, socket, onTag }) => {
  return (
    <Canvas>
      <Lighting />
      <Environment />
      <PlayerCharacter {...playerProps} />
      <BotCharacter {...bot1Props} />
      <BotCharacter {...bot2Props} />
      <Arena />
    </Canvas>
  );
};

// Solo/components/SoloHUD.tsx (150 lines)
export const SoloHUD = ({ gameState, onPause }) => {
  return (
    <div className={styles.hud}>
      <GameTimer time={gameState.timeRemaining} />
      <ScoreDisplay scores={gameState.scores} />
      <TagIndicator isIt={gameState.playerIsIt} />
      <PauseButton onClick={onPause} />
    </div>
  );
};
```

---

## Testing Patterns

### Component Testing with Hooks

**Test extracted hooks independently:**

```typescript
// __tests__/hooks/usePlayerMovement.test.ts
import { renderHook } from "@testing-library/react";
import { usePlayerMovement } from "../../lib/hooks/usePlayerMovement";

describe("usePlayerMovement", () => {
  it("should move forward when W is pressed", () => {
    const meshRef = { current: createMockMesh() };
    const keysPressed = { current: { [W]: true } };

    const { result } = renderHook(() =>
      usePlayerMovement(meshRef, keysPressed, false)
    );

    // Simulate frame update
    act(() => {
      // Trigger useFrame manually in test
    });

    expect(meshRef.current.position.z).toBeCloseTo(0.1);
  });
});
```

**Integration testing for composed components:**

```typescript
// __tests__/pages/Solo.integration.test.tsx
describe("Solo page integration", () => {
  it("should handle complete tag gameplay", async () => {
    const { getByTestId } = render(<Solo />);

    // Wait for game to load
    await waitFor(() => {
      expect(getByTestId("game-canvas")).toBeInTheDocument();
    });

    // Simulate player movement
    fireEvent.keyDown(window, { key: "w" });

    // Verify position update
    await waitFor(() => {
      expect(getByTestId("player-position")).toHaveTextContent("0, 0, 0.1");
    });

    // Simulate tag
    fireEvent.click(getByTestId("tag-button"));

    // Verify tag state
    await waitFor(() => {
      expect(getByTestId("is-it-indicator")).toHaveTextContent("Bot1 is IT!");
    });
  });
});
```

---

## CSS Module Pattern

### **Before: Global CSS**

```css
/* App.css */
.container {
  display: flex;
}

.button {
  padding: 10px;
}
```

### **After: CSS Modules**

```css
/* Button.module.css */
.button {
  padding: 10px;
  border-radius: 4px;
}

.button.primary {
  background: var(--primary-color);
}

.button.secondary {
  background: var(--secondary-color);
}
```

```typescript
// Button.tsx
import styles from "./Button.module.css";

export const Button = ({ variant = "primary", children, ...props }) => {
  return (
    <button className={`${styles.button} ${styles[variant]}`} {...props}>
      {children}
    </button>
  );
};
```

---

## Design Tokens System

**Create centralized design tokens:**

```typescript
// lib/design-tokens.ts
export const colors = {
  primary: {
    main: "#6366f1",
    light: "#818cf8",
    dark: "#4f46e5",
  },
  secondary: {
    main: "#ec4899",
    light: "#f472b6",
    dark: "#db2777",
  },
  neutral: {
    50: "#f9fafb",
    100: "#f3f4f6",
    // ... more shades
    900: "#111827",
  },
} as const;

export const spacing = {
  xs: "4px",
  sm: "8px",
  md: "16px",
  lg: "24px",
  xl: "32px",
} as const;

export const breakpoints = {
  mobile: "640px",
  tablet: "768px",
  desktop: "1024px",
  wide: "1280px",
} as const;

export const typography = {
  fontSize: {
    xs: "12px",
    sm: "14px",
    base: "16px",
    lg: "18px",
    xl: "20px",
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
} as const;
```

**Usage in CSS:**

```css
/* Generate CSS variables from tokens */
:root {
  --color-primary-main: #6366f1;
  --spacing-md: 16px;
  /* ... etc */
}

.button {
  padding: var(--spacing-md);
  background: var(--color-primary-main);
}
```

---

## Server Architecture Pattern

**Current monolithic server.js → Modular structure:**

```bash
server/
├── index.js              # Entry point
├── app.js                # Express app setup
├── socket.js             # Socket.io configuration
├── middleware/
│   ├── cors.js
│   ├── rateLimit.js
│   └── validation.js
├── routes/
│   ├── health.js
│   └── api.js
├── sockets/
│   ├── connection.js     # Connection handling
│   ├── movement.js       # Move events
│   ├── chat.js           # Chat events
│   └── game.js           # Game events
├── utils/
│   ├── profanity.js
│   └── logger.js
└── validation/
    ├── schemas.js        # Zod schemas
    └── validators.js
```

**Example refactored server:**

```javascript
// server/sockets/movement.js
import { validatePosition } from "../validation/validators.js";

export const setupMovementHandlers = (io) => {
  io.on("connection", (client) => {
    client.on("move", ({ rotation, position }) => {
      // Validate input
      if (!validatePosition(position)) {
        client.emit("error", { message: "Invalid position" });
        return;
      }

      // Update state
      clients[client.id] = { position, rotation };

      // Broadcast
      io.emit("move", clients);
    });
  });
};
```

---

## Next Steps

1. **Start with highest impact:**

   - Fix mobile controls (P0)
   - Decompose Solo.tsx (P0)
   - Create logger utility (P1)

2. **Establish patterns early:**

   - Document chosen patterns in this file
   - Create templates for new components/hooks
   - Enforce via code review

3. **Incremental refactoring:**
   - Don't refactor everything at once
   - Refactor when adding features
   - Always maintain test coverage

---

**Related Documents:**

- [L7_ENGINEERING_REVIEW.md](./L7_ENGINEERING_REVIEW.md) - Full analysis
- [TECH_DEBT.md](./TECH_DEBT.md) - Prioritized items
- [ROADMAP.md](./ROADMAP.md) - Implementation timeline

## Related
- [[repos/darkmoon/docs/archive/L7_ENGINEERING_REVIEW|L7 Engineering Review]] — full analysis this document is derived from
- [[repos/darkmoon/docs/ARCHITECTURE|Architecture]] — current active architecture document
- [[repos/darkmoon|darkmoon runbook]] — repo context
