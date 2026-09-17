
/* WARNING: Removing unreachable block (ram,0x00452bef) */
/* WARNING: Removing unreachable block (ram,0x00452b81) */
/* WARNING: Removing unreachable block (ram,0x00452b13) */
/* WARNING: Removing unreachable block (ram,0x00452aa7) */
/* WARNING: Removing unreachable block (ram,0x00452981) */
/* WARNING: Removing unreachable block (ram,0x00452925) */
/* WARNING: Removing unreachable block (ram,0x004528d0) */
/* WARNING: Removing unreachable block (ram,0x00452878) */
/* WARNING: Removing unreachable block (ram,0x004527fb) */
/* WARNING: Removing unreachable block (ram,0x004527a0) */
/* WARNING: Removing unreachable block (ram,0x00452746) */
/* WARNING: Removing unreachable block (ram,0x004526e2) */
/* WARNING: Removing unreachable block (ram,0x00452686) */
/* WARNING: Removing unreachable block (ram,0x0045262c) */
/* WARNING: Removing unreachable block (ram,0x004525d0) */
/* WARNING: Removing unreachable block (ram,0x00452575) */
/* WARNING: Removing unreachable block (ram,0x00452379) */
/* WARNING: Removing unreachable block (ram,0x00452326) */
/* WARNING: Removing unreachable block (ram,0x00452188) */
/* WARNING: Removing unreachable block (ram,0x00452159) */
/* WARNING: Removing unreachable block (ram,0x004522f5) */
/* WARNING: Removing unreachable block (ram,0x0045234f) */
/* WARNING: Removing unreachable block (ram,0x004523ab) */
/* WARNING: Removing unreachable block (ram,0x0045259f) */
/* WARNING: Removing unreachable block (ram,0x004525fa) */
/* WARNING: Removing unreachable block (ram,0x0045265d) */
/* WARNING: Removing unreachable block (ram,0x004526b0) */
/* WARNING: Removing unreachable block (ram,0x00452714) */
/* WARNING: Removing unreachable block (ram,0x00452777) */
/* WARNING: Removing unreachable block (ram,0x004527ca) */
/* WARNING: Removing unreachable block (ram,0x00452824) */
/* WARNING: Removing unreachable block (ram,0x004528a4) */
/* WARNING: Removing unreachable block (ram,0x004528f9) */
/* WARNING: Removing unreachable block (ram,0x0045294f) */
/* WARNING: Removing unreachable block (ram,0x00452a6b) */
/* WARNING: Removing unreachable block (ram,0x00452adc) */
/* WARNING: Removing unreachable block (ram,0x00452b4a) */
/* WARNING: Removing unreachable block (ram,0x00452bb8) */
/* WARNING: Removing unreachable block (ram,0x00452c80) */
/* WARNING: Removing unreachable block (ram,0x00452bd6) */
/* WARNING: Removing unreachable block (ram,0x00452b68) */
/* WARNING: Removing unreachable block (ram,0x00452afa) */
/* WARNING: Removing unreachable block (ram,0x00452912) */
/* WARNING: Removing unreachable block (ram,0x00452891) */
/* WARNING: Removing unreachable block (ram,0x00452616) */
/* WARNING: Removing unreachable block (ram,0x00452395) */
/* WARNING: Removing unreachable block (ram,0x004523c7) */
/* WARNING: Removing unreachable block (ram,0x00452648) */
/* WARNING: Removing unreachable block (ram,0x004528bd) */
/* WARNING: Removing unreachable block (ram,0x00452a8c) */
/* WARNING: Removing unreachable block (ram,0x00452b31) */
/* WARNING: Removing unreachable block (ram,0x00452b9f) */
/* WARNING: Removing unreachable block (ram,0x00452c0d) */

void FUN__text__00452130(ushort *param_1)

