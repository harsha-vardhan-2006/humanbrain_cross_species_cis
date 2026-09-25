# CROSS-SCALE ANALYSIS (E07)


All fly numbers read from frozen artifacts; all human numbers from E03/E03b/E04/E05 of this study. No absolute CIS values are compared across scales.


                                                   quantity                                                 fly_value                                                                                 human_value comparison_type                                                                                        note
        CIS distribution shift (target vs matched controls)                                    Cliff's delta = 0.0979 Cliff's delta = 0.100 (median across 801 subjects; residual CIS vs degree-matched controls)          DIRECT same effect-size statistic; fly cells vs matched cells, human nodes vs degree-matched nodes
Null survival of group-level CIS effect (degree-preserving)                        z = 1.21, p = 0.109 (NOT survived)   battery B (E04b/E05): see NULL_MODEL_REPORT; top-50 median vs 100 degree-preserving nulls          DIRECT                                         100-null degree-preserving ensembles on both scales
            Top-K enrichment vs tested universe (control A) K=50 visual_centrifugal: obs 21, enrich 11.7x, z_A = 14.5                                                        E05 system enrichment z_A per system      NORMALIZED                                 fly: cell classes; human: macro-systems; both label-shuffle
 Top-K enrichment vs degree-matched expectation (control B)          K=50: E_B 8.0, enrich 2.63x, z_B = 5.30, p ~1e-4                                              E05 z_B per system (degree-matched peer pools)          DIRECT                                          identical two-control design (E12-strong template)
                                 Chokepoint catalogue depth               50 nodes catalogued; 13 A_strong_chokepoint       top-100 catalogue (human_chokepoint_catalogue.csv); A/B classing pending E05 q-values     QUALITATIVE                                      class labels map to human systems via the 4S456 labels
                              Visual-system share of top-50        80% (visual_system_fraction_top50, e14_v2_summary)                                                           2% of top-50 nodes in Vis systems          DIRECT                                                                    fractions are scale-free


## Human top-50 composition


Subcortical_Cerebellar    26
SalVentAttn                8
Default                    5
Cont                       4
DorsAttn                   3
SomMot                     2
Limbic                     1
Vis                        1


## Catalogue head (population top-20)


 rank  node                 system  cis_population_mean  degree_population_mean  peer_pool_n  peer_median_cis  cis_excess_ratio  top50_member
    1   414 Subcortical_Cerebellar             0.004564              235.283396            4         0.004018          1.135722          True
    2   400 Subcortical_Cerebellar             0.004288              226.531835            4         0.004018          1.067061          True
    3   415 Subcortical_Cerebellar             0.003749              227.485643            4         0.004018          0.932939          True
    4   401 Subcortical_Cerebellar             0.003417              213.342072            3         0.003749          0.911424          True
    5   451 Subcortical_Cerebellar             0.002057              144.687890            7         0.001091          1.885519          True
    6   442 Subcortical_Cerebellar             0.001985              159.056180            6         0.001522          1.303958          True
    7   444 Subcortical_Cerebellar             0.001821              158.838951            6         0.001522          1.196528          True
    8   286               DorsAttn             0.001446              124.590512            9         0.000797          1.814690          True
    9    97            SalVentAttn             0.001223              160.213483            6         0.001522          0.803472          True
   10   432 Subcortical_Cerebellar             0.001091              146.455680            7         0.001223          0.891900          True
   11   439 Subcortical_Cerebellar             0.001039              146.199750            7         0.001223          0.849781          True
   12   428 Subcortical_Cerebellar             0.001000              134.436954            9         0.001000          1.000000          True
   13   435 Subcortical_Cerebellar             0.000851              131.459426            6         0.000833          1.021941          True
   14   430 Subcortical_Cerebellar             0.000815              123.800250            9         0.000797          1.022700          True
   15   425 Subcortical_Cerebellar             0.000797              118.257179           13         0.000681          1.170043          True
   16   446 Subcortical_Cerebellar             0.000766              103.672909           26         0.000523          1.465469          True
   17   411 Subcortical_Cerebellar             0.000743              114.973783           18         0.000573          1.298186          True
   18   174                Default             0.000731              111.139825           17         0.000557          1.312069          True
   19   418 Subcortical_Cerebellar             0.000699              125.767790            8         0.000806          0.866960          True
   20   437 Subcortical_Cerebellar             0.000681              111.006242           17         0.000557          1.222299          True
