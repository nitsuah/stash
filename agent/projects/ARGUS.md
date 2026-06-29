repo [[repos/odysseus|odysseus]]
# Project ARGUS: Obsidian External Data Integration Plan

This document outlines the plan to connect external data sources (Google Drive, Microsoft Todo) to your Obsidian vault for a more centralized and effective life prioritization system.

## Phase 1: Community Plugin Integration (Low-Effort, High-Reward)

We will start with well-supported community plugins. This is the fastest and most stable way to achieve our goal.

### 1.1. Google Drive Integration

**Goal:** Sync files from a specific Google Drive folder into your Obsidian vault for seamless access and search.

**Recommended Plugin:** `Remotely Save`

**Why this plugin?**

* It's one of the most popular and well-maintained sync plugins.
* It supports multiple cloud services, including Google Drive.
* It syncs automatically in the background.
* It's a one-way or two-way sync, giving you flexibility.

**Your Action Plan:**

1. Open Obsidian.
2. Go to `Settings` > `Community plugins`.
3. Turn off `Restricted mode` if it's on.
4. Click `Browse` and search for **"Remotely Save"**.
5. Click `Install`, then `Enable`.
6. Open the `Remotely Save` settings in Obsidian.
7. Choose `Google Drive` as the remote service and follow the on-screen instructions to authorize access.
8. Configure it to sync a specific folder from your Google Drive into a specific folder within your Obsidian vault (e.g., `Google Drive Sync/`).

### 1.2. Microsoft Todo Integration

**Goal:** Bring your MS Todo tasks into Obsidian to link them with notes and projects.

**Recommended Plugin:** `Obsidian Tasks` in combination with a sync service. Direct MS Todo integration is less common than using a bridge. The most effective bridge is `Todoist`.

**Why this approach?**

* `Obsidian Tasks` is the de-facto standard for task management within Obsidian. It allows powerful queries.
* MS Todo has a limited API for third-party apps compared to services like Todoist.
* You can set up a one-way sync from MS Todo to Todoist, and then use a Todoist plugin in Obsidian.

**Your Action Plan:**

### **Step A: Sync MS Todo with Todoist (if you don't use Todoist already)**

1. Use a service like `Zapier`, `IFTTT`, or `Integromat` to create a one-way sync. A common recipe is "If a new task is created in Microsoft To Do, create a task in Todoist". This is often free for a limited number of tasks per month.
2. *Alternative:* Some power users write a small script for this, but a service is easier to start.

### **Step B: Install Todoist Plugin in Obsidian**

1. In Obsidian, go to `Settings` > `Community plugins`.
2. Browse for **"Todoist Plugin"**.
3. Install and enable it.
4. Follow the plugin's instructions to link it to your Todoist account using an API token.

### 1.3. Evaluation Criteria

After setting up the plugins, we will assess their success based on these questions:

* **Google Drive:** Can you see and search for your Google Drive files within Obsidian? Does sync happen automatically?
* **MS Todo:** Can you see your tasks in Obsidian? Can you link them to your notes? Is the sync delay acceptable?
* **Claude Interaction:** Can I (Claude) read the synced files and task lists using the available MCP tools?

## Phase 2: Custom MCP Development (If Necessary)

If the community plugins are insufficient, we will proceed to build our own MCP servers. This gives us maximum control and "Claude-native" interaction.

**When do we move to this phase?**

* If `Remotely Save` is too slow, or you need more complex file-handling logic.
* If the MS Todo -> Todoist bridge is unreliable or you need direct, two-way MS Todo sync.
* If you want Claude to have more direct, API-level control over these services (e.g., "Claude, create a new Google Doc in my 'Projects' folder and add it to my 'Writing' list in MS Todo").

**Plan for Custom MCPs:**

1. **Design:** We will define the exact functions needed (e.g., `list_gdrive_files`, `get_gdrive_doc`, `create_ms_todo_task`).
2. **Implementation:** I will write the server code for the MCPs (likely in Python or Node.js).
3. **Deployment:** I will guide you on how to run these servers locally (e.g., via Docker).
4. **Integration:** We will use `mcp-add` to make these new tools available to me.

This phased approach ensures we take the path of least resistance first, and only invest in custom development if it's truly required.
