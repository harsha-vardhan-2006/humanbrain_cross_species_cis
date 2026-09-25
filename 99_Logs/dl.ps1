param([string[]]$Items)  # each item: url|dest|expected_bytes
$ErrorActionPreference = 'Continue'
$logCsv = 'D:\HumanBrain\00_Metadata\download_manifest.csv'
if(-not (Test-Path $logCsv)){
  'timestamp,filename,url,drive,dest,expected_bytes,actual_bytes,status,seconds' | Set-Content $logCsv
}
$QUAR = @('D:\HumanBrain\99_Logs\QUARANTINE\','F:\HumanBrain\99_Logs\QUARANTINE\')
foreach($it in $Items){
  $p = $it -split '\|',3
  $url=$p[0]; $dest=$p[1]; $exp=[long]$p[2]
  $drive = $dest.Substring(0,1)
  $free = (Get-PSDrive $drive).Free
  if($free -lt 15GB){ Write-Output "STOP_DISKLOW|$dest|freeGB=$([math]::Round($free/1GB,1))"; break }
  if(Test-Path -LiteralPath $dest){
    $a=(Get-Item -LiteralPath $dest).Length
    if($exp -gt 0 -and $a -eq $exp){ Write-Output "SKIP_EXISTS|$dest|$a"; continue }
    $d="$dest"; $i=0
    while(Test-Path -LiteralPath $d){ $i++; $d = $dest -replace '(\.[^.]+)$', "_v$i`$1" }
    Write-Output "RENAME_EXISTING|$dest|size=$a|newname=$d"
    $dest = $d
  }
  $tmp = "$dest.part"
  if(Test-Path -LiteralPath $tmp){
    $pa=(Get-Item -LiteralPath $tmp).Length
    if($exp -gt 0 -and $pa -eq $exp){ Move-Item -LiteralPath $tmp -Destination $dest -Force; Write-Output "OK_FROM_PART|$dest|$pa"; continue }
    Write-Output "RESUME|$dest|part=$pa"
  }
  $t0 = Get-Date
  curl.exe -L -sS -C - --retry 4 --retry-delay 3 -o $tmp $url
  $rc = $LASTEXITCODE
  $t1 = Get-Date
  if($rc -ne 0 -or -not (Test-Path -LiteralPath $tmp)){ Write-Output "FAIL_CURL|$dest|rc=$rc"; continue }
  $a = (Get-Item -LiteralPath $tmp).Length
  if($exp -gt 0 -and $a -ne $exp){
    Write-Output "SIZE_MISMATCH|$dest|exp=$exp|act=$a"
    $q = $QUAR[[int]($drive -eq 'F')] + (Split-Path $dest -Leaf) + '.quarantine'
    Move-Item -LiteralPath $tmp -Destination $q -Force
    "$((Get-Date).ToString('s')),$(Split-Path $dest -Leaf),$url,$drive,$dest,$exp,$a,SIZE_MISMATCH_QUARANTINED,0" | Add-Content $logCsv
    continue
  }
  Move-Item -LiteralPath $tmp -Destination $dest -Force
  $secs = [math]::Round(($t1-$t0).TotalSeconds,1)
  Write-Output "OK|$dest|$a|$secs"
  "$((Get-Date).ToString('s')),$(Split-Path $dest -Leaf),$url,$drive,$dest,$exp,$a,OK,$secs" | Add-Content $logCsv
}
Write-Output 'BATCH_DONE'