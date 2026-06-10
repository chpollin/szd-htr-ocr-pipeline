# QA-Report: GAMS-Ingest SZ-AAL-2026-06

Generiert von `c:/tmp/aal_qa_report.py`. Prueft pro Objekt die Kette
Lieferungs-Book-XML -> lokale Scans (Staging) -> GAMS-METS -> Pipeline-Backup.
GAMS-URL-Spalte basiert auf dem HEAD-Check aller IMG.n vom 2026-06-09.
Die Sprache steht in ALLEN 379 METS pauschal als 'Deutsch/de' (Cirilo-Default,
kein Katalogwert); die Book-XMLs der Lieferung enthalten gar kein Sprachfeld.

## Zusammenfassung

- Objekte gesamt: **379**, Seiten gesamt: **1599**
- Bilder vollstaendig konsistent (XML=lokal=METS=Backup, Masse OK, GAMS liefert): **379**
- Komplett ohne Befund: **353**
- Nur 'Datum leer': **23**
- Objekte mit sonstigen Befunden: **3**
- Transkribiert (Stand Reportlauf, Batch laeuft): **15**

## Befunde (alles ausser 'OK')

| Signatur | PID | Seiten XML | Autor | Datum | Befund |
|---|---|---|---|---|---|
| SZ-AAL/B1.110 | o:szd.3034 | 7 | BRIEFE GEHÖREN NICHT ZUSAMMEN! | - | Autor unueblich: 'BRIEFE GEHÖREN NICHT ZUSAMMEN!'; Datum leer |
| SZ-AAL/B10.9 | o:szd.3229 | 3 | Trading | 21.11.1938 | Autor unueblich: 'Trading' |
| SZ-AAL/B12 | o:szd.3231 | 7 | Beierle, Alfred | - | Datum leer |
| SZ-AAL/B19 | o:szd.3238 | 3 | Sambat, M. | - | Datum leer |
| SZ-AAL/B3.1 | o:szd.3338 | 3 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.110 | o:szd.3349 | 3 | Zweig, Stefan | - | Datum leer |
| SZ-AAL/B3.111 | o:szd.3350 | 5 | Zweig, Stefan | - | Datum leer |
| SZ-AAL/B3.112 | o:szd.3351 | 9 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.113 | o:szd.3352 | 3 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.114 | o:szd.3353 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.115 | o:szd.3354 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.116 | o:szd.3355 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.117 | o:szd.3356 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.118 | o:szd.3357 | 7 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.119 | o:szd.3358 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.120 | o:szd.3360 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.121 | o:szd.3361 | 11 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.122 | o:szd.3362 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.123 | o:szd.3363 | 9 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.124 | o:szd.3364 | 9 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.125 | o:szd.3365 | 5 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.126 | o:szd.3366 | 3 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.127 | o:szd.3367 | 3 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.128 | o:szd.3368 | 3 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.130 | o:szd.3369 | 3 | Zweig, Friderike | - | Datum leer |
| SZ-AAL/B3.138 | o:szd.3376 | 3 | Unidentified | 7.12.1938 | Autor unueblich: 'Unidentified' |

## Alle Objekte

