# VHS Scanner — System Flow Diagrams

## Diagram 1 — Capture Types & Staging States

```mermaid
flowchart TD
    subgraph ENTRY["Entry Points"]
        BC["🔲 Barcode Scan\ncamera.js · ZXing / BarcodeDetector\n4 s debounce on lastCode"]
        IMG["📷 Image Capture\nbtn-cap / Space key\ncropFrame() from video stream"]
        MULTI["📚 Multi-Spine\ncropFrame() → 5 canvas slices\neach staged independently"]
        FILE["📁 File Upload\nbtn-upload → fileInput\nfileToB64() + fileToThumb()"]
        MANUAL["✏️ Manual Entry\n+ Add Tape modal\nskips all processing"]
    end

    BC -->|"addBarcodeCard(code)\n★ bypasses captureQueue entirely"| BC_LOOKUP["lookupBarcode()\nGET /api/lookup/barcode/:code\n1. UPCItemDB\n2. Open Library (ISBN-13)\n3. OMDb enrichment\n✦ no Ollama — fast path"]

    BC_LOOKUP -->|"title found"| BC_DUP{"Duplicate?\ntitle match via findDup()\nor barcode match\nin inventory"}
    BC_DUP -->|"yes"| TOAST_ERR["🔴 Toast: Already in collection\nreturn — nothing written"]
    BC_DUP -->|"no"| AUTO["Auto-confirm straight to collection\ndbAdd(rec) · inventory.push(rec)\nrenderInv() · _flashInvRow()\n🟢 Toast: Added"]
    BC_LOOKUP -->|"404 / null / error"| BC_CARD["Review card · processingState='ready'\nsource='barcode'\nbarcode pre-filled · title empty\n🟡 Toast: No match — enter title"]

    IMG & MULTI & FILE --> CQUEUE["captureQueue [ {base64, thumb} ]\nRendered in queue strip below camera\nItems individually removable"]
    CQUEUE -->|"⬤ Analyze N button\nor Enter key"| PROCESS["processQueue()"]

    PROCESS -->|"barcodeItems"| ADD_BC["addBarcodeCard()\nsame path as direct scan"]
    PROCESS -->|"imageItems"| APIKEY{"Claude\nAPI key set?"}

    APIKEY -->|"yes"| CLAUDE["callAI(base64)\n→ preprocessForAI() boost contrast 160%\n→ callClaude() Vision API\n→ verifyWithOmdb() if omdbKey\n→ addCard() per result\ncards arrive as processingState='ready'"]

    APIKEY -->|"no"| SERVER["POST /api/jobs per image\n{image, thumb}\n→ upload_jobs · status=pending\nCard 1: processingState='processing'\nCards 2+: processingState='queued'\n5s poll begins via startJobPoller()"]

    ADD_BC --> TAPES[("tapes table")]
    AUTO --> TAPES
    MANUAL --> TAPES
    CLAUDE --> REVPANEL["Review Panel"]
    SERVER --> REVPANEL
    BC_CARD --> REVPANEL
```

---

## Diagram 2 — Server Job Lifecycle (upload_jobs state machine)

```mermaid
stateDiagram-v2
    [*] --> pending : POST /api/jobs\nINSERT upload_jobs

    pending --> processing : processJobs() every 5 s\nSELECT pending LIMIT 1 FIFO\nUPDATE status=processing

    processing --> pending : STUCK RESET\nprocessJobs() detects\nupdated_at older than 10 min\nUPDATE status=pending

    processing --> transient_fail : Ollama error / timeout\nUPDATE status=failed\nretry_count++

    transient_fail --> pending : TRANSIENT RETRY\nretry_count < 3\nAND updated_at older than 60 s\nUPDATE status=pending retry_count reset

    transient_fail --> perm_fail : PERMANENT FAIL\nretry_count ≥ 3

    perm_fail --> [*] : INSERT review_item\nstatus=failed · source=scan\nfail_reason=error message\nDELETE upload_job

    processing --> zero_detected : Ollama returns 0 tapes

    zero_detected --> [*] : INSERT review_item\nstatus=failed · source=scan\nfail_reason=No tapes detected\nDELETE upload_job

    processing --> success : Ollama returns ≥1 tapes

    success --> [*] : OMDb enrich per tape\nlogScanAnalytics()\nINSERT review_item·pending per tape\nDELETE upload_job

    note right of pending
        Guard: if review_item already exists
        for this job_id (from stuck-reset
        double-processing), skip + delete job
    end note
```

---

## Diagram 3 — Review Card Lifecycle

```mermaid
stateDiagram-v2
    direction LR

    [*] --> processing : Image submitted to server\n(1st job in batch)\njobId = upload_job.id\ninflightSince = now

    [*] --> queued : Image submitted to server\n(2nd+ job in batch)\nwaiting for slot

    [*] --> ready : Barcode no-match\nor Claude API result\nor pollReviewItems() arrives\nwith source=manual/revalidate

    queued --> processing : pollReviewItems finds\nthe previous job's review_item\nnextQueued.processingState = 'processing'

    processing --> ready : pollReviewItems finds\nmatching review_item·pending\n(srcJobId === item.job_id)\nupgrades card · promotes next queued

    processing --> failed : pollReviewItems finds\nreview_item·failed

    ready --> confirmed : ✓ Confirm\n(see confirm flow)
    ready --> [*] : ✕ Discard\nDELETE review_item\nlog analytics: discarded (scan only)
    ready --> ready : 🔍 Lookup\nlookupMetadata(title)\nfills year/label/imdb_id/value_*/poster

    failed --> [*] : ✕ Discard\nDELETE review_item

    processing --> [*] : ⬛ Stop Processing\n_claimJob → DELETE upload_job
    queued --> [*] : ⬛ Stop Processing\n_claimJob → DELETE upload_job

    confirmed --> [*]

    note right of processing
        Stuck (client-side derived):
        processingState === 'processing'
        AND inflightSince > 10 min
        → CSS class card-failed
        → ↺ Retry button appears
        Retry: POST /api/jobs/:id/retry
        resets retry_count=0 status=pending
    end note
```