{
  int iVar1;
  undefined4 *puVar2;
  undefined4 local_48 [17];
  
  puVar2 = local_48;
  for (iVar1 = 0x11; iVar1 != 0; iVar1 = iVar1 + -1) {
    *puVar2 = 0xcccccccc;
    puVar2 = puVar2 + 1;
  }
  if (0x3ff < *param_1) {
    *param_1 = 0x3ff;
  }
  if (0x3ff < param_1[1]) {
    param_1[1] = 0x3ff;
  }
  if ((char)param_1[2] == '\0') {
    *(undefined1 *)(param_1 + 2) = 1;
  }
  else if (0x87 < (byte)param_1[2]) {
    *(undefined1 *)(param_1 + 2) = 0x87;
  }
  if (*(char *)((int)param_1 + 5) == '\0') {
    *(undefined1 *)((int)param_1 + 5) = 1;
  }
  else if (0x87 < *(byte *)((int)param_1 + 5)) {
    *(undefined1 *)((int)param_1 + 5) = 0x87;
  }
  if ((char)param_1[3] == '\0') {
    *(undefined1 *)(param_1 + 3) = 1;
  }
  else if (0x87 < (byte)param_1[3]) {
    *(undefined1 *)(param_1 + 3) = 0x87;
  }
  if (*(char *)((int)param_1 + 7) == '\0') {
    *(undefined1 *)((int)param_1 + 7) = 1;
  }
  else if (0x87 < *(byte *)((int)param_1 + 7)) {
    *(undefined1 *)((int)param_1 + 7) = 0x87;
  }
  if ((char)param_1[4] == '\0') {
    *(undefined1 *)(param_1 + 4) = 1;
  }
  else if (0x87 < (byte)param_1[4]) {
    *(undefined1 *)(param_1 + 4) = 0x87;
  }
  if (*(char *)((int)param_1 + 9) == '\0') {
    *(undefined1 *)((int)param_1 + 9) = 1;
  }
  else if (0x87 < *(byte *)((int)param_1 + 9)) {
    *(undefined1 *)((int)param_1 + 9) = 0x87;
  }
  if ((char)param_1[5] == '\0') {
    *(undefined1 *)(param_1 + 5) = 1;
  }
  else if (0x87 < (byte)param_1[5]) {
    *(undefined1 *)(param_1 + 5) = 0x87;
  }
  if (0x3ff < param_1[6]) {
    param_1[6] = 0x3ff;
  }
  if (0x32 < (byte)param_1[7]) {
    *(undefined1 *)(param_1 + 7) = 0x32;
  }
  if (5 < *(byte *)((int)param_1 + 0xf)) {
    *(undefined1 *)((int)param_1 + 0xf) = 5;
  }
  if ((short)param_1[10] < 1) {
    param_1[10] = 1;
  }
  else if (999 < (short)param_1[10]) {
    param_1[10] = 999;
  }
  if ((short)param_1[0xb] < 0) {
    param_1[0xb] = 0;
  }
  else if (999 < (short)param_1[0xb]) {
    param_1[0xb] = 999;
  }
  if ((short)param_1[0xc] < 1) {
    param_1[0xc] = 1;
  }
  else if (999 < (short)param_1[0xc]) {
    param_1[0xc] = 999;
  }
  if ((short)param_1[0xd] < 1) {
    param_1[0xd] = 1;
  }
  else if (999 < (short)param_1[0xd]) {
    param_1[0xd] = 999;
  }
  if ((short)param_1[0xe] < 0) {
    param_1[0xe] = 0;
  }
  else if (999 < (short)param_1[0xe]) {
    param_1[0xe] = 999;
  }
  if ((short)param_1[0xf] < 1) {
    param_1[0xf] = 1;
  }
  else if (999 < (short)param_1[0xf]) {
    param_1[0xf] = 999;
  }
  if (*(int *)(param_1 + 0x10) < 0) {
    param_1[0x10] = 0;
    param_1[0x11] = 0;
  }
  else if (0x7fffffff < *(int *)(param_1 + 0x10)) {
    param_1[0x10] = 0xffff;
    param_1[0x11] = 0x7fff;
  }
  if (*(int *)(param_1 + 0x12) < 0) {
    param_1[0x12] = 0;
    param_1[0x13] = 0;
  }
  else if (0x7fffffff < *(int *)(param_1 + 0x12)) {
    param_1[0x12] = 0xffff;
    param_1[0x13] = 0x7fff;
  }
  if (*(int *)(param_1 + 0x14) < 0) {
    param_1[0x14] = 0;
    param_1[0x15] = 0;
  }
  else if (0x7fffffff < *(int *)(param_1 + 0x14)) {
    param_1[0x14] = 0xffff;
    param_1[0x15] = 0x7fff;
  }
  if (0x20 < (byte)param_1[0x16]) {
    *(undefined1 *)(param_1 + 0x16) = 0x20;
  }
  if (999 < param_1[0x17]) {
    param_1[0x17] = 999;
  }
  if (3 < (byte)param_1[0x18]) {
    *(undefined1 *)(param_1 + 0x18) = 3;
  }
  if (0x7f < (byte)param_1[0x1b]) {
    *(undefined1 *)(param_1 + 0x1b) = 0x7f;
  }
  if (0x20 < *(byte *)((int)param_1 + 0x37)) {
    *(undefined1 *)((int)param_1 + 0x37) = 0x20;
  }
  if (999 < param_1[0x1c]) {
    param_1[0x1c] = 999;
  }
  if (999 < param_1[0x1d]) {
    param_1[0x1d] = 999;
  }
  if (999 < param_1[0x1e]) {
    param_1[0x1e] = 999;
  }
  if (999 < param_1[0x1f]) {
    param_1[0x1f] = 999;
  }
  if (7 < (byte)param_1[0x20]) {
    *(undefined1 *)(param_1 + 0x20) = 7;
  }
  if (100 < *(byte *)((int)param_1 + 0x41)) {
    *(undefined1 *)((int)param_1 + 0x41) = 100;
  }
  if (999 < param_1[0x21]) {
    param_1[0x21] = 999;
  }
  if (0x7f < (byte)param_1[0x22]) {
    *(undefined1 *)(param_1 + 0x22) = 0x7f;
  }
  if (0x7f < *(byte *)((int)param_1 + 0x45)) {
    *(undefined1 *)((int)param_1 + 0x45) = 0x7f;
  }
  if (*(int *)(param_1 + 0x24) < 0) {
    param_1[0x24] = 0;
    param_1[0x25] = 0;
  }
  else if (0x7fffffff < *(int *)(param_1 + 0x24)) {
    param_1[0x24] = 0xffff;
    param_1[0x25] = 0x7fff;
  }
  if (100 < (byte)param_1[0x27]) {
    *(undefined1 *)(param_1 + 0x27) = 100;
  }
  if (100 < (byte)param_1[0x28]) {
    *(undefined1 *)(param_1 + 0x28) = 100;
  }
  if (999 < param_1[0x29]) {
    param_1[0x29] = 999;
  }
  if (999 < param_1[0x2a]) {
    param_1[0x2a] = 999;
  }
  *(undefined1 *)(param_1 + 0x2b) = 0;
  param_1[0x2c] = 0;
  param_1[0x2d] = 0;
  param_1[0x2e] = 0;
  param_1[0x2f] = 0;
  *(undefined1 *)(param_1 + 0x30) = 0;
  *(undefined1 *)((int)param_1 + 0x61) = 0;
  *(undefined1 *)(param_1 + 0x31) = 0;
  *(undefined1 *)((int)param_1 + 99) = 0;
  *(undefined1 *)(param_1 + 0x32) = 0;
  *(undefined1 *)((int)param_1 + 0x65) = 0;
  param_1[0x33] = 0;
  param_1[0x34] = 0;
  param_1[0x36] = 0;
  param_1[0x37] = 0;
  *(undefined1 *)(param_1 + 0x38) = 0;
  param_1[0x39] = 0;
  param_1[0x3a] = 0;
  param_1[0x3c] = 0;
  param_1[0x3d] = 0;
  *(undefined1 *)(param_1 + 0x3e) = 0;
  *(undefined1 *)((int)param_1 + 0x7d) = 0;
  *(undefined1 *)(param_1 + 0x3f) = 0;
  *(undefined1 *)((int)param_1 + 0x7f) = 0;
  param_1[0x40] = 0;
  param_1[0x41] = 0;
  if (0xf < (byte)param_1[0x4a]) {
    *(undefined1 *)(param_1 + 0x4a) = 0xf;
  }
  *(undefined1 *)((int)param_1 + 0x9b) = 0;
  *(undefined1 *)(param_1 + 0x4e) = 0;
  *(undefined1 *)((int)param_1 + 0x9d) = 0;
  *(undefined1 *)(param_1 + 0x4f) = 0;
  *(undefined1 *)((int)param_1 + 0x9f) = 0;
  *(undefined1 *)(param_1 + 0x50) = 0;
  *(undefined1 *)((int)param_1 + 0xa1) = 0;
  *(undefined1 *)(param_1 + 0x51) = 0;
  *(undefined1 *)((int)param_1 + 0xa3) = 0;
  if (0xf < (byte)param_1[0x52]) {
    *(undefined1 *)(param_1 + 0x52) = 0xf;
  }
  param_1[0x53] = 0xffff;
  param_1[0x54] = 0;
  param_1[0x55] = 0;
  param_1[0x56] = 0;
  *(undefined1 *)(param_1 + 0x57) = 0;
  return;
}

