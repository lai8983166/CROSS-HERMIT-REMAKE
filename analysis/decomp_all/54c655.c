
void FUN__text__0054c655(int param_1,undefined4 param_2,int param_3)

{
  byte bVar1;
  uint uVar2;
  uint uVar3;
  undefined1 local_20 [4];
  undefined1 local_1c [4];
  byte local_18;
  byte local_17;
  byte local_16;
  byte local_15;
  byte local_14;
  uint local_10;
  uint local_c;
  uint local_8;
  
  if (*(int *)(param_1 + 0x58) != 0) {
    FUN__text__0054381d(param_1,"Out of place IHDR");
  }
  if (param_3 != 0xd) {
    FUN__text__0054381d(param_1,"Invalid IHDR chunk");
  }
  *(uint *)(param_1 + 0x58) = *(uint *)(param_1 + 0x58) | 1;
  FUN__text__0054bcf9(param_1,local_20,0xd);
  FUN__text__0054c5c9(param_1,0);
  uVar2 = FUN__text__0054bcc3(local_20);
  uVar3 = FUN__text__0054bcc3(local_1c);
  local_10 = (uint)local_16;
  local_c = (uint)local_15;
  local_8 = (uint)local_14;
  if ((((uVar2 == 0) || (0x7fffffff < uVar2)) || (uVar3 == 0)) || (0x7fffffff < uVar3)) {
    FUN__text__0054381d(param_1,"Invalid image size in IHDR");
  }
  if (((local_18 != 1) && (local_18 != 2)) &&
     ((local_18 != 4 && ((local_18 != 8 && (local_18 != 0x10)))))) {
    FUN__text__0054381d(param_1,"Invalid bit depth in IHDR");
  }
  if (((local_17 == 1) || (local_17 == 5)) || (6 < local_17)) {
    FUN__text__0054381d(param_1,"Invalid color type in IHDR");
  }
  if (((local_17 == 3) && (8 < local_18)) ||
     (((local_17 == 2 || ((local_17 == 4 || (local_17 == 6)))) && (local_18 < 8)))) {
    FUN__text__0054381d(param_1,"Invalid color type/bit depth combination in IHDR");
  }
  if (1 < (int)local_8) {
    FUN__text__0054381d(param_1,"Unknown interlace method in IHDR");
  }
  if (local_10 != 0) {
    FUN__text__0054381d(param_1,"Unknown compression method in IHDR");
  }
  if (local_c != 0) {
    FUN__text__0054381d(param_1,"Unknown filter method in IHDR");
  }
  *(undefined1 *)(param_1 + 0x113) = (undefined1)local_8;
  *(uint *)(param_1 + 0xb8) = uVar2;
  *(uint *)(param_1 + 0xbc) = uVar3;
  *(byte *)(param_1 + 0x117) = local_18;
  *(byte *)(param_1 + 0x116) = local_17;
  if (local_17 != 0) {
    if (local_17 == 2) {
      *(undefined1 *)(param_1 + 0x11a) = 3;
      goto LAB__text__0054c80d;
    }
    if (local_17 != 3) {
      if (local_17 == 4) {
        *(undefined1 *)(param_1 + 0x11a) = 2;
      }
      else if (local_17 == 6) {
        *(undefined1 *)(param_1 + 0x11a) = 4;
      }
      goto LAB__text__0054c80d;
    }
  }
  *(undefined1 *)(param_1 + 0x11a) = 1;
LAB__text__0054c80d:
  bVar1 = *(char *)(param_1 + 0x11a) * local_18;
  *(byte *)(param_1 + 0x119) = bVar1;
  *(uint *)(param_1 + 200) = bVar1 * uVar2 + 7 >> 3;
  FUN__text__00546405(param_1,param_2,uVar2,uVar3,local_18,local_17,local_8,local_10,local_c);
  return;
}

