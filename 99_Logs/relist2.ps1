$L = 'F:\HumanBrain\00_Metadata\remote_listings'
$m = [ordered]@{
  'cls_hist_nii'   = 'BigBrainRelease.2015/3D_Classified_Volumes/Histological_Space/nii'
  'mri_nii'        = 'BigBrainRelease.2015/3D_MRI/nii'
  'roi_occipital'  = 'BigBrainRelease.2015/3D_ROIs/Occipital/nii'
  'roi_heschl'     = 'BigBrainRelease.2015/3D_ROIs/Heschl/nii'
  'roi_central'    = 'BigBrainRelease.2015/3D_ROIs/Central/nii'
  'roi_ba10'       = 'BigBrainRelease.2015/3D_ROIs/BA10/nii'
  'roi_hippo'      = 'BigBrainRelease.2015/3D_ROIs/Hippocampus/nii'
  'roi_hypothalamus' = 'BigBrainRelease.2015/3D_ROIs/Hypothalamus/nii'
  'roi_cerebellum' = 'BigBrainRelease.2015/3D_ROIs/Cerebellum/nii'
}
foreach($k in $m.Keys){
  $out = curl.exe -sS --max-time 30 --user anonymous:bigbrain@anonymous.org ("ftp://ftp.bigbrainproject.org/" + $m[$k] + '/') 2>&1 | Out-String
  Set-Content -Path (Join-Path $L ($k + '.txt')) -Value $out
  Write-Output "=== $k ==="
  Write-Output $out
}
Write-Output 'RELIST2_DONE'
