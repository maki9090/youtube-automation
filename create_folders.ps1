# create_folders.ps1
$base = "C:\Users\youmi\Desktop\YoutubeTemplate"

# 생성할 폴더 목록
$dirs = @(
    "credentials",
    "config",
    "data\trends_web",
    "data\trends_yt",
    "data\videos_meta",
    "archive\trends_web",
    "archive\trends_yt",
    "archive\videos_meta",
    "logs",
    "scripts",
    "state",
    "venv",
    "ffmpeg-master-latest-win64-gpl-shared"
)

foreach ($d in $dirs) {
    $full = Join-Path $base $d

    if (-not (Test-Path $full)) {
        # 폴더가 없으면 새로 생성
        New-Item -ItemType Directory -Path $full | Out-Null
        Write-Host "Created folder: $full"
    } else {
        Write-Host "Exists       : $full"
    }
}

# 빈 파일 생성 (존재하면 건너뜀)
$fileList = @(
    "config\config.json",
    "state\state.json",
    "logs\pipeline.log"
)
foreach ($f in $fileList) {
    $path = Join-Path $base $f
    if (-not (Test-Path $path)) {
        New-Item -ItemType File -Path $path | Out-Null
        Write-Host "Created file  : $path"
    } else {
        Write-Host "File exists   : $path"
    }
}