| Signatur | PID | Seiten XML | lokal | METS | Backup | GAMS-URLs | Bildmasse | Objekttyp | Autor | Datum | Sprache erkannt | Transkribiert | Befund |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| SZ-AAL/B1.1 | o:szd.3020 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 20.12.1938 | en | ja | OK |
| SZ-AAL/B1.10 | o:szd.3021 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 29.1.1940 | de | ja | OK |
| SZ-AAL/B1.100 | o:szd.3022 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 15.2.1941 | en | ja | OK |
| SZ-AAL/B1.101 | o:szd.3023 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 17.2.1941 | en | ja | OK |
| SZ-AAL/B1.102 | o:szd.3024 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 02.1941 | en | ja | OK |
| SZ-AAL/B1.103 | o:szd.3025 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Lotte | 7.3.1941 | en | ja | OK |
| SZ-AAL/B1.104 | o:szd.3026 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 12.3.1941 | en | ja | OK |
| SZ-AAL/B1.105 | o:szd.3027 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 13.3.1941 | en | ja | OK |
| SZ-AAL/B1.106 | o:szd.3028 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 13.3.1941 | en | ja | OK |
| SZ-AAL/B1.107 | o:szd.3029 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 19.3.1941 | en | ja | OK |
| SZ-AAL/B1.108 | o:szd.3030 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 31.3.1941 | en | ja | OK |
| SZ-AAL/B1.109 | o:szd.3031 | 2 | 2 | 2 | 2 | OK | OK | Brief | Zweig, Lotte | 04.1941 | en | ja | OK |
| SZ-AAL/B1.109a | o:szd.3032 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Lotte | 04.1941 | en | ja | OK |
| SZ-AAL/B1.11 | o:szd.3033 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 4.4.1940 | en | ja | OK |
| SZ-AAL/B1.110 | o:szd.3034 | 7 | 7 | 7 | 7 | OK | OK | Brief | BRIEFE GEHÖREN NICHT ZUSAMMEN! | - | en | ja | Autor unueblich: 'BRIEFE GEHÖREN NICHT ZUSAMMEN!'; Datum leer |
| SZ-AAL/B1.111 | o:szd.3035 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 04.1941 | - | nein | OK |
| SZ-AAL/B1.112 | o:szd.3036 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 4.4.1941 | - | nein | OK |
| SZ-AAL/B1.113 | o:szd.3037 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 5.4.1941 | - | nein | OK |
| SZ-AAL/B1.114 | o:szd.3038 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 5.4.1941 | - | nein | OK |
| SZ-AAL/B1.115 | o:szd.3039 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.4.1941 | - | nein | OK |
| SZ-AAL/B1.116 | o:szd.3040 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 10.4.1941 | - | nein | OK |
| SZ-AAL/B1.117 | o:szd.3041 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 04.1941 | - | nein | OK |
| SZ-AAL/B1.118 | o:szd.3042 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 16.4.1941 | - | nein | OK |
| SZ-AAL/B1.119 | o:szd.3043 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 18.4.1941 | - | nein | OK |
| SZ-AAL/B1.12 | o:szd.3044 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 1940 | - | nein | OK |
| SZ-AAL/B1.120 | o:szd.3045 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 25.4.1941 | - | nein | OK |
| SZ-AAL/B1.121 | o:szd.3046 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 29.4.1941 | - | nein | OK |
| SZ-AAL/B1.122 | o:szd.3047 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 04.1941 | - | nein | OK |
| SZ-AAL/B1.123 | o:szd.3048 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 04.1941 | - | nein | OK |
| SZ-AAL/B1.124 | o:szd.3049 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 6.5.1941 | - | nein | OK |
| SZ-AAL/B1.125 | o:szd.3050 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 8.5.1941 | - | nein | OK |
| SZ-AAL/B1.126 | o:szd.3051 | 4 | 4 | 4 | 4 | OK | OK | Brief | Zweig, Stefan | 12.5.1941 | - | nein | OK |
| SZ-AAL/B1.127 | o:szd.3052 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 14.5.1941 | - | nein | OK |
| SZ-AAL/B1.128 | o:szd.3053 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 05.1941 | - | nein | OK |
| SZ-AAL/B1.129 | o:szd.3054 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 18.5.1941 | - | nein | OK |
| SZ-AAL/B1.13 | o:szd.3055 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 1940 | - | nein | OK |
| SZ-AAL/B1.130 | o:szd.3056 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 18.5.1941 | - | nein | OK |
| SZ-AAL/B1.131 | o:szd.3057 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 05.1941 | - | nein | OK |
| SZ-AAL/B1.132 | o:szd.3058 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 14.5.1941 | - | nein | OK |
| SZ-AAL/B1.133 | o:szd.3059 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 1.6.1941 | - | nein | OK |
| SZ-AAL/B1.134 | o:szd.3060 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 2.6.1941 | - | nein | OK |
| SZ-AAL/B1.135 | o:szd.3061 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 06.1941 | - | nein | OK |
| SZ-AAL/B1.136 | o:szd.3062 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 2.6.1941 | - | nein | OK |
| SZ-AAL/B1.137 | o:szd.3063 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 8.6.1941 | - | nein | OK |
| SZ-AAL/B1.138 | o:szd.3064 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 17.6.1941 | - | nein | OK |
| SZ-AAL/B1.139 | o:szd.3065 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 20.6.1941 | - | nein | OK |
| SZ-AAL/B1.14 | o:szd.3066 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 12.1939 | - | nein | OK |
| SZ-AAL/B1.140 | o:szd.3067 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 25.6.1941 | - | nein | OK |
| SZ-AAL/B1.141 | o:szd.3068 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 26.6.1941 | - | nein | OK |
| SZ-AAL/B1.142 | o:szd.3069 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 1.7.1941 | - | nein | OK |
| SZ-AAL/B1.143 | o:szd.3070 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 4.7.1941 | - | nein | OK |
| SZ-AAL/B1.144 | o:szd.3071 | 4 | 4 | 4 | 4 | OK | OK | Brief | Zweig, Stefan | 07.1941 | - | nein | OK |
| SZ-AAL/B1.145 | o:szd.3072 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 6.7.1941 | - | nein | OK |
| SZ-AAL/B1.146 | o:szd.3073 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 12.7.1941 | - | nein | OK |
| SZ-AAL/B1.147 | o:szd.3074 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 19.7.1941 | - | nein | OK |
| SZ-AAL/B1.148 | o:szd.3075 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 07.1941 | - | nein | OK |
| SZ-AAL/B1.149 | o:szd.3076 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 21.7.1941 | - | nein | OK |
| SZ-AAL/B1.15 | o:szd.3077 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 7.10.1939 | - | nein | OK |
| SZ-AAL/B1.150 | o:szd.3078 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 25.7.1941 | - | nein | OK |
| SZ-AAL/B1.151 | o:szd.3079 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 31.7.1941 | - | nein | OK |
| SZ-AAL/B1.152 | o:szd.3080 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 31.7.1941 | - | nein | OK |
| SZ-AAL/B1.153 | o:szd.3081 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 08.1941 | - | nein | OK |
| SZ-AAL/B1.154 | o:szd.3082 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 6.8.1941 | - | nein | OK |
| SZ-AAL/B1.155 | o:szd.3083 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 6.8.1941 | - | nein | OK |
| SZ-AAL/B1.156 | o:szd.3084 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 11.8.1941 | - | nein | OK |
| SZ-AAL/B1.157 | o:szd.3085 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 08.1941 | - | nein | OK |
| SZ-AAL/B1.158 | o:szd.3086 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 15.8.1941 | - | nein | OK |
| SZ-AAL/B1.159 | o:szd.3087 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 08.1941 | - | nein | OK |
| SZ-AAL/B1.16 | o:szd.3088 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 02.1940 | - | nein | OK |
| SZ-AAL/B1.160 | o:szd.3089 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 24.8.1941 | - | nein | OK |
| SZ-AAL/B1.161 | o:szd.3090 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 08.1941 | - | nein | OK |
| SZ-AAL/B1.162 | o:szd.3091 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Lotte | 31.8.1941 | - | nein | OK |
| SZ-AAL/B1.163 | o:szd.3092 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 4.9.1941 | - | nein | OK |
| SZ-AAL/B1.164 | o:szd.3093 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 09.1941 | - | nein | OK |
| SZ-AAL/B1.165 | o:szd.3094 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 13.9.1941 | - | nein | OK |
| SZ-AAL/B1.166 | o:szd.3095 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 13.9.1941 | - | nein | OK |
| SZ-AAL/B1.167 | o:szd.3096 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 09.1941 | - | nein | OK |
| SZ-AAL/B1.168 | o:szd.3097 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 3.10.1941 | - | nein | OK |
| SZ-AAL/B1.169 | o:szd.3098 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.1941 | - | nein | OK |
| SZ-AAL/B1.17 | o:szd.3099 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 02.1940 | - | nein | OK |
| SZ-AAL/B1.170 | o:szd.3100 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Lotte | 10.1941 | - | nein | OK |
| SZ-AAL/B1.171 | o:szd.3101 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.1941 | - | nein | OK |
| SZ-AAL/B1.172 | o:szd.3102 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 11.10.1941 | - | nein | OK |
| SZ-AAL/B1.173 | o:szd.3103 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.1941 | - | nein | OK |
| SZ-AAL/B1.174 | o:szd.3104 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 16.10.1941 | - | nein | OK |
| SZ-AAL/B1.175 | o:szd.3105 | 6 | 6 | 6 | 6 | OK | OK | Brief | Zweig, Lotte | 28.10.1941 | - | nein | OK |
| SZ-AAL/B1.176 | o:szd.3106 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.1941 | - | nein | OK |
| SZ-AAL/B1.177 | o:szd.3107 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 7.11.1941 | - | nein | OK |
| SZ-AAL/B1.178 | o:szd.3108 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 7.11.1941 | - | nein | OK |
| SZ-AAL/B1.179 | o:szd.3109 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.11.1941 | - | nein | OK |
| SZ-AAL/B1.18 | o:szd.3110 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 15.12.1939 | - | nein | OK |
| SZ-AAL/B1.180 | o:szd.3111 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 10.11.1941 | - | nein | OK |
| SZ-AAL/B1.181 | o:szd.3112 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 15.11.1941 | - | nein | OK |
| SZ-AAL/B1.182 | o:szd.3113 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 16.11.1941 | - | nein | OK |
| SZ-AAL/B1.183 | o:szd.3114 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 24.11.1941 | - | nein | OK |
| SZ-AAL/B1.184 | o:szd.3115 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 24.11.1941 | - | nein | OK |
| SZ-AAL/B1.185 | o:szd.3116 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 2.12.1941 | - | nein | OK |
| SZ-AAL/B1.186 | o:szd.3117 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.12.1941 | - | nein | OK |
| SZ-AAL/B1.187 | o:szd.3118 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 31.12.1941 | - | nein | OK |
| SZ-AAL/B1.188 | o:szd.3119 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 10.1.1942 | - | nein | OK |
| SZ-AAL/B1.189 | o:szd.3120 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 01.1942 | - | nein | OK |
| SZ-AAL/B1.19 | o:szd.3121 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 28.11.1939 | - | nein | OK |
| SZ-AAL/B1.190 | o:szd.3122 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 16.1.1942 | - | nein | OK |
| SZ-AAL/B1.191 | o:szd.3123 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 21.1.1942 | - | nein | OK |
| SZ-AAL/B1.192 | o:szd.3124 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 01.1942 | - | nein | OK |
| SZ-AAL/B1.193 | o:szd.3125 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 21.1.1942 | - | nein | OK |
| SZ-AAL/B1.194 | o:szd.3126 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 01.1942 | - | nein | OK |
| SZ-AAL/B1.195 | o:szd.3127 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 1.2.1942 | - | nein | OK |
| SZ-AAL/B1.196 | o:szd.3128 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 1.2.1942 | - | nein | OK |
| SZ-AAL/B1.197 | o:szd.3129 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.2.1942 | - | nein | OK |
| SZ-AAL/B1.198 | o:szd.3130 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 10.2.1942 | - | nein | OK |
| SZ-AAL/B1.199 | o:szd.3131 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 21.2.1942 | - | nein | OK |
| SZ-AAL/B1.2 | o:szd.3132 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 02.1939 | - | nein | OK |
| SZ-AAL/B1.20 | o:szd.3133 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 11.1939 | - | nein | OK |
| SZ-AAL/B1.200 | o:szd.3134 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 21.2.1942 | - | nein | OK |
| SZ-AAL/B1.21 | o:szd.3135 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 10.1939 | - | nein | OK |
| SZ-AAL/B1.22 | o:szd.3136 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 23.9.1939 | - | nein | OK |
| SZ-AAL/B1.23 | o:szd.3137 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 14.10.1939 | - | nein | OK |
| SZ-AAL/B1.24 | o:szd.3138 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 12.3.1940 | - | nein | OK |
| SZ-AAL/B1.25 | o:szd.3139 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 20.10.1939 | - | nein | OK |
| SZ-AAL/B1.26 | o:szd.3140 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 19.9.1939 | - | nein | OK |
| SZ-AAL/B1.27 | o:szd.3141 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 25.6.1940 | - | nein | OK |
| SZ-AAL/B1.28 | o:szd.3142 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 25.6.1940 | - | nein | OK |
| SZ-AAL/B1.29 | o:szd.3143 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 8.7.1940 | - | nein | OK |
| SZ-AAL/B1.3 | o:szd.3144 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 01.1939 | - | nein | OK |
| SZ-AAL/B1.30 | o:szd.3145 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 07.1940 | - | nein | OK |
| SZ-AAL/B1.31 | o:szd.3146 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 13.7.1940 | - | nein | OK |
| SZ-AAL/B1.32 | o:szd.3147 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 18.7.1940 | - | nein | OK |
| SZ-AAL/B1.33 | o:szd.3148 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 18.7.1940 | - | nein | OK |
| SZ-AAL/B1.34 | o:szd.3149 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 21.7.1940 | - | nein | OK |
| SZ-AAL/B1.35 | o:szd.3150 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Lotte | 25.7.1940 | - | nein | OK |
| SZ-AAL/B1.36 | o:szd.3151 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 27.7.1940 | - | nein | OK |
| SZ-AAL/B1.37 | o:szd.3152 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 28.7.1940 | - | nein | OK |
| SZ-AAL/B1.38 | o:szd.3153 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 07.1940 | - | nein | OK |
| SZ-AAL/B1.39 | o:szd.3154 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 07.1940 | - | nein | OK |
| SZ-AAL/B1.4 | o:szd.3155 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 11.9.1939 | - | nein | OK |
| SZ-AAL/B1.40 | o:szd.3156 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 4.8.1940 | - | nein | OK |
| SZ-AAL/B1.41 | o:szd.3157 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 14.8.1940 | - | nein | OK |
| SZ-AAL/B1.42 | o:szd.3158 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 1940 | - | nein | OK |
| SZ-AAL/B1.43 | o:szd.3159 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 08.1940 | - | nein | OK |
| SZ-AAL/B1.44 | o:szd.3160 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 23.8.1940 | - | nein | OK |
| SZ-AAL/B1.45 | o:szd.3161 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 23.8.1940 | - | nein | OK |
| SZ-AAL/B1.46 | o:szd.3162 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 6.9.1940 | - | nein | OK |
| SZ-AAL/B1.47 | o:szd.3163 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 10.9.1940 | - | nein | OK |
| SZ-AAL/B1.48 | o:szd.3164 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 15.9.1940 | - | nein | OK |
| SZ-AAL/B1.49 | o:szd.3165 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 15.9.1940 | - | nein | OK |
| SZ-AAL/B1.5 | o:szd.3166 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 1939 | - | nein | OK |
| SZ-AAL/B1.50 | o:szd.3167 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 09.1940 | - | nein | OK |
| SZ-AAL/B1.51 | o:szd.3168 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 22.9.1940 | - | nein | OK |
| SZ-AAL/B1.52 | o:szd.3169 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 29.9.1940 | - | nein | OK |
| SZ-AAL/B1.53 | o:szd.3170 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 6.10.1940 | - | nein | OK |
| SZ-AAL/B1.54 | o:szd.3171 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 10.10.1940 | - | nein | OK |
| SZ-AAL/B1.55 | o:szd.3172 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 16.10.1940 | - | nein | OK |
| SZ-AAL/B1.56 | o:szd.3173 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Lotte | 19.10.1940 | - | nein | OK |
| SZ-AAL/B1.57 | o:szd.3174 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 23.10.1940 | - | nein | OK |
| SZ-AAL/B1.58 | o:szd.3175 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 26.10.1940 | - | nein | OK |
| SZ-AAL/B1.59 | o:szd.3176 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 27.10.1940 | - | nein | OK |
| SZ-AAL/B1.6 | o:szd.3177 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 6.11.1939 | - | nein | OK |
| SZ-AAL/B1.60 | o:szd.3178 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 1.11.1940 | - | nein | OK |
| SZ-AAL/B1.61 | o:szd.3179 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 9.11.1940 | - | nein | OK |
| SZ-AAL/B1.62 | o:szd.3180 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 12.11.1940 | - | nein | OK |
| SZ-AAL/B1.63 | o:szd.3181 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 15.11.1940 | - | nein | OK |
| SZ-AAL/B1.64 | o:szd.3182 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 19.11.1940 | - | nein | OK |
| SZ-AAL/B1.65 | o:szd.3183 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 22.11.1940 | - | nein | OK |
| SZ-AAL/B1.66 | o:szd.3184 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 27.11.1940 | - | nein | OK |
| SZ-AAL/B1.67 | o:szd.3185 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 3.12.1940 | - | nein | OK |
| SZ-AAL/B1.68 | o:szd.3186 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 12.1940 | - | nein | OK |
| SZ-AAL/B1.69 | o:szd.3187 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 7.12.1940 | - | nein | OK |
| SZ-AAL/B1.7 | o:szd.3188 | 3 | 3 | 3 | 3 | OK | OK | Brief | Altmann, Eva | 2.12.1939 | - | nein | OK |
| SZ-AAL/B1.70 | o:szd.3189 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 11.12.1940 | - | nein | OK |
| SZ-AAL/B1.71 | o:szd.3190 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 11.12.1940 | - | nein | OK |
| SZ-AAL/B1.73 | o:szd.3191 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 11.12.1940 | - | nein | OK |
| SZ-AAL/B1.74 | o:szd.3192 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 15.12.1940 | - | nein | OK |
| SZ-AAL/B1.75 | o:szd.3193 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 16.12.1940 | - | nein | OK |
| SZ-AAL/B1.76 | o:szd.3194 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 18.12.1940 | - | nein | OK |
| SZ-AAL/B1.77 | o:szd.3195 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Lotte | 27.12.1940 | - | nein | OK |
| SZ-AAL/B1.77a | o:szd.3196 | 2 | 2 | 2 | 2 | OK | OK | Brief | Zweig, Stefan | 1940 | - | nein | OK |
| SZ-AAL/B1.78 | o:szd.3197 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 31.12.1940 | - | nein | OK |
| SZ-AAL/B1.79 | o:szd.3198 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 01.1941 | - | nein | OK |
| SZ-AAL/B1.8 | o:szd.3199 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 8.12.1939 | - | nein | OK |
| SZ-AAL/B1.80 | o:szd.3200 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 01.1941 | - | nein | OK |
| SZ-AAL/B1.81 | o:szd.3201 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Lotte | 11.1.1941 | - | nein | OK |
| SZ-AAL/B1.82 | o:szd.3202 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Lotte | 12.1.1941 | - | nein | OK |
| SZ-AAL/B1.83 | o:szd.3203 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 12.1.1941 | - | nein | OK |
| SZ-AAL/B1.84 | o:szd.3204 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 16.1.1941 | - | nein | OK |
| SZ-AAL/B1.85 | o:szd.3205 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 22.1.1941 | - | nein | OK |
| SZ-AAL/B1.86 | o:szd.3206 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 22.1.1941 | - | nein | OK |
| SZ-AAL/B1.87 | o:szd.3207 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 01.1941 | - | nein | OK |
| SZ-AAL/B1.88 | o:szd.3208 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Lotte | 25.1.1941 | - | nein | OK |
| SZ-AAL/B1.89 | o:szd.3209 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 27.1.1941 | - | nein | OK |
| SZ-AAL/B1.9 | o:szd.3210 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 19.12.1939 | - | nein | OK |
| SZ-AAL/B1.90 | o:szd.3211 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 27.1.1941 | - | nein | OK |
| SZ-AAL/B1.91 | o:szd.3212 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Lotte | 29.1.1941 | - | nein | OK |
| SZ-AAL/B1.92 | o:szd.3213 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 30.1.1941 | - | nein | OK |
| SZ-AAL/B1.93 | o:szd.3214 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 31.1.1941 | - | nein | OK |
| SZ-AAL/B1.94 | o:szd.3215 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 01.1941 | - | nein | OK |
| SZ-AAL/B1.95 | o:szd.3216 | 5 | 5 | 5 | 5 | OK | OK | Brief | Altmann, Eva | 1.2.1941 | - | nein | OK |
| SZ-AAL/B1.96 | o:szd.3217 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 4.2.1941 | - | nein | OK |
| SZ-AAL/B1.97 | o:szd.3218 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 02.1941 | - | nein | OK |
| SZ-AAL/B1.98 | o:szd.3219 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Lotte | 10.2.1941 | - | nein | OK |
| SZ-AAL/B1.99 | o:szd.3220 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Lotte | 13.2.1941 | - | nein | OK |
| SZ-AAL/B10.1 | o:szd.3221 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Alfred | 10.9.1937 | - | nein | OK |
| SZ-AAL/B10.2 | o:szd.3222 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Alfred | 11.9.1937 | - | nein | OK |
| SZ-AAL/B10.3 | o:szd.3223 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Alfred | 14.9.1937 | - | nein | OK |
| SZ-AAL/B10.4 | o:szd.3224 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Alfred | 1.9.1938 | - | nein | OK |
| SZ-AAL/B10.5 | o:szd.3225 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Alfred | 8.9.1938 | - | nein | OK |
| SZ-AAL/B10.6 | o:szd.3226 | 15 | 15 | 15 | 15 | OK | OK | Brieffragment | Zweig, Alfred | 7.10.1938 | - | nein | OK |
| SZ-AAL/B10.7 | o:szd.3227 | 3 | 3 | 3 | 3 | OK | OK | Brief | Birman, C. | 17.11.1938 | - | nein | OK |
| SZ-AAL/B10.8 | o:szd.3228 | 3 | 3 | 3 | 3 | OK | OK | Brief | Süssland, Ernst | 21.11.1938 | - | nein | OK |
| SZ-AAL/B10.9 | o:szd.3229 | 3 | 3 | 3 | 3 | OK | OK | Briefabschriften | Trading | 21.11.1938 | - | nein | Autor unueblich: 'Trading' |
| SZ-AAL/B11 | o:szd.3230 | 3 | 3 | 3 | 3 | OK | OK | Brief | Wolfenstein, Alfred | 3.12.1937 | - | nein | OK |
| SZ-AAL/B12 | o:szd.3231 | 7 | 7 | 7 | 7 | OK | OK | Brief | Beierle, Alfred | - | - | nein | Datum leer |
| SZ-AAL/B13 | o:szd.3232 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zarek, Otto | 30.9.1938 | - | nein | OK |
| SZ-AAL/B14 | o:szd.3233 | 5 | 5 | 5 | 5 | OK | OK | Brief | Frenkel, Lotte | 7.11.1935 | - | nein | OK |
| SZ-AAL/B15 | o:szd.3234 | 5 | 5 | 5 | 5 | OK | OK | Brief | Kiefer, Oskar Alexander | 2.10.1937 | - | nein | OK |
| SZ-AAL/B16 | o:szd.3235 | 5 | 5 | 5 | 5 | OK | OK | Brief | Chaine, René | 4.3.1938 | - | nein | OK |
| SZ-AAL/B17 | o:szd.3236 | 5 | 5 | 5 | 5 | OK | OK | Brief | Rieger, Erwin | 12.9.1937 | - | nein | OK |
| SZ-AAL/B18 | o:szd.3237 | 3 | 3 | 3 | 3 | OK | OK | Telegramm | Monath, Paul | 19.9.1939 | - | nein | OK |
| SZ-AAL/B19 | o:szd.3238 | 3 | 3 | 3 | 3 | OK | OK | Brief | Sambat, M. | - | - | nein | Datum leer |
| SZ-AAL/B2.1 | o:szd.3239 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 1.5.1934 | - | nein | OK |
| SZ-AAL/B2.10 | o:szd.3240 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 20.8.1934 | - | nein | OK |
| SZ-AAL/B2.11 | o:szd.3241 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 23.8.1934 | - | nein | OK |
| SZ-AAL/B2.12 | o:szd.3242 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 29.8.1934 | - | nein | OK |
| SZ-AAL/B2.13 | o:szd.3243 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 4.9.1934 | - | nein | OK |
| SZ-AAL/B2.14 | o:szd.3244 | 6 | 6 | 6 | 6 | OK | OK | Brief | Zweig, Stefan | 6.9.1934 | - | nein | OK |
| SZ-AAL/B2.15 | o:szd.3245 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 9.9.1934 | - | nein | OK |
| SZ-AAL/B2.16 | o:szd.3246 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 10.9.1934 | - | nein | OK |
| SZ-AAL/B2.17 | o:szd.3247 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 6.1.1935 | - | nein | OK |
| SZ-AAL/B2.18 | o:szd.3248 | 9 | 9 | 9 | 9 | OK | OK | Brief | Zweig, Stefan | 10.1.1935 | - | nein | OK |
| SZ-AAL/B2.19 | o:szd.3249 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 17.1.1935 | - | nein | OK |
| SZ-AAL/B2.2 | o:szd.3250 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 9.5.1934 | - | nein | OK |
| SZ-AAL/B2.20 | o:szd.3251 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 20.1.1935 | - | nein | OK |
| SZ-AAL/B2.21 | o:szd.3252 | 3 | 3 | 3 | 3 | OK | OK | Ansichtspostkarte | Zweig, Stefan | 24.1.1935 | - | nein | OK |
| SZ-AAL/B2.22 | o:szd.3253 | 3 | 3 | 3 | 3 | OK | OK | Kuvert | Zweig, Stefan | 19.2.1935 | - | nein | OK |
| SZ-AAL/B2.23 | o:szd.3254 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 02.1935 | - | nein | OK |
| SZ-AAL/B2.24 | o:szd.3255 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 4.3.1935 | - | nein | OK |
| SZ-AAL/B2.25 | o:szd.3256 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 23.3.1935 | - | nein | OK |
| SZ-AAL/B2.26 | o:szd.3257 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 2.4.1935 | - | nein | OK |
| SZ-AAL/B2.27 | o:szd.3258 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 04.1935 | - | nein | OK |
| SZ-AAL/B2.28 | o:szd.3259 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 10.4.1935 | - | nein | OK |
| SZ-AAL/B2.29 | o:szd.3260 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 14.4.1935 | - | nein | OK |
| SZ-AAL/B2.3 | o:szd.3261 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 30.7.1934 | - | nein | OK |
| SZ-AAL/B2.30 | o:szd.3262 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 04.1935 | - | nein | OK |
| SZ-AAL/B2.31 | o:szd.3263 | 3 | 3 | 3 | 3 | OK | OK | Ansichtspostkarte | Zweig, Stefan | 22.4.1935 | - | nein | OK |
| SZ-AAL/B2.32 | o:szd.3264 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 29.4.1935 | - | nein | OK |
| SZ-AAL/B2.33 | o:szd.3265 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 9.5.1935 | - | nein | OK |
| SZ-AAL/B2.34 | o:szd.3266 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 19.5.1935 | - | nein | OK |
| SZ-AAL/B2.35 | o:szd.3267 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 31.5.1935 | - | nein | OK |
| SZ-AAL/B2.36 | o:szd.3268 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 6.6.1935 | - | nein | OK |
| SZ-AAL/B2.37 | o:szd.3269 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 12.6.1935 | - | nein | OK |
| SZ-AAL/B2.38 | o:szd.3270 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 13.6.1935 | - | nein | OK |
| SZ-AAL/B2.39 | o:szd.3271 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 14.6.1935 | - | nein | OK |
| SZ-AAL/B2.4 | o:szd.3272 | 13 | 13 | 13 | 13 | OK | OK | Brief | Zweig, Stefan | 5.8.1934 | - | nein | OK |
| SZ-AAL/B2.40 | o:szd.3273 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 16.6.1935 | - | nein | OK |
| SZ-AAL/B2.41 | o:szd.3274 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 30.7.1935 | - | nein | OK |
| SZ-AAL/B2.42 | o:szd.3275 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 4.8.1935 | - | nein | OK |
| SZ-AAL/B2.43 | o:szd.3276 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 9.8.1935 | - | nein | OK |
| SZ-AAL/B2.44 | o:szd.3277 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 20.8.1935 | - | nein | OK |
| SZ-AAL/B2.45 | o:szd.3278 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 25.8.1935 | - | nein | OK |
| SZ-AAL/B2.46 | o:szd.3279 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 09-4.1935 | - | nein | OK |
| SZ-AAL/B2.47 | o:szd.3280 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 8.9.1935 | - | nein | OK |
| SZ-AAL/B2.48 | o:szd.3281 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 12.9.1935 | - | nein | OK |
| SZ-AAL/B2.49 | o:szd.3282 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 14.9.1935 | - | nein | OK |
| SZ-AAL/B2.5 | o:szd.3283 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 6.8.1934 | - | nein | OK |
| SZ-AAL/B2.50 | o:szd.3284 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 19.9.1935 | - | nein | OK |
| SZ-AAL/B2.51 | o:szd.3285 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 23.9.1935 | - | nein | OK |
| SZ-AAL/B2.52 | o:szd.3286 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 2.12.1935 | - | nein | OK |
| SZ-AAL/B2.53 | o:szd.3287 | 3 | 3 | 3 | 3 | OK | OK | Ansichtspostkarte | Zweig, Stefan | 4.12.1935 | - | nein | OK |
| SZ-AAL/B2.54 | o:szd.3288 | 6 | 6 | 6 | 6 | OK | OK | Brief | Zweig, Stefan | 15.12.1935 | - | nein | OK |
| SZ-AAL/B2.55 | o:szd.3289 | 3 | 3 | 3 | 3 | OK | OK | Kuvert | Zweig, Stefan | 20.12.1935 | - | nein | OK |
| SZ-AAL/B2.56 | o:szd.3290 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 21.12.1935 | - | nein | OK |
| SZ-AAL/B2.57 | o:szd.3291 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 23.12.1935 | - | nein | OK |
| SZ-AAL/B2.58 | o:szd.3292 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 24.12.1935 | - | nein | OK |
| SZ-AAL/B2.59 | o:szd.3293 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 20.6.1936 | - | nein | OK |
| SZ-AAL/B2.6 | o:szd.3294 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 8.8.1934 | - | nein | OK |
| SZ-AAL/B2.60 | o:szd.3295 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 21.6.1936 | - | nein | OK |
| SZ-AAL/B2.61 | o:szd.3296 | 3 | 3 | 3 | 3 | OK | OK | Kuvert | Zweig, Stefan | 21.6.1936 | - | nein | OK |
| SZ-AAL/B2.62 | o:szd.3297 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 22.6.1936 | - | nein | OK |
| SZ-AAL/B2.63 | o:szd.3298 | 8 | 8 | 8 | 8 | OK | OK | Brief | Zweig, Stefan | 24.6.1936 | - | nein | OK |
| SZ-AAL/B2.64 | o:szd.3299 | 4 | 4 | 4 | 4 | OK | OK | Brief | Zweig, Stefan | 29.6.1936 | - | nein | OK |
| SZ-AAL/B2.65 | o:szd.3300 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 3.7.1936 | - | nein | OK |
| SZ-AAL/B2.66 | o:szd.3301 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 8.8.1936 | - | nein | OK |
| SZ-AAL/B2.67 | o:szd.3302 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 10.8.1936 | - | nein | OK |
| SZ-AAL/B2.68 | o:szd.3303 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 21.8.1936 | - | nein | OK |
| SZ-AAL/B2.69 | o:szd.3304 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 26.8.1936 | - | nein | OK |
| SZ-AAL/B2.7 | o:szd.3305 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 11.8.1934 | - | nein | OK |
| SZ-AAL/B2.70 | o:szd.3306 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 3.9.1936 | - | nein | OK |
| SZ-AAL/B2.71 | o:szd.3307 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 12.9.1936 | - | nein | OK |
| SZ-AAL/B2.72 | o:szd.3308 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 17.9.1936 | - | nein | OK |
| SZ-AAL/B2.73 | o:szd.3309 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 20.12.1936 | - | nein | OK |
| SZ-AAL/B2.74 | o:szd.3310 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 7.5.1937 | - | nein | OK |
| SZ-AAL/B2.75 | o:szd.3311 | 3 | 3 | 3 | 3 | OK | OK | Ansichtspostkarte | Zweig, Stefan | 8.5.1937 | - | nein | OK |
| SZ-AAL/B2.76 | o:szd.3312 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 11.5.1937 | - | nein | OK |
| SZ-AAL/B2.77 | o:szd.3313 | 4 | 4 | 4 | 4 | OK | OK | Brief | Zweig, Stefan | 12.5.1937 | - | nein | OK |
| SZ-AAL/B2.78 | o:szd.3314 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Stefan | 14.5.1937 | - | nein | OK |
| SZ-AAL/B2.79 | o:szd.3315 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 19.8.1937 | - | nein | OK |
| SZ-AAL/B2.8 | o:szd.3316 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 13.8.1934 | - | nein | OK |
| SZ-AAL/B2.80 | o:szd.3317 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 21.8.1937 | - | nein | OK |
| SZ-AAL/B2.81 | o:szd.3318 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 23.8.1937 | - | nein | OK |
| SZ-AAL/B2.82 | o:szd.3319 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 25.8.1937 | - | nein | OK |
| SZ-AAL/B2.83 | o:szd.3320 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 27.8.1937 | - | nein | OK |
| SZ-AAL/B2.84 | o:szd.3321 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 30.8.1937 | - | nein | OK |
| SZ-AAL/B2.85 | o:szd.3322 | 3 | 3 | 3 | 3 | OK | OK | Ansichtspostkarte | Zweig, Stefan | 26.11.1937 | - | nein | OK |
| SZ-AAL/B2.86 | o:szd.3323 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Zweig, Stefan | 8.11.1938 | - | nein | OK |
| SZ-AAL/B2.87 | o:szd.3324 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 9.11.1938 | - | nein | OK |
| SZ-AAL/B2.88 | o:szd.3325 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 10.4.1940 | - | nein | OK |
| SZ-AAL/B2.89 | o:szd.3326 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 11.4.1940 | - | nein | OK |
| SZ-AAL/B2.9 | o:szd.3327 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 14.8.1934 | - | nein | OK |
| SZ-AAL/B2.90 | o:szd.3328 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 13.4.1940 | - | nein | OK |
| SZ-AAL/B2.91 | o:szd.3329 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 13.4.1940 | - | nein | OK |
| SZ-AAL/B2.92 | o:szd.3330 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 16.4.1940 | - | nein | OK |
| SZ-AAL/B2.93 | o:szd.3331 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 19.4.1940 | - | nein | OK |
| SZ-AAL/B2.94 | o:szd.3332 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 19.4.1940 | - | nein | OK |
| SZ-AAL/B2.95 | o:szd.3333 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 21.4.1940 | - | nein | OK |
| SZ-AAL/B2.96 | o:szd.3334 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 22.4.1940 | - | nein | OK |
| SZ-AAL/B2.97 | o:szd.3335 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Stefan | 24.4.1940 | - | nein | OK |
| SZ-AAL/B20 | o:szd.3336 | 5 | 5 | 5 | 5 | OK | OK | Brief | Garcés, Mario | 21.7.1937 | - | nein | OK |
| SZ-AAL/B21 | o:szd.3337 | 3 | 3 | 3 | 3 | OK | OK | Brief | Singer, Emmerich | 20.10.1938 | - | nein | OK |
| SZ-AAL/B3.1 | o:szd.3338 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.10 | o:szd.3339 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | 18.5.1936 | - | nein | OK |
| SZ-AAL/B3.100 | o:szd.3340 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Friderike | 20.9.1937 | - | nein | OK |
| SZ-AAL/B3.101 | o:szd.3341 | 3 | 3 | 3 | 3 | OK | OK | Kuvert | Zweig, Friderike | 23.9.1937 | - | nein | OK |
| SZ-AAL/B3.102 | o:szd.3342 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Friderike | 24.9.1937 | - | nein | OK |
| SZ-AAL/B3.103 | o:szd.3343 | 7 | 7 | 7 | 7 | OK | OK | Brief | Meiler, Friedrich | 24.9.1937 | - | nein | OK |
| SZ-AAL/B3.104 | o:szd.3344 | 3 | 3 | 3 | 3 | OK | OK | Brief | Meiler, Friedrich | 28.9.1937 | - | nein | OK |
| SZ-AAL/B3.105 | o:szd.3345 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Friderike | 28.9.1937 | - | nein | OK |
| SZ-AAL/B3.106 | o:szd.3346 | 5 | 5 | 5 | 5 | OK | OK | Brief | Meiler, Friedrich | 30.9.1937 | - | nein | OK |
| SZ-AAL/B3.109 | o:szd.3347 | 7 | 7 | 7 | 7 | OK | OK | Briefentwurf | Zweig, Stefan | 29.7.1937 | - | nein | OK |
| SZ-AAL/B3.11 | o:szd.3348 | 3 | 3 | 3 | 3 | OK | OK | Telegramm | Zweig, Friderike | 1.7.1936 | - | nein | OK |
| SZ-AAL/B3.110 | o:szd.3349 | 3 | 3 | 3 | 3 | OK | OK | Entwurf | Zweig, Stefan | - | - | nein | Datum leer |
| SZ-AAL/B3.111 | o:szd.3350 | 5 | 5 | 5 | 5 | OK | OK | Entwurf | Zweig, Stefan | - | - | nein | Datum leer |
| SZ-AAL/B3.112 | o:szd.3351 | 9 | 9 | 9 | 9 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.113 | o:szd.3352 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.114 | o:szd.3353 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.115 | o:szd.3354 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.116 | o:szd.3355 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.117 | o:szd.3356 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.118 | o:szd.3357 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.119 | o:szd.3358 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.12 | o:szd.3359 | 7 | 7 | 7 | 7 | OK | OK | Brief | Zweig, Friderike | 20.7.1936 | - | nein | OK |
| SZ-AAL/B3.120 | o:szd.3360 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.121 | o:szd.3361 | 11 | 11 | 11 | 11 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.122 | o:szd.3362 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.123 | o:szd.3363 | 9 | 9 | 9 | 9 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.124 | o:szd.3364 | 9 | 9 | 9 | 9 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.125 | o:szd.3365 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.126 | o:szd.3366 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.127 | o:szd.3367 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.128 | o:szd.3368 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.130 | o:szd.3369 | 3 | 3 | 3 | 3 | OK | OK | Brieffragment | Zweig, Friderike | - | - | nein | Datum leer |
| SZ-AAL/B3.132 | o:szd.3370 | 3 | 3 | 3 | 3 | OK | OK | Brief | Haupolter, Walter | 25.8.1938 | - | nein | OK |
| SZ-AAL/B3.133 | o:szd.3371 | 3 | 3 | 3 | 3 | OK | OK | Brief | Haupolter, Walter | 16.9.1938 | - | nein | OK |
| SZ-AAL/B3.134 | o:szd.3372 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Stefan | 19.9.1938 | - | nein | OK |
| SZ-AAL/B3.135 | o:szd.3373 | 3 | 3 | 3 | 3 | OK | OK | Brief | Hofmannsthal, Emil von | 28.9.1938 | - | nein | OK |
| SZ-AAL/B3.136 | o:szd.3374 | 3 | 3 | 3 | 3 | OK | OK | Brief | Haupolter, Walter | 23.11.1938 | - | nein | OK |
| SZ-AAL/B3.137 | o:szd.3375 | 15 | 15 | 15 | 15 | OK | OK | Brief | Haupolter, Walter | 2.12.1938 | - | nein | OK |
| SZ-AAL/B3.138 | o:szd.3376 | 3 | 3 | 3 | 3 | OK | OK | Brief | Unidentified | 7.12.1938 | - | nein | Autor unueblich: 'Unidentified' |
| SZ-AAL/B3.139 | o:szd.3377 | 3 | 3 | 3 | 3 | OK | OK | Brief | Zweig, Friderike | 8.12.1938 | - | nein | OK |
| SZ-AAL/B3.14 | o:szd.3378 | 5 | 5 | 5 | 5 | OK | OK | Brief | Zweig, Friderike | 17.11.1936 | - | nein | OK |
| SZ-AAL/B4.1 | o:szd.3379 | 7 | 7 | 7 | 7 | OK | OK | Brief | Maass, Joachim | 24.1.1936 | - | nein | OK |
| SZ-AAL/B4.2 | o:szd.3380 | 7 | 7 | 7 | 7 | OK | OK | Brief | Maass, Joachim | 7.1.1936 | - | nein | OK |
| SZ-AAL/B4.3 | o:szd.3381 | 5 | 5 | 5 | 5 | OK | OK | Brief | Maass, Joachim | 2.4.1936 | - | nein | OK |
| SZ-AAL/B4.4 | o:szd.3382 | 5 | 5 | 5 | 5 | OK | OK | Brief | Maass, Joachim | 30.5.1936 | - | nein | OK |
| SZ-AAL/B4.5 | o:szd.3383 | 5 | 5 | 5 | 5 | OK | OK | Brief | Maass, Joachim | 10.10.1936 | - | nein | OK |
| SZ-AAL/B4.6 | o:szd.3384 | 3 | 3 | 3 | 3 | OK | OK | Brief | Maass, Joachim | 7.4.1938 | - | nein | OK |
| SZ-AAL/B4.7 | o:szd.3385 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Maass, Joachim | 25.5.1938 | - | nein | OK |
| SZ-AAL/B4.8 | o:szd.3386 | 3 | 3 | 3 | 3 | OK | OK | Brief | Maass, Joachim | 12.6.1938 | - | nein | OK |
| SZ-AAL/B4.9 | o:szd.3387 | 3 | 3 | 3 | 3 | OK | OK | Postkarte | Maass, Joachim | 27.7.1938 | - | nein | OK |
| SZ-AAL/B5.1 | o:szd.3388 | 3 | 3 | 3 | 3 | OK | OK | Brief | Walter, Rose | 3.9.1935 | - | nein | OK |
| SZ-AAL/B5.2 | o:szd.3389 | 5 | 5 | 5 | 5 | OK | OK | Brief | Walter, Rose | 19.9.1935 | - | nein | OK |
| SZ-AAL/B6 | o:szd.3390 | 3 | 3 | 3 | 3 | OK | OK | Ansichtspostkarte | Zweig, Friderike | 06.1934 | - | nein | OK |
| SZ-AAL/B7.1 | o:szd.3391 | 5 | 5 | 5 | 5 | OK | OK | Brief | Kaufmann, Charlotte | 3.2.1936 | - | nein | OK |
| SZ-AAL/B7.2 | o:szd.3392 | 5 | 5 | 5 | 5 | OK | OK | Brief | Kaufmann, Charlotte | 20.3.1936 | - | nein | OK |
| SZ-AAL/B8.1 | o:szd.3393 | 5 | 5 | 5 | 5 | OK | OK | Brief | Bauer, Walter | 13.8.1935 | - | nein | OK |
| SZ-AAL/B8.2 | o:szd.3394 | 5 | 5 | 5 | 5 | OK | OK | Brief | Bauer, Walter | 10.1.1936 | - | nein | OK |
| SZ-AAL/B9.1 | o:szd.3395 | 5 | 5 | 5 | 5 | OK | OK | Brief | Roth, Joseph | 27.2.1935 | - | nein | OK |
| SZ-AAL/B9.2 | o:szd.3396 | 3 | 3 | 3 | 3 | OK | OK | Brief | Roth, Joseph | 8.8.1936 | - | nein | OK |
| SZ-AAL/B9.3 | o:szd.3397 | 3 | 3 | 3 | 3 | OK | OK | Brief | Roth, Joseph | 13.8.1936 | - | nein | OK |
| SZ-AAL/B9.4 | o:szd.3398 | 3 | 3 | 3 | 3 | OK | OK | Ansichtspostkarte | Roth, Joseph | 6.6.1937 | - | nein | OK |
