# Aplicatia mobila Android

---

## Coduri de request bluetooth

Aplicatia va trimite prin bluetooth urmatoarele coduri:

1. Deschidere bariera - 0x1001
2. Cerere date personale - 0x1002
3. Cerere lista pontaj - 0x1003

Acestea vor fi urmate de codul PUK (15 octeti).
Exemplu de mesaj trimis:
`0x1001012345678901234` - deschidere bariera, PUK 012345678901234