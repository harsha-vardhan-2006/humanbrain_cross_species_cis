$L = 'F:\HumanBrain\00_Metadata\remote_listings'
$m = [ordered]@{
  'surfaces_gii'        = 'BigBrainRelease.2015/3D_Surfaces/Apr7_2016/gii'
  'parcel_BB_Brainnetome' = 'BigBrainRelease.2015/Surface_Parcellations/BigBrain_space/Brainnetome'
  'parcel_BB_Surfaces'  = 'BigBrainRelease.2015/Surface_Parcellations/BigBrain_space/Surfaces'
  'parcel_fsLR_HCPMMP'  = 'BigBrainRelease.2015/Surface_Parcellations/fs_LR/HCP-MMP-1.0'
  'warp_white_surfaces' = 'BigBrainRelease.2015/BigBrainWarp_Support/white_surfaces'
  'warp_mni152_spheres' = 'BigBrainRelease.2015/BigBrainWarp_Support/BigBrain_to_MNI152/spheres'
  'warp_fsLR_spheres'   = 'BigBrainRelease.2015/BigBrainWarp_Support/BigBrain_to_fsLR/spheres'
  'hippo_gii'           = 'BigBrainRelease.2015/Hippocampus_Segmentation/gii'
}
foreach($k in $m.Keys){
  $out = curl.exe -sS --max-time 30 --user anonymous:bigbrain@anonymous.org ("ftp://ftp.bigbrainproject.org/" + $m[$k] + '/') 2>&1 | Out-String
  Set-Content -Path (Join-Path $L ($k + '.txt')) -Value $out
  Write-Output "=== $k ==="
  Write-Output $out
}
Write-Output 'RELIST_DONE'