### Confirm routing

```mermaid
flowchart TD
    CONFIRM["confirmCard(uid)"]

    CONFIRM --> PROC{"processingState =\nprocessing or queued?"}
    PROC -->|"yes AND no title"| ABORT["abort — title must be\npre-filled before sending"]
    PROC -->|"no, or title present"| SRC{"card.source?"}

    SRC -->|"'fill' or 'revalidate'"| UPD["Find existing tape by tape_id\nApply only empty non-title fields\ndbPut(t)\n_claimJob → DELETE review_item\nToast: Updated"]

    SRC -->|"'scan' / 'barcode' / null"| TITLE{"title\npresent?"}
    TITLE -->|"no"| HILITE["Highlight title input red\nabort"]
    TITLE -->|"yes"| DUP{"findDup(title)\nduplicate?"}
    DUP -->|"yes"| ASK["askDup modal\nAdd anyway / Cancel"]
    DUP -->|"no"| GO
    ASK -->|"confirmed"| GO

    GO["rotateImage90CCW(thumb)\nID = barcode if valid UPC-format\n  AND not already used as an id\nelse nextId() → VHS-XXXX"]
    GO --> ADD["dbAdd(rec)\nPOST /api/tapes\ninventory.push(rec)"]
    ADD --> ANALYTICS["_reportOutcome()\nPOST /api/analytics/outcome\naction = accepted if title unchanged\naction = corrected if user edited AI title\n(only when card._aiTitle is set)"]
    ANALYTICS --> CLAIM["_claimJob(card)\nprocessing/queued → DELETE upload_job\nready/failed → DELETE review_item"]
    CLAIM --> FLASH["renderInv()\n_flashInvRow(id)\nToast: Added"]
```

---

## Diagram 4 — Collection Metadata Fields

```mermaid
flowchart LR
    subgraph CORE["🔵 Core — always set, always displayed"]
        C1["id\nVHS-XXXX or barcode UPC\nPrimary key + dedup guard"]
        C2["title\nRequired — search, sort, display,\nall views, lookup key for Fill"]
        C3["format\nVHS / DVD / Blu-ray / etc.\nfilter dropdown"]
        C4["condition\ngreat / good / fair / poor\nfilter, sort, badge color"]
        C5["status\nin_collection / for_sale / sold\n/ donated / missing / wanted\nfilter, bulk-update target"]
        C6["scanned_at\ndefault sort key\ndisplayed in table"]
    end

    subgraph ENRICHED["🟡 AI / OMDb enriched — Fill targets"]
        E1["year\nOMDb authoritative source\nfill target, sort, year-range slider"]
        E2["label\nVHS distributor / studio\nfill target, filter, display"]
        E3["imdb_id\nOMDb confidence gate for Fill\n(skip tape if no imdb_id match)\nanalytics log field"]
        E4["barcode\nUPC/EAN scan identifier\ndedup guard, UPC-as-id path"]
        E5["value_low / value_high\nUSD resale estimate\nClaude fill target, display, sort"]
    end

    subgraph TAGS["🟢 User-set"]
        T1["tags[]\nGenre chips (Horror, Sci-Fi, etc.)\nFilter chips UI · user-assigned"]
    end

    subgraph MEDIA["📷 Photo fields"]
        M1["photos[]\nFull gallery array\nDetail modal: rotate 90°, pin, delete\nSource of truth for all derived fields"]
        M2["photo_thumbnail\nAuto-set on confirm (thumb rotated 90°CCW)\nUniversal fallback across all views"]
        M3["photo_face\nUser-pinned in detail modal\nCover wall primary · StacksUp fallback"]
        M4["photo_spine\nUser-pinned in detail modal\nSpine wall primary · StacksUp primary\nCSS rotate(90deg) in StacksUp cards"]
    end

    subgraph LIGHT["⚪ Present — light use"]
        L1["condition_notes\nDetail modal only\nnot in table/wall · not filterable"]
        L2["sold_price\nDetail modal only\nshown when status = sold"]
        L3["notes\nTable column (mc-12)\nsearchable but rarely populated"]
    end

    subgraph VIEWS["Collection Views — photo fallback chain"]
        V0["wallMode 0 · Table/List\nphoto_spine ∥ photo_thumbnail"]
        V1["wallMode 1 · Cover Wall\nphoto_face ∥ photo_thumbnail"]
        V2["wallMode 2 · Spine Landscape\nphoto_spine ∥ photo_thumbnail"]
        V3["wallMode 3 · StacksUp\nphoto_spine (CSS rotate 90°CW)\n∥ photo_face ∥ photo_thumbnail"]
    end

    subgraph AUDIT["scan_analytics table (background — never displayed)"]
        A1["job_id · ai_model (llava:7b)\nsuggestions JSONB · omdb_verified\naction (accepted/corrected/discarded)\nfinal_title · final_year · final_label · imdb_id"]
    end

    M2 -.->|"fallback"| V0 & V1 & V2 & V3
    M3 -.->|"primary"| V1
    M3 -.->|"fallback"| V3
    M4 -.->|"primary"| V0 & V2 & V3
```
