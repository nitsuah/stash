# 🐿️ Conker's Bad Fur Day — Open Source Three.js Recreation Guide

> **For Agent Use**: This document is a complete implementation specification for recreating the gameplay systems, maps, modes, and mechanics of *Conker's Bad Fur Day* (Rare, 2001) using Three.js as the rendering foundation. Assume a base framework is already in place (scene graph, input handler, asset loader, basic physics stub, and render loop). Your job is to **extend** that framework with the systems described below.

---

## Table of Contents

1. [Project Philosophy & Scope](#1-project-philosophy--scope)
2. [Architecture Overview](#2-architecture-overview)
3. [World & Map System](#3-world--map-system)
4. [Character System](#4-character-system)
5. [Combat & Weapons](#5-combat--weapons)
6. [Context-Sensitive Actions (The B-Button System)](#6-context-sensitive-actions-the-b-button-system)
7. [NPC & Enemy AI](#7-npc--enemy-ai)
8. [Chapters / Story Progression](#8-chapters--story-progression)
9. [Multiplayer Modes](#9-multiplayer-modes)
10. [Camera System](#10-camera-system)
11. [Audio Architecture](#11-audio-architecture)
12. [Graphics Upgrade Targets](#12-graphics-upgrade-targets)
13. [UI & HUD](#13-ui--hud)
14. [Cutscene & Dialogue System](#14-cutscene--dialogue-system)
15. [Save System](#15-save-system)
16. [Asset Pipeline](#16-asset-pipeline)
17. [Implementation Priority Order](#17-implementation-priority-order)

---

## 1. Project Philosophy & Scope

### What We're Building
An open-source, browser-playable homage to Conker's Bad Fur Day that:
- Runs entirely in Three.js (WebGL)
- Recreates the core gameplay loop, chapter structure, and multiplayer modes
- Upgrades visuals to modern standards (PBR materials, dynamic lighting, shadow maps)
- Preserves the tone: adult humor, cinematic presentation, genre-parody gameplay

### What We Are NOT Doing
- Copying original game assets (models, audio, textures are contraband — everything must be original or CC-licensed)
- Emulating the N64 binary
- Claiming affiliation with Rare or Microsoft

### Core Gameplay Pillars (from the original)
| Pillar | Description |
|---|---|
| Context-Sensitive | One button does wildly different things depending on where Conker stands |
| Platforming | Precision 3D jumping, swimming, rolling |
| Combat | Third-person melee + ranged combat |
| Cinematic chapters | Each chapter feels like a movie genre parody |
| Multiplayer | 4-player split-screen with multiple distinct modes |
| Toilet humor & fourth-wall breaking | NPC dialogue, cutscene awareness |

---

## 2. Architecture Overview

### Folder Structure to Extend Your Framework

```
/src
  /core             ← your existing framework lives here
  /game
    /world          ← map chunks, portals, triggers
    /characters     ← Conker + NPCs
    /combat         ← weapons, projectiles, hit detection
    /ai             ← enemy state machines
    /chapters       ← chapter managers + scripted events
    /multiplayer    ← mode managers (war, heist, etc.)
    /camera         ← camera rigs and state machine
    /ui             ← HUD, menus, dialogue boxes
    /cutscenes      ← director system
    /audio          ← spatial audio, music layers
    /save           ← save slots, chapter flags
  /assets
    /models         ← .glb files
    /textures       ← .webp or .ktx2 compressed
    /audio          ← .ogg or .mp3
    /shaders        ← custom GLSL
```

### Key Engine Modules to Register

```js
// main.js — extend your existing game loop
import { WorldManager }       from './game/world/WorldManager.js';
import { CharacterController } from './game/characters/CharacterController.js';
import { CameraRig }          from './game/camera/CameraRig.js';
import { ChapterDirector }    from './game/chapters/ChapterDirector.js';
import { MultiplayerManager } from './game/multiplayer/MultiplayerManager.js';
import { HUD }                from './game/ui/HUD.js';
import { AudioManager }       from './game/audio/AudioManager.js';
import { SaveManager }        from './game/save/SaveManager.js';

// Register all systems with your existing GameLoop / ServiceLocator
GameLoop.register([
  WorldManager,
  CharacterController,
  CameraRig,
  ChapterDirector,
  MultiplayerManager,
  HUD,
  AudioManager,
  SaveManager
]);
```

---

## 3. World & Map System

### 3.1 Overworld Hub — "Windy"

Windy is the central hub that connects all chapters. It must be implemented as a persistent scene with portals.

**Implementation:**

```js
// world/WorldManager.js
export class WorldManager {
  constructor(scene, loader) {
    this.scene = scene;
    this.loader = loader;
    this.chunks = new Map();       // chunkId → THREE.Group
    this.portals = [];             // Portal[] — transition volumes
    this.activeChunk = null;
  }

  async loadChunk(chunkId) {
    if (this.chunks.has(chunkId)) return;
    const gltf = await this.loader.loadAsync(`/assets/models/chunks/${chunkId}.glb`);
    const group = gltf.scene;
    // Tag collision meshes
    group.traverse(obj => {
      if (obj.name.startsWith('COL_')) {
        obj.visible = false;
        obj.userData.isCollider = true;
      }
      if (obj.name.startsWith('PORTAL_')) {
        this.registerPortal(obj);
      }
      if (obj.name.startsWith('TRIGGER_')) {
        this.registerTrigger(obj);
      }
    });
    this.scene.add(group);
    this.chunks.set(chunkId, group);
  }

  registerPortal(mesh) {
    this.portals.push({
      mesh,
      targetChunk: mesh.userData.targetChunk,
      targetSpawn: mesh.userData.targetSpawn,
      bounds: new THREE.Box3().setFromObject(mesh)
    });
  }

  checkPortals(playerPosition) {
    for (const portal of this.portals) {
      if (portal.bounds.containsPoint(playerPosition)) {
        this.transition(portal.targetChunk, portal.targetSpawn);
        return;
      }
    }
  }

  async transition(chunkId, spawnId) {
    // Fade out → unload current → load next → fade in
    await ScreenFade.fadeOut();
    this.unloadChunk(this.activeChunk);
    await this.loadChunk(chunkId);
    this.activeChunk = chunkId;
    await ScreenFade.fadeIn();
  }
}
```

### 3.2 Chapter Map List

Each chapter is a self-contained world chunk (or series of connected chunks). Implement each as its own GLB + a `ChapterConfig` object.

| Chapter | Environment Type | Key Features to Implement |
|---|---|---|
| **Windy** | Rolling countryside hub | Wind physics on grass, scarecrows, beehive, barn |
| **Hungover** | Farmland / barn | Pitchfork-throwing farmer, hay bales, Mrs. Bee boss |
| **Barn Boys** | Mechanical barn | Hay-stacking puzzle, Sergeant machinery, pitchfork combat |
| **Bats Tower** | Gothic tower at night | Bat swarms, gargoyle boss, vertical platforming |
| **Uga Buga** | Prehistoric cavern | Dinosaur riding, tribal enemies, fire hazards |
| **Spooky** | Halloween forest | Zombie hordes (survival wave mode), mansion |
| **It's War** | WWII battlefield | Trenches, cover system, machine gun nests, tanks |
| **Heist** | Bank vault | Stealth-optional, safe cracking, vault swim |
| **Future World** | Sci-fi facility | Zero-gravity sections, Alien parody boss |

### 3.3 Collision System

Use a layered approach since Three.js has no built-in physics:

```js
// Integrate with Rapier.js (WASM) for physics — lightweight and browser-ready
import RAPIER from '@dimforge/rapier3d-compat';

export class PhysicsWorld {
  async init() {
    await RAPIER.init();
    this.world = new RAPIER.World({ x: 0, y: -20, z: 0 }); // gravity
    this.bodies = new Map(); // THREE.Object3D.uuid → RigidBody
  }

  addStaticMesh(threeMesh) {
    const desc = RAPIER.RigidBodyDesc.fixed();
    const body = this.world.createRigidBody(desc);
    // Auto-generate trimesh collider from geometry
    const geo = threeMesh.geometry;
    const verts = new Float32Array(geo.attributes.position.array);
    const indices = new Uint32Array(geo.index.array);
    const collider = RAPIER.ColliderDesc.trimesh(verts, indices);
    this.world.createCollider(collider, body);
  }

  step(delta) {
    this.world.timestep = delta;
    this.world.step();
  }
}
```

### 3.4 Trigger Volumes

Used for: chapter events, cutscene triggers, enemy spawns, context-sensitive prompt zones.

```js
export class TriggerVolume {
  constructor(mesh, onEnter, onExit = null) {
    this.bounds = new THREE.Box3().setFromObject(mesh);
    this.onEnter = onEnter;
    this.onExit = onExit;
    this.wasInside = false;
  }

  check(position) {
    const inside = this.bounds.containsPoint(position);
    if (inside && !this.wasInside) this.onEnter();
    if (!inside && this.wasInside && this.onExit) this.onExit();
    this.wasInside = inside;
  }
}
```

---

## 4. Character System

### 4.1 Conker — Player Controller

Conker's movement is the foundation of everything. Replicate the original's "floaty but precise" feel.

```js
// characters/CharacterController.js
export class CharacterController {
  constructor(physicsBody, model, animator) {
    this.body = physicsBody;
    this.model = model;
    this.animator = animator;

    // Tuned to feel like original
    this.moveSpeed     = 7.5;
    this.runSpeed      = 14.0;
    this.jumpForce     = 10.5;
    this.doubleJumpForce = 8.0;
    this.rollSpeed     = 18.0;

    this.state = 'idle';   // idle | run | jump | fall | roll | attack | swim | context
    this.grounded = false;
    this.canDoubleJump = false;
    this.health = 3;       // honey pots (each = 1 hit)
    this.money = 0;        // squirrel tails / dollar bills

    this.contextAction = null;  // set by proximity to context zones
  }

  update(input, delta) {
    this._handleMovement(input, delta);
    this._handleJump(input);
    this._handleRoll(input);
    this._handleAttack(input);
    this._handleContext(input);
    this._syncModel();
    this._updateAnimator();
  }

  _handleMovement(input, delta) {
    const dir = new THREE.Vector3(input.horizontal, 0, input.vertical).normalize();
    if (dir.length() > 0.1) {
      const speed = input.run ? this.runSpeed : this.moveSpeed;
      // Apply velocity through physics body
      const vel = this.body.linvel();
      this.body.setLinvel({ x: dir.x * speed, y: vel.y, z: dir.z * speed }, true);
      // Face direction of movement
      const angle = Math.atan2(dir.x, dir.z);
      this.model.rotation.y = THREE.MathUtils.lerp(
        this.model.rotation.y, angle, 0.18
      );
      this.state = input.run ? 'run' : 'walk';
    } else {
      this.state = 'idle';
    }
  }

  _handleJump(input) {
    if (input.jumpPressed) {
      if (this.grounded) {
        this.body.applyImpulse({ x: 0, y: this.jumpForce, z: 0 }, true);
        this.canDoubleJump = true;
        this.state = 'jump';
        this.animator.play('jump');
      } else if (this.canDoubleJump) {
        this.body.setLinvel({ x: this.body.linvel().x, y: 0, z: this.body.linvel().z }, true);
        this.body.applyImpulse({ x: 0, y: this.doubleJumpForce, z: 0 }, true);
        this.canDoubleJump = false;
        this.animator.play('doublejump');
      }
    }
  }

  _handleRoll(input) {
    if (input.rollPressed && this.grounded && this.state !== 'roll') {
      this.state = 'roll';
      const dir = new THREE.Vector3(input.horizontal, 0, input.vertical).normalize();
      this.body.applyImpulse({ x: dir.x * this.rollSpeed, y: 2, z: dir.z * this.rollSpeed }, true);
      this.animator.playOnce('roll', () => this.state = 'idle');
    }
  }

  takeDamage(amount = 1) {
    this.health -= amount;
    if (this.health <= 0) this._die();
    else this.animator.playOnce('hurt');
  }
}
```

### 4.2 Conker States (Full State Machine)

```
idle → walk → run → jump → double_jump → fall → land
                          ↘ swim_surface → swim_dive → swim_surface
                                          ↘ drown (no air)
idle → roll (ground only)
idle → tail_whip → combo_whip_2 → combo_whip_3
idle → context_action (varies by zone: drink beer, use gun, ride, etc.)
any  → hurt → (resume)
any  → dead → respawn
```

### 4.3 Health & Currency

- **Health**: displayed as honey pots (1–3). Refill by picking up honey.
- **Money**: Conker collects "money" throughout levels. Some doors/items require payment.
- Store both in `PlayerState` singleton, persist to `SaveManager`.

---

## 5. Combat & Weapons

### 5.1 Tail Whip (Default Melee)

```js
export class TailWhip {
  constructor(conkerModel) {
    this.hitbox = new THREE.Sphere(conkerModel.position, 1.8);
    this.damage = 1;
    this.comboWindow = 0.5; // seconds to chain next attack
    this.comboStep = 0;
  }

  attack(enemies, onHit) {
    enemies.forEach(enemy => {
      if (this.hitbox.containsPoint(enemy.position)) {
        enemy.takeDamage(this.damage);
        onHit(enemy);
      }
    });
    this.comboStep = (this.comboStep + 1) % 3;
  }
}
```

### 5.2 Context Weapons (equipped per chapter)

Each weapon is unlocked via context zones. Implement as swappable modules:

| Weapon | Chapter | Mechanic |
|---|---|---|
| Frying Pan | Barn Boys | Heavy swing, stun |
| Shotgun (Sawn-off) | Various | Hitscan, 2-shot |
| Flamethrower | Uga Buga | Cone AoE fire |
| Bazooka | It's War | Projectile, splash |
| Sniper Rifle | It's War | Zoom, 1-shot |
| Katana | Future World | Fast multi-slash |
| Machine Gun | War (mounted) | Hold trigger, spread |

```js
// combat/WeaponManager.js
export class WeaponManager {
  constructor() {
    this.equipped = null;
    this.registry = new Map();
  }

  register(id, WeaponClass) {
    this.registry.set(id, WeaponClass);
  }

  equip(id, ...args) {
    if (this.registry.has(id)) {
      this.equipped = new (this.registry.get(id))(...args);
    }
  }

  fire(origin, direction, scene) {
    if (this.equipped) this.equipped.fire(origin, direction, scene);
  }
}

// Example: Shotgun
export class Shotgun {
  constructor() {
    this.ammo = 2;
    this.spread = 0.08;
    this.range = 20;
    this.damage = 2;
  }

  fire(origin, direction, scene) {
    if (this.ammo <= 0) return;
    // Cast 5 rays with spread for pellet simulation
    for (let i = 0; i < 5; i++) {
      const spreadDir = direction.clone().add(
        new THREE.Vector3(
          (Math.random() - 0.5) * this.spread,
          (Math.random() - 0.5) * this.spread,
          0
        )
      ).normalize();
      Raycaster.cast(origin, spreadDir, this.range, hit => {
        if (hit.enemy) hit.enemy.takeDamage(this.damage);
        SpawnDecal(hit.point, hit.normal, scene);
      });
    }
    this.ammo--;
    AudioManager.play('sfx_shotgun_fire', origin);
  }
}
```

---

## 6. Context-Sensitive Actions (The B-Button System)

This is the **most iconic mechanic** in the game. A single button performs entirely different actions based on what Conker is near.

### 6.1 Architecture

```js
// combat/ContextSystem.js
export class ContextSystem {
  constructor() {
    this.zones = [];        // ContextZone[]
    this.activeZone = null;
  }

  registerZone(zone) {
    this.zones.push(zone);
  }

  update(playerPosition) {
    this.activeZone = null;
    for (const zone of this.zones) {
      if (zone.bounds.containsPoint(playerPosition)) {
        this.activeZone = zone;
        HUD.showContextPrompt(zone.label, zone.iconKey);
        return;
      }
    }
    HUD.hideContextPrompt();
  }

  activate(player) {
    if (this.activeZone) {
      this.activeZone.action(player);
    }
  }
}

export class ContextZone {
  constructor({ position, radius, label, iconKey, action }) {
    this.bounds = new THREE.Sphere(position, radius);
    this.label  = label;    // e.g. "Drink Beer"
    this.iconKey = iconKey; // HUD icon reference
    this.action = action;   // (player) => void
  }
}
```

### 6.2 Example Context Zone Definitions

```js
// chapters/Hungover/hungoverContextZones.js

// Beer keg — restores health
new ContextZone({
  position: kegMesh.position,
  radius: 2.0,
  label: 'Chug Beer',
  iconKey: 'icon_beer',
  action: (player) => {
    player.animator.playOnce('drink');
    player.health = Math.min(player.health + 1, 3);
    AudioManager.play('sfx_drink');
  }
});

// Barrel — Conker hides inside
new ContextZone({
  position: barrelMesh.position,
  radius: 1.5,
  label: 'Hide',
  iconKey: 'icon_barrel',
  action: (player) => {
    player.state = 'hiding';
    player.model.visible = false;
    barrelMesh.userData.occupied = true;
  }
});

// Catapult launch pad
new ContextZone({
  position: catapultMesh.position,
  radius: 2.5,
  label: 'Launch',
  iconKey: 'icon_launch',
  action: (player) => {
    player.body.applyImpulse({ x: 0, y: 35, z: -20 }, true);
    CameraRig.setMode('cinematic', 3.0); // dramatic follow
    AudioManager.play('sfx_launch');
  }
});
```

---

## 7. NPC & Enemy AI

### 7.1 Base Enemy Class

```js
// ai/Enemy.js
export class Enemy {
  constructor(model, physicsBody, config) {
    this.model = model;
    this.body = physicsBody;
    this.health = config.health;
    this.damage = config.damage;
    this.sightRange = config.sightRange || 15;
    this.attackRange = config.attackRange || 2;
    this.moveSpeed = config.moveSpeed || 5;
    this.state = 'idle'; // idle | patrol | chase | attack | hurt | dead
    this.target = null;
    this.patrolPoints = config.patrolPoints || [];
    this.patrolIndex = 0;
  }

  update(player, delta) {
    switch (this.state) {
      case 'idle':    this._idle(player); break;
      case 'patrol':  this._patrol(delta); break;
      case 'chase':   this._chase(player, delta); break;
      case 'attack':  this._attack(player); break;
    }
  }

  _idle(player) {
    const dist = this.model.position.distanceTo(player.model.position);
    if (dist < this.sightRange) {
      this.state = 'chase';
      this.target = player;
    } else if (this.patrolPoints.length > 0) {
      this.state = 'patrol';
    }
  }

  _patrol(delta) {
    const target = this.patrolPoints[this.patrolIndex];
    const dir = target.clone().sub(this.model.position).normalize();
    this.body.setLinvel({ x: dir.x * this.moveSpeed, y: this.body.linvel().y, z: dir.z * this.moveSpeed }, true);
    if (this.model.position.distanceTo(target) < 0.5) {
      this.patrolIndex = (this.patrolIndex + 1) % this.patrolPoints.length;
    }
  }

  _chase(player, delta) {
    const dist = this.model.position.distanceTo(player.model.position);
    if (dist > this.sightRange * 1.5) { this.state = 'patrol'; return; }
    if (dist < this.attackRange) { this.state = 'attack'; return; }
    const dir = player.model.position.clone().sub(this.model.position).normalize();
    this.body.setLinvel({ x: dir.x * this.moveSpeed, y: this.body.linvel().y, z: dir.z * this.moveSpeed }, true);
  }

  takeDamage(amount) {
    this.health -= amount;
    this.state = 'hurt';
    if (this.health <= 0) this._die();
    else setTimeout(() => this.state = 'chase', 400);
  }

  _die() {
    this.state = 'dead';
    this.animator.playOnce('death', () => {
      this.body.remove();
      this.model.parent.remove(this.model);
    });
    this.onDeath?.();
  }
}
```

### 7.2 Enemy Roster by Chapter

| Enemy | Chapter | Behavior Notes |
|---|---|---|
| Wasp Drones | Hungover | Aerial patrol, dive-bomb attack |
| Bees (Mrs.) | Hungover | Boss — phases: chase, charge, stun |
| Zombie Scarecrow | Windy | Shamble toward player, knockback on hit |
| Zombie Bat | Bats Tower | Swoop attack, group flocking |
| Rock Soldier | Uga Buga | Shield blocks front, flank required |
| Dinosaur (riding) | Uga Buga | Player mounts — stomp mechanic |
| Tediz Soldier | It's War | Cover-seek, suppressing fire, flank |
| Tediz Heavy | It's War | Minigun, slow movement, high health |
| Xenomorph | Future World | Wall-crawl, ceiling drop, acid spit |
| The Big Big Guy | Barn Boys | Boss — weak point on back, circle-strafe |

### 7.3 Boss Framework

```js
// ai/BossEnemy.js
export class BossEnemy extends Enemy {
  constructor(model, physicsBody, config) {
    super(model, physicsBody, config);
    this.phases = config.phases;  // [{ healthThreshold, behavior }]
    this.currentPhase = 0;
    this.isEnraged = false;
  }

  update(player, delta) {
    super.update(player, delta);
    this._checkPhaseTransition();
  }

  _checkPhaseTransition() {
    const nextPhase = this.phases[this.currentPhase + 1];
    if (nextPhase && this.health <= nextPhase.healthThreshold) {
      this.currentPhase++;
      this._enterPhase(this.phases[this.currentPhase]);
    }
  }

  _enterPhase(phase) {
    this.isEnraged = true;
    this.moveSpeed *= 1.35;
    this.animator.playOnce('enrage');
    AudioManager.playOneshot('sfx_boss_enrage');
    CameraRig.shake(0.5, 1.2);
    phase.behavior(this);
  }
}
```

---

## 8. Chapters / Story Progression

### 8.1 ChapterDirector

A scripted event system that drives cutscenes, chapter unlocks, and narrative beats.

```js
// chapters/ChapterDirector.js
export class ChapterDirector {
  constructor(worldManager, cutsceneSystem, saveManager) {
    this.world = worldManager;
    this.cutscenes = cutsceneSystem;
    this.save = saveManager;
    this.chapters = [];
    this.currentChapter = null;
  }

  registerChapter(chapterConfig) {
    this.chapters.push(chapterConfig);
  }

  async startChapter(chapterId) {
    const config = this.chapters.find(c => c.id === chapterId);
    if (!config) return;
    await this.world.loadChunk(config.chunkId);
    if (config.openingCutscene && !this.save.hasSeen(config.openingCutscene)) {
      await this.cutscenes.play(config.openingCutscene);
      this.save.markSeen(config.openingCutscene);
    }
    this.currentChapter = config;
    config.onStart?.();
  }

  completeObjective(objectiveId) {
    this.save.completeObjective(objectiveId);
    this.currentChapter?.onObjective?.(objectiveId);
  }

  triggerChapterEnd() {
    this.save.markChapterComplete(this.currentChapter.id);
    this.cutscenes.play(this.currentChapter.endingCutscene).then(() => {
      this.world.transition('windy', 'spawn_main');
    });
  }
}
```

### 8.2 Example Chapter Config — "It's War"

```js
ChapterDirector.registerChapter({
  id: 'its_war',
  chunkId: 'world_war',
  title: "It's War!",
  unlockRequires: ['barn_boys_complete', 'bats_tower_complete'],
  openingCutscene: 'cutscene_war_intro',
  endingCutscene: 'cutscene_war_end',

  objectives: [
    { id: 'war_reach_trenches',    label: 'Reach the trenches' },
    { id: 'war_kill_tediz_squad',  label: 'Eliminate Tediz squad (12)' },
    { id: 'war_blow_bridge',       label: 'Destroy the bridge' },
    { id: 'war_rescue_squirrels',  label: 'Rescue captured squirrels (3)' },
    { id: 'war_defeat_general',    label: 'Defeat General Tediz' }
  ],

  onStart: () => {
    WeaponManager.equip('shotgun');
    WeaponManager.equip('sniper');
    EnemySpawner.spawnGroup('tediz_patrol', 4, warPatrolPoints);
    AudioManager.setAmbient('music_war_ambient');
  },

  onObjective: (id) => {
    if (id === 'war_blow_bridge') {
      ExplosionFX.play(bridgeMesh.position);
      bridgeMesh.parent.remove(bridgeMesh);
      AudioManager.play('sfx_explosion_large', bridgeMesh.position);
    }
  }
});
```

---

## 9. Multiplayer Modes

The original shipped with a robust 4-player split-screen multiplayer. Implement these as discrete game modes, selectable from the main menu.

### 9.1 Multiplayer Framework

```js
// multiplayer/MultiplayerManager.js
export class MultiplayerManager {
  constructor(renderer, scene) {
    this.renderer = renderer;
    this.scene = scene;
    this.players = [];    // up to 4
    this.mode = null;     // active mode instance
    this.viewports = [];  // split-screen viewports
  }

  setupSplitScreen(playerCount) {
    // Divide the canvas into quadrants
    const w = this.renderer.domElement.clientWidth;
    const h = this.renderer.domElement.clientHeight;
    const configs = {
      2: [ [0, h/2, w/2, h/2], [w/2, h/2, w/2, h/2] ],
      3: [ [0, h/2, w/2, h/2], [w/2, h/2, w/2, h/2], [0, 0, w/2, h/2] ],
      4: [ [0, h/2, w/2, h/2], [w/2, h/2, w/2, h/2], [0, 0, w/2, h/2], [w/2, 0, w/2, h/2] ]
    };
    this.viewports = configs[playerCount].map(([x, y, vw, vh], i) => ({
      x, y, width: vw, height: vh,
      camera: this.players[i].camera
    }));
  }

  renderSplitScreen() {
    this.renderer.setScissorTest(true);
    for (const vp of this.viewports) {
      this.renderer.setViewport(vp.x, vp.y, vp.width, vp.height);
      this.renderer.setScissor(vp.x, vp.y, vp.width, vp.height);
      this.renderer.render(this.scene, vp.camera);
    }
    this.renderer.setScissorTest(false);
  }

  startMode(ModeCls, map) {
    this.mode = new ModeCls(this.players, this.scene, map);
    this.mode.start();
  }
}
```

### 9.2 Mode: Beach (Deathmatch)

Classic arena deathmatch. Players kill each other; first to X kills wins.

```js
// multiplayer/modes/BeachMode.js
export class BeachMode {
  constructor(players, scene, map) {
    this.players = players;
    this.scene = scene;
    this.map = map;
    this.killLimit = 10;
    this.kills = new Map(players.map(p => [p.id, 0]));
    this.weapons = ['shotgun', 'bazooka', 'flamethrower'];
  }

  start() {
    this.map.load('mp_beach');
    this.players.forEach(p => {
      p.spawn(this.map.randomSpawn());
      WeaponManager.equip(p, this.weapons[Math.floor(Math.random() * this.weapons.length)]);
      p.onDeath = (killer) => this._onKill(killer, p);
    });
    this.hud = new MultiHUD(this.kills);
    AudioManager.setAmbient('music_mp_beach');
  }

  _onKill(killer, victim) {
    this.kills.set(killer.id, this.kills.get(killer.id) + 1);
    this.hud.update(this.kills);
    victim.respawn(this.map.randomSpawn(), 3000);
    if (this.kills.get(killer.id) >= this.killLimit) {
      this._endGame(killer);
    }
  }

  _endGame(winner) {
    AudioManager.play('sfx_win');
    VictoryScreen.show(winner);
  }
}
```

### 9.3 Mode: Heist

Two teams: Robbers vs Guards. Robbers carry cash to an escape van; Guards eliminate them.

```js
// multiplayer/modes/HeistMode.js
export class HeistMode {
  constructor(players, scene, map) {
    this.robbers = players.slice(0, 2);
    this.guards  = players.slice(2, 4);
    this.cashCarried = 0;
    this.cashGoal = 5;
    this.map = map;
  }

  start() {
    this.map.load('mp_heist_bank');
    this.robbers.forEach(p => {
      p.spawn(this.map.getSpawn('robber'));
      p.team = 'robbers';
      WeaponManager.equip(p, 'shotgun');
    });
    this.guards.forEach(p => {
      p.spawn(this.map.getSpawn('guard'));
      p.team = 'guards';
      WeaponManager.equip(p, 'rifle');
    });
    this._spawnCashBags();
  }

  _spawnCashBags() {
    this.cashPositions = this.map.getCashSpawns();
    this.cashPositions.forEach(pos => {
      const bag = new PickupItem('cash_bag', pos);
      bag.onPickup = (player) => {
        if (player.team === 'robbers') {
          player.carrying = 'cash';
          this._checkDelivery(player);
        }
      };
      this.scene.add(bag.mesh);
    });
  }

  _checkDelivery(player) {
    const vanZone = this.map.getEscapeZone();
    // Check each frame if carrier enters van zone
    player.onEnterTrigger = (zone) => {
      if (zone === vanZone && player.carrying === 'cash') {
        this.cashCarried++;
        player.carrying = null;
        if (this.cashCarried >= this.cashGoal) this._robbersWin();
      }
    };
  }
}
```

### 9.4 Mode: Race

Conker and friends race around a track on varied vehicles.

```js
// multiplayer/modes/RaceMode.js
export class RaceMode {
  constructor(players, scene, map) {
    this.players = players;
    this.laps = 3;
    this.checkpoints = [];
    this.progress = new Map(players.map(p => [p.id, { lap: 0, checkpoint: 0 }]));
  }

  start() {
    this.map.load('mp_race_track');
    this.checkpoints = this.map.getCheckpoints();
    this.players.forEach((p, i) => {
      p.spawn(this.map.getRaceStart(i));
      p.vehicle = VehicleFactory.create('cart', p);
    });
  }

  onCheckpoint(player, checkpointIndex) {
    const prog = this.progress.get(player.id);
    if (checkpointIndex === prog.checkpoint) {
      prog.checkpoint++;
      if (prog.checkpoint >= this.checkpoints.length) {
        prog.checkpoint = 0;
        prog.lap++;
        if (prog.lap >= this.laps) this._finishRace(player);
      }
    }
  }
}
```

### 9.5 Mode: War (Team Deathmatch — "It's War" map)

```js
// multiplayer/modes/WarMode.js
export class WarMode {
  constructor(players, scene, map) {
    this.squirrels = players.slice(0, 2); // team A
    this.tediz     = players.slice(2, 4); // team B
    this.teamKills = { squirrels: 0, tediz: 0 };
    this.killLimit = 15;
  }

  start() {
    this.map.load('mp_warzone');
    this.squirrels.forEach(p => {
      p.team = 'squirrels';
      p.spawn(this.map.getSpawn('squirrel'));
      WeaponManager.equip(p, 'rifle');
    });
    this.tediz.forEach(p => {
      p.team = 'tediz';
      p.spawn(this.map.getSpawn('tediz'));
      WeaponManager.equip(p, 'rifle');
    });
  }
}
```

### 9.6 Mode: Raptor (Survival / Capture)

Players are chased by a T-Rex. Last player alive wins, or survivors capture the egg.

```js
// multiplayer/modes/RaptorMode.js
export class RaptorMode {
  constructor(players, scene, map) {
    this.players = players;
    this.rexAI = null;
  }

  start() {
    this.map.load('mp_jungle');
    this.players.forEach(p => p.spawn(this.map.randomSpawn()));
    this.rexAI = new DinoAI({
      position: this.map.getRexSpawn(),
      targets: this.players,
      damage: 99,
      moveSpeed: 8
    });
  }
}
```

---

## 10. Camera System

Conker's camera is a critical part of the experience — it cinematic-ally adjusts to gameplay.

```js
// camera/CameraRig.js
export class CameraRig {
  constructor(camera) {
    this.camera = camera;
    this.target = null;
    this.mode = 'follow';   // follow | fixed | cinematic | aiming | boss

    // Follow camera config
    this.followOffset    = new THREE.Vector3(0, 3.5, -7);
    this.lookAheadFactor = 0.4;
    this.lerpSpeed       = 0.08;

    this._shakeIntensity = 0;
    this._shakeDuration  = 0;
  }

  setTarget(object3D) {
    this.target = object3D;
  }

  setMode(mode, duration = 0) {
    this.mode = mode;
    if (duration > 0) setTimeout(() => this.mode = 'follow', duration * 1000);
  }

  update(delta) {
    if (!this.target) return;
    switch (this.mode) {
      case 'follow':    this._updateFollow(delta); break;
      case 'aiming':    this._updateAiming(delta); break;
      case 'cinematic': this._updateCinematic(delta); break;
      case 'boss':      this._updateBoss(delta); break;
    }
    this._applyShake(delta);
  }

  _updateFollow(delta) {
    const targetPos = this.target.position.clone();
    const vel = this.target.userData.velocity || new THREE.Vector3();
    const lookAhead = vel.clone().multiplyScalar(this.lookAheadFactor);
    const desiredPos = targetPos.clone()
      .add(this.followOffset.clone().applyQuaternion(this.target.quaternion));
    this.camera.position.lerp(desiredPos, this.lerpSpeed);
    this.camera.lookAt(targetPos.add(lookAhead).add(new THREE.Vector3(0, 1.5, 0)));
  }

  _updateAiming(delta) {
    // Over-the-shoulder for ranged weapons
    const shoulderOffset = new THREE.Vector3(0.6, 1.8, -3.5);
    const desiredPos = this.target.position.clone()
      .add(shoulderOffset.applyQuaternion(this.target.quaternion));
    this.camera.position.lerp(desiredPos, 0.15);
  }

  shake(intensity, duration) {
    this._shakeIntensity = intensity;
    this._shakeDuration  = duration;
  }

  _applyShake(delta) {
    if (this._shakeDuration <= 0) return;
    this._shakeDuration -= delta;
    const s = this._shakeIntensity;
    this.camera.position.x += (Math.random() - 0.5) * s;
    this.camera.position.y += (Math.random() - 0.5) * s;
  }
}
```

---

## 11. Audio Architecture

### 11.1 AudioManager

```js
// audio/AudioManager.js — built on Web Audio API + Three.js PositionalAudio
export class AudioManager {
  constructor(camera) {
    this.listener = new THREE.AudioListener();
    camera.add(this.listener);
    this.loader = new THREE.AudioLoader();
    this.sounds = new Map();
    this.musicTracks = new Map();
    this.currentMusic = null;
    this.musicVolume = 0.6;
    this.sfxVolume = 1.0;
  }

  async preload(manifest) {
    for (const { id, url, positional } of manifest) {
      const buffer = await this.loader.loadAsync(url);
      this.sounds.set(id, { buffer, positional });
    }
  }

  play(id, position = null) {
    const entry = this.sounds.get(id);
    if (!entry) return;
    const audio = entry.positional && position
      ? new THREE.PositionalAudio(this.listener)
      : new THREE.Audio(this.listener);
    audio.setBuffer(entry.buffer);
    audio.setVolume(this.sfxVolume);
    if (position && audio.isPositionalAudio) {
      audio.position.copy(position);
      audio.setRefDistance(5);
    }
    audio.play();
  }

  setAmbient(trackId) {
    if (this.currentMusic) {
      this.currentMusic.stop();
    }
    const entry = this.sounds.get(trackId);
    if (!entry) return;
    const track = new THREE.Audio(this.listener);
    track.setBuffer(entry.buffer);
    track.setLoop(true);
    track.setVolume(this.musicVolume);
    track.play();
    this.currentMusic = track;
  }
}
```

### 11.2 Audio Design Notes

- Use **layered music**: a base ambient track + a combat layer that cross-fades in when enemies are near.
- Every enemy type needs: idle loop, alert bark, attack bark, death sound.
- Conker needs: jump grunt, land grunt, hurt scream, death yell, idle humming.
- Context actions need clear UI audio feedback (hover click, activation sound).

---

## 12. Graphics Upgrade Targets

This is where the "updated graphics" come in. Use Three.js's modern pipeline:

### 12.1 Renderer Setup

```js
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.2;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
```

### 12.2 Lighting Per Chapter

| Chapter | Sky | Key Light | Fill Light | Special |
|---|---|---|---|---|
| Windy | HDR sky (daytime) | Warm directional sun | Blue ambient | Wind volumetric |
| Bats Tower | Night HDR | Cold moonlight | Near-black ambient | Dynamic torch point lights |
| It's War | Overcast HDR | Desaturated sun | Khaki ambient | Muzzle flash point lights |
| Future World | Dark sci-fi HDR | Cold-white directional | Emissive panels GI | Neon strip point lights |

### 12.3 Material Upgrades

All characters and environments use `MeshStandardMaterial` (PBR):

```js
const material = new THREE.MeshStandardMaterial({
  map:          colorTexture,          // albedo
  normalMap:    normalTexture,         // surface detail
  roughnessMap: roughnessTexture,
  metalnessMap: metalnessTexture,
  aoMap:        aoTexture,             // baked AO
});
```

### 12.4 Post-Processing (via three/addons or postprocessing npm)

```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass }     from 'three/addons/postprocessing/RenderPass.js';
import { UnrealBloomPass }from 'three/addons/postprocessing/UnrealBloomPass.js';
import { SSAOPass }       from 'three/addons/postprocessing/SSAOPass.js';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
composer.addPass(new SSAOPass(scene, camera, w, h));
composer.addPass(new UnrealBloomPass(new THREE.Vector2(w, h), 0.4, 0.4, 0.85));
```

### 12.5 Character Shader — Cel/Toon Hybrid

The original had a slightly cartoonish look. Blend PBR + cel quantization:

```glsl
// shaders/conkerChar.frag.glsl
uniform sampler2D map;
uniform float quantizeSteps;  // e.g. 4.0

void main() {
  vec4 color = texture2D(map, vUv);
  // Quantize lighting into bands
  float light = dot(normalize(vNormal), normalize(lightDir));
  light = floor(light * quantizeSteps) / quantizeSteps;
  gl_FragColor = vec4(color.rgb * (0.2 + light * 0.8), color.a);
}
```

### 12.6 Particle Systems

Use `THREE.Points` + custom shaders for:
- Explosion sparks
- Coin/money pickup shimmer
- Rain (Windy/War chapters)
- Fire (Uga Buga / Flamethrower)
- Snow (if applicable)

---

## 13. UI & HUD

### 13.1 HUD Components

Render the HUD as an HTML overlay on top of the canvas (CSS + JS), NOT as 3D objects:

```html
<!-- index.html overlay -->
<div id="hud">
  <div id="health-bar">
    <img id="honey-pot-1" class="honey active" src="/ui/honeypot.webp">
    <img id="honey-pot-2" class="honey active" src="/ui/honeypot.webp">
    <img id="honey-pot-3" class="honey active" src="/ui/honeypot.webp">
  </div>
  <div id="money-display">
    <span id="money-icon">💰</span>
    <span id="money-count">$0</span>
  </div>
  <div id="ammo-display" class="hidden">
    <span id="ammo-count">--</span>
  </div>
  <div id="context-prompt" class="hidden">
    <img id="context-icon" src="">
    <span id="context-label"></span>
    <kbd>B</kbd>
  </div>
  <div id="chapter-title" class="hidden"></div>
</div>
```

```js
// ui/HUD.js
export const HUD = {
  updateHealth(hp) {
    document.querySelectorAll('.honey').forEach((el, i) => {
      el.classList.toggle('active', i < hp);
      el.classList.toggle('empty', i >= hp);
    });
  },
  updateMoney(amount) {
    document.getElementById('money-count').textContent = `$${amount}`;
  },
  showContextPrompt(label, iconSrc) {
    const el = document.getElementById('context-prompt');
    el.classList.remove('hidden');
    document.getElementById('context-label').textContent = label;
    document.getElementById('context-icon').src = iconSrc;
  },
  hideContextPrompt() {
    document.getElementById('context-prompt').classList.add('hidden');
  },
  showChapterTitle(title) {
    const el = document.getElementById('chapter-title');
    el.textContent = title;
    el.classList.remove('hidden');
    setTimeout(() => el.classList.add('hidden'), 4000);
  }
};
```

### 13.2 Main Menu

Build as a full-screen HTML/CSS screen that sits above the canvas:
- **New Game / Continue** → triggers ChapterDirector
- **Multiplayer** → mode + player count selection
- **Options** → audio sliders, graphics quality, controls rebinding
- **Credits**

### 13.3 Pause Menu

```js
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') GameLoop.togglePause();
});
```

Pause menu must freeze physics world, freeze audio, and overlay a semi-transparent menu.

---

## 14. Cutscene & Dialogue System

### 14.1 CutsceneDirector

Cutscenes are scripted sequences of camera moves, animations, and dialogue.

```js
// cutscenes/CutsceneDirector.js
export class CutsceneDirector {
  constructor(cameraRig, audioManager) {
    this.rig = cameraRig;
    this.audio = audioManager;
    this.scripts = new Map();
    this.isPlaying = false;
  }

  register(id, steps) {
    this.scripts.set(id, steps);
  }

  async play(id) {
    const steps = this.scripts.get(id);
    if (!steps) return;
    this.isPlaying = true;
    GameLoop.pause('cutscene');
    for (const step of steps) {
      await this._executeStep(step);
    }
    GameLoop.resume('cutscene');
    this.isPlaying = false;
  }

  async _executeStep(step) {
    return new Promise(resolve => {
      switch (step.type) {
        case 'wait':
          setTimeout(resolve, step.duration * 1000);
          break;
        case 'moveCam':
          this.rig.moveTo(step.position, step.lookAt, step.duration).then(resolve);
          break;
        case 'dialogue':
          DialogueBox.show(step.speaker, step.text, step.portrait).then(resolve);
          break;
        case 'playAnim':
          step.target.animator.playOnce(step.anim, resolve);
          break;
        case 'playSFX':
          this.audio.play(step.id);
          resolve();
          break;
        case 'custom':
          Promise.resolve(step.fn()).then(resolve);
          break;
      }
    });
  }
}
```

### 14.2 Dialogue Box

```js
// ui/DialogueBox.js
export const DialogueBox = {
  show(speaker, text, portrait) {
    return new Promise(resolve => {
      const box = document.getElementById('dialogue-box');
      document.getElementById('dialogue-speaker').textContent = speaker;
      document.getElementById('dialogue-portrait').src = portrait;
      this._typewrite(text, document.getElementById('dialogue-text'), () => {
        box.classList.remove('hidden');
        document.addEventListener('keydown', function handler(e) {
          if (e.key === ' ' || e.key === 'Enter') {
            box.classList.add('hidden');
            document.removeEventListener('keydown', handler);
            resolve();
          }
        });
      });
    });
  },

  _typewrite(text, el, onDone) {
    el.textContent = '';
    let i = 0;
    const interval = setInterval(() => {
      el.textContent += text[i++];
      if (i >= text.length) { clearInterval(interval); onDone(); }
    }, 30);
  }
};
```

---

## 15. Save System

```js
// save/SaveManager.js
export class SaveManager {
  constructor(slot = 0) {
    this.slot = slot;
    this.key = `conker_save_${slot}`;
    this.data = this._load();
  }

  _load() {
    const raw = localStorage.getItem(this.key);
    return raw ? JSON.parse(raw) : this._defaultData();
  }

  _defaultData() {
    return {
      completedChapters: [],
      seenCutscenes: [],
      completedObjectives: [],
      money: 0,
      health: 3,
      lastChunk: 'windy',
      lastSpawn: 'spawn_main',
      playtime: 0
    };
  }

  save() {
    localStorage.setItem(this.key, JSON.stringify(this.data));
  }

  markChapterComplete(id) {
    if (!this.data.completedChapters.includes(id)) {
      this.data.completedChapters.push(id);
      this.save();
    }
  }

  hasSeen(cutsceneId) {
    return this.data.seenCutscenes.includes(cutsceneId);
  }

  markSeen(cutsceneId) {
    this.data.seenCutscenes.push(cutsceneId);
    this.save();
  }

  completeObjective(id) {
    if (!this.data.completedObjectives.includes(id)) {
      this.data.completedObjectives.push(id);
      this.save();
    }
  }

  isObjectiveComplete(id) {
    return this.data.completedObjectives.includes(id);
  }
}
```

---

## 16. Asset Pipeline

### 16.1 Models

- Source: Blender (.blend) → export as `.glb`
- All characters need: rigged skeleton, blend shapes for facial animation
- LODs: 3 levels per mesh (high, medium, low) — switch at 15m / 40m distance
- Naming convention: `COL_` prefix = collision mesh, `PORTAL_` = transition, `TRIGGER_` = event zone

### 16.2 Texture Pipeline

- Format: `.ktx2` with Basis compression for best GPU performance
- Albedo: sRGB, Roughness/Metal/AO: linear non-sRGB
- Resolution: Characters 1024×1024, Environments 2048×2048, UI 512×512

```bash
# Convert with basisu CLI
basisu input.png -output_file output.ktx2 -uastc -uastc_rdo_l 1.5
```

### 16.3 Audio

- Format: `.ogg` (broad browser support)
- SFX: mono, 44.1kHz
- Music: stereo, 44.1kHz, looping (loop points embedded in OGG comments)

---

## 17. Implementation Priority Order

Follow this sequence to build the game up incrementally:

### Phase 1 — Core Loop (Get Conker Moving)
1. `CharacterController` with full movement/jump/roll
2. `CameraRig` in follow mode
3. `PhysicsWorld` with Rapier integration
4. Basic `WorldManager` — load one chunk (Windy), walk around

### Phase 2 — Interaction
5. `ContextSystem` with 3 example zones
6. `TailWhip` combat + 1 enemy type (zombie scarecrow)
7. `HUD` — health, money, context prompt
8. `AudioManager` — footsteps, hits, ambient music

### Phase 3 — First Chapter (Hungover)
9. Full Hungover chapter with all objectives
10. `ChapterDirector` + opening/closing cutscenes
11. `DialogueBox` + `CutsceneDirector`
12. Mrs. Bee boss fight
13. `SaveManager`

### Phase 4 — Graphics Polish
14. PBR materials across all existing meshes
15. Post-processing stack (SSAO, Bloom)
16. Dynamic lighting per chapter
17. Cel-shader hybrid on Conker

### Phase 5 — Remaining Chapters
18. Implement chapters in story order: Barn Boys → Bats Tower → Uga Buga → Spooky → It's War → Heist → Future World

### Phase 6 — Multiplayer
19. Split-screen renderer
20. Beach (deathmatch) mode
21. Heist mode
22. War mode
23. Race mode
24. Raptor mode

### Phase 7 — Polish & QA
25. Full audio pass (all SFX, music layers)
26. Performance profiling (target 60fps on mid-range GPU)
27. Mobile/gamepad input support
28. Loading screens, main menu, credits

---

## Appendix A — Key Constants Reference

```js
export const GAME_CONSTANTS = {
  GRAVITY:               -20,
  PLAYER_MOVE_SPEED:     7.5,
  PLAYER_RUN_SPEED:      14.0,
  PLAYER_JUMP_FORCE:     10.5,
  PLAYER_DOUBLE_JUMP:    8.0,
  PLAYER_ROLL_SPEED:     18.0,
  MAX_HEALTH:            3,
  CAMERA_FOLLOW_LERP:    0.08,
  CAMERA_FOLLOW_OFFSET:  [0, 3.5, -7],
  ENEMY_SIGHT_RANGE:     15,
  ENEMY_ATTACK_RANGE:    2.0,
  CONTEXT_ZONE_RADIUS:   2.0,
  PORTAL_CHECK_INTERVAL: 100,   // ms
  SAVE_SLOT_COUNT:       3,
  MP_MAX_PLAYERS:        4,
  MP_KILL_LIMIT_DEFAULT: 10,
};
```

---

## Appendix B — Dependency List

```json
{
  "dependencies": {
    "three": "^0.165.0",
    "@dimforge/rapier3d-compat": "^0.12.0",
    "postprocessing": "^6.36.0"
  },
  "devDependencies": {
    "vite": "^5.0.0",
    "@types/three": "^0.165.0"
  }
}
```

---

*This guide is intended for autonomous agent implementation. Each section is self-contained and can be tackled in isolation. Always extend the existing framework — do not rewrite systems that already exist. When in doubt, favor modularity over performance optimization until Phase 7.*
