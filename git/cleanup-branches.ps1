# Script to clean up merged branches in all repositories
# Removes both local and remote branches that have been merged to main/master

param(
    [string]$Path = "c:\Users\ajhar\code",
    [switch]$DryRun = $false,
    [switch]$Force = $false
)

Write-Host "Cleaning up merged branches in: $Path" -ForegroundColor Cyan
Write-Host "Dry run: $DryRun" -ForegroundColor Yellow
Write-Host ""

# Get all git repositories
$repos = Get-ChildItem -Path $Path -Directory | Where-Object {
    Test-Path (Join-Path $_.FullName ".git")
}

foreach ($repo in $repos) {
    Write-Host "==================================================" -ForegroundColor Green
    Write-Host "Repository: $($repo.Name)" -ForegroundColor Green
    Write-Host "==================================================" -ForegroundColor Green
    
    Push-Location $repo.FullName
    
    try {
        # Fetch and prune remote references
        Write-Host "Fetching and pruning..." -ForegroundColor Yellow
        git fetch --all --prune | Out-Null
        
        # Get default branch (main or master)
        $defaultBranch = git symbolic-ref refs/remotes/origin/HEAD 2>$null
        if ($defaultBranch) {
            $defaultBranch = $defaultBranch -replace 'refs/remotes/origin/', ''
        } else {
            $defaultBranch = "main"
        }
        
        Write-Host "Default branch: $defaultBranch" -ForegroundColor Cyan
        
        # Get current branch
        $currentBranch = git branch --show-current
        Write-Host "Current branch: $currentBranch" -ForegroundColor Cyan
        
        # Switch to default branch if not already there
        if ($currentBranch -ne $defaultBranch) {
            Write-Host "Switching to $defaultBranch..." -ForegroundColor Yellow
            git checkout $defaultBranch 2>$null | Out-Null
            git pull 2>$null | Out-Null
        }
        
        # Find merged local branches
        $mergedBranches = git branch --merged $defaultBranch | 
            ForEach-Object { $_.Trim() } | 
            Where-Object { $_ -notmatch '^\*' -and $_ -ne $defaultBranch -and $_ -ne "master" -and $_ -ne "main" }
        
        if ($mergedBranches) {
            Write-Host "`nMerged local branches:" -ForegroundColor Yellow
            $mergedBranches | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
            
            if (-not $DryRun) {
                if ($Force -or (Read-Host "`nDelete these local branches? (y/n)") -eq 'y') {
                    foreach ($branch in $mergedBranches) {
                        Write-Host "Deleting local branch: $branch" -ForegroundColor Red
                        git branch -d $branch 2>&1 | Out-Null
                    }
                }
            }
        } else {
            Write-Host "`nNo merged local branches to delete." -ForegroundColor Green
        }
        
        # Find merged remote branches
        $remoteBranches = git branch -r --merged $defaultBranch | 
            ForEach-Object { $_.Trim() } | 
            Where-Object { 
                $_ -notmatch 'origin/HEAD' -and 
                $_ -notmatch "origin/$defaultBranch" -and 
                $_ -notmatch 'origin/master' -and
                $_ -notmatch 'origin/main'
            }
        
        if ($remoteBranches) {
            Write-Host "`nMerged remote branches:" -ForegroundColor Yellow
            $remoteBranches | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
            
            if (-not $DryRun) {
                if ($Force -or (Read-Host "`nDelete these remote branches? (y/n)") -eq 'y') {
                    foreach ($branch in $remoteBranches) {
                        $branchName = $branch -replace 'origin/', ''
                        Write-Host "Deleting remote branch: $branchName" -ForegroundColor Red
                        git push origin --delete $branchName 2>&1 | Out-Null
                    }
                }
            }
        } else {
            Write-Host "`nNo merged remote branches to delete." -ForegroundColor Green
        }
        
        Write-Host ""
        
    } catch {
        Write-Host "Error processing repository: $_" -ForegroundColor Red
    } finally {
        Pop-Location
    }
}

Write-Host "`n==================================================" -ForegroundColor Green
Write-Host "Cleanup complete!" -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Green
