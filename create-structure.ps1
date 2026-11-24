
# ============================================================
# WorkMind API - Structure Creator
# Root directory: Script location
# ============================================================

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot

Write-Host "`nCreating WorkMind API structure..." -ForegroundColor Cyan

# Directories
$Directories = @(
    "app",
    "app/core",
    "app/api/v1",
    "app/db",

    "app/modules/auth",
    "app/modules/users",
    "app/modules/companies",
    "app/modules/knowledge",
    "app/modules/documents",
    "app/modules/training",
    "app/modules/workplace",
    "app/modules/development",
    "app/modules/search",

    "app/ai/providers",
    "app/ai/embeddings",
    "app/ai/retrieval",
    "app/ai/prompts",
    "app/ai/orchestration",

    "app/common",

    "alembic/versions",

    "tests/unit",
    "tests/integration",
    "tests/api",

    "scripts"
)

foreach ($Directory in $Directories) {
    $Path = Join-Path $Root $Directory

    if (!(Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "[DIR]  $Directory" -ForegroundColor DarkCyan
    }
}

# Files
$Files = @(
    "app/__init__.py",
    "app/main.py",

    "app/core/config.py",
    "app/core/security.py",
    "app/core/logging.py",
    "app/core/exceptions.py",

    "app/api/v1/router.py",
    "app/api/v1/dependencies.py",

    "app/db/base.py",
    "app/db/session.py",
    "app/db/init_db.py",

    "app/modules/auth/router.py",
    "app/modules/auth/service.py",
    "app/modules/auth/repository.py",
    "app/modules/auth/models.py",
    "app/modules/auth/schemas.py",

    "app/ai/providers/ollama.py",

    "app/common/permissions.py",
    "app/common/pagination.py",
    "app/common/constants.py",

    "alembic/env.py",

    "tests/conftest.py",

    "scripts/seed.py",

    ".env.example",
    ".gitignore",
    "alembic.ini",
    "pyproject.toml",
    "README.md"
)

foreach ($File in $Files) {
    $Path = Join-Path $Root $File

    if (!(Test-Path $Path)) {
        New-Item -ItemType File -Path $Path -Force | Out-Null
        Write-Host "[FILE] $File" -ForegroundColor Gray
    }
}

Write-Host "`nWorkMind API structure created!" -ForegroundColor Green

Write-Host "`nFinal project structure:" -ForegroundColor Cyan
tree $Root /F /A

Write-Host "`nCompleted successfully!" -ForegroundColor Green
