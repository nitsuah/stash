# Remora

![remora-home.png](https://raw.githubusercontent.com/nitsuah/stash/develop/projects/remora/assets/remora-home.png)

Remora is an Advanced Privileged Access Management (PAM) Tool built using Microsoft Access, Excel, and VBA. Built for a SecOps team it stores user access, links to other collected artifacts, and reports on role based access controls (RBAC) and provisioned access across multiple systems.

## Features

- **System Access** - Stores user directory lists for distributed softwares and reports on role based access controls (RBAC) and provisioned access across multiple systems.
- **Local Drive Storage**- Links to authorized signatory documents in shared folders for RBAC, and provisioning federal audits, and other artifact attachments. Also stores a compressed copy in the Access database.
  - `doc-links.vb` - generates a clickable link to the local drive storage for each artifact.
- **Global Search** - Search for users, systems, and artifacts across all records. Single search bar view into everything.
- **Automated Notifications** - It can even automate emails that would be sent to owners to requesst data or other details that may be missing. Never miss a sign-off or approval again!
- **Import Anything** - Import users and artifacts from any source. Joins data seamlessly into union by user email attribute. Batch load documents and attachments to local drive storage utilizing existing folder structure.
  - `file-batcher.vb` - batch loads access requests using a tracker file and a single combined pdf file.
  - `sat-rob-loader.vb` - batch loads other signatory forms using a tracker file and a single combined pdf file.
- **Export Anything** - Export users and artifacts. Generates automated exports for audits and other purposes. Splits external partner access by domain and generates encrypted files and confirmation emails for quarterly access audits.
- **Reports & More** Generate reports by system, company, organization, manager, user, and even by access or role!
- **Automated Backups** - Automated backups to local drive and cloud storage using ShadowCopy and OneDrive sync.
- **Event & Audit Logging** - Audit logs for all user actions and events. Keeps track of all additions and modifications by users.
  - `audit-log.vb` - logs all user actions and events.
- **Historical Tracking** - Tracks all changes to user access and artifacts. Keeps track of all additions and modifications by users.
- **Automated Health Checks** - Generates reports for unprivledged accounts, orphaned accounts, and other health checks around linked files and artifacts.
  - `import-cleanup.vb` - cleans up artifacts and generates reports of links to artifacts that no longer exist.
