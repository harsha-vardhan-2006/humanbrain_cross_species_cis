$log = 'D:\HumanBrain\99_Logs\watcher.log'
function Log($m){ "$((Get-Date).ToString('s')) $m" | Add-Content $log }
Log 'watcher started'
while($true){
  Start-Sleep -Seconds 120
  try {
    $m = Import-Csv D:\HumanBrain\00_Metadata\download_manifest.csv
    $ok = ($m | Where-Object {$_.status -in 'OK','SKIP_EXISTS','OK_FROM_PART'}).Count
    $bad = ($m | Where-Object {$_.status -notin 'OK','SKIP_EXISTS','OK_FROM_PART'}).Count
    $pycount = (Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
                Where-Object { $_.CommandLine -like '*dl_batch*' }).Count
    Log "progress: ok=$ok bad=$bad dl_batch_procs=$pycount"
  } catch { Log "poll error: $_"; continue }
  if($pycount -eq 0){
    Log 'downloaders finished; re-running straggler passes (resume-safe)'
    foreach($t in @('volumes','small')){
      $list = if($t -eq 'volumes'){'dl_D_volumes.txt'}else{'dl_D_small.txt'}
      try { py D:\HumanBrain\99_Logs\dl_batch.py "D:\HumanBrain\00_Metadata\$list" $t *>> "D:\HumanBrain\99_Logs\straggler_$t.log" } catch { Log "straggler $t error: $_" }
    }
    Log 'verification pass (gzip CRC + NIfTI/gii/PNG + SHA-256)'
    try { py D:\HumanBrain\99_Logs\verify_downloads.py *>> D:\HumanBrain\99_Logs\verify_run.log } catch { Log "verify error: $_" }
    Log 're-collect + finalize cross-species manifests'
    try { py D:\HumanBrain\99_Logs\csm_collect.py *>> D:\HumanBrain\99_Logs\csm_run.log } catch { Log "csm error: $_" }
    try { py D:\HumanBrain\99_Logs\csm_finalize.py *>> D:\HumanBrain\99_Logs\csm_run.log } catch { Log "csm finalize error: $_" }
    Log 'final acquisition report'
    try { py D:\HumanBrain\99_Logs\final_report.py *>> D:\HumanBrain\99_Logs\final_run.log } catch { Log "final report error: $_" }
    Log 'WATCHER_DONE'
    break
  }
}
