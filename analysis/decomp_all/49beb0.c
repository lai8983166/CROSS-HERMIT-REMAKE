
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

void __fastcall FUN__text__0049beb0(int param_1)

{
  byte bVar1;
  ushort uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_8c [16];
  undefined1 local_4c [32];
  undefined *local_2c;
  int local_28;
  undefined4 local_24;
  int local_20;
  uint local_1c;
  uint local_18;
  int local_14;
  uint local_10;
  uint local_c;
  int local_8;
  
  puVar4 = local_8c;
  for (iVar3 = 0x22; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  if (*(char *)(param_1 + 0x108b48) == '\0') {
    local_8 = param_1;
    FUN__text__004077c0(DAT_007a49fc);
    *(undefined2 *)(local_8 + 0xde708) = 0;
    if (*(int *)(local_8 + 0x108b50) != 0) {
      local_28 = 0;
      for (local_c = 0; local_c != *(uint *)(local_8 + 0x108b50); local_c = local_c + 1) {
        local_24 = *(undefined4 *)(local_8 + 0x108b60 + local_c * 4);
        iVar3 = FUN__text__00468d80(local_24);
        if ((iVar3 != 0) && (iVar3 = FUN__text__004690a0(local_24), iVar3 == 0)) {
          local_28 = *(int *)(local_8 + 0x108b60 + local_c * 4);
          break;
        }
      }
      if (local_28 == 0) {
        local_28 = *(int *)(local_8 + 0x108b60);
      }
      local_20 = local_28;
      iVar3 = FUN__text__00468d80(local_28);
      if (iVar3 != 0) {
        *(undefined2 *)(local_8 + 0xde726) = 199;
        *(undefined1 *)(local_8 + 0xde717) = 0xff;
        *(undefined4 *)(local_8 + 0xde70c) = 0;
        if (*(char *)(*(int *)(local_20 + 600) + 0x9d) != '\0') {
          *(undefined1 *)(local_8 + 0xde716) = 0x80;
          *(undefined1 *)(local_8 + 0xde715) = 0x80;
          *(undefined1 *)(local_8 + 0xde714) = 0x80;
          FUN__text__00407870(0x5a,DAT_0061ae58);
          FUN__text__004079c0(_DAT_0061adb8,_DAT_0061adbc);
        }
        *(undefined1 *)(local_8 + 0xde716) = 0x80;
        *(undefined1 *)(local_8 + 0xde715) = 0x80;
        *(undefined1 *)(local_8 + 0xde714) = 0x80;
        bVar1 = *(byte *)(*(int *)(local_20 + 600) + 0x9f);
        local_1c = CONCAT31(local_1c._1_3_,bVar1);
        FUN__text__00407870(0x5a,bVar1 + 0xc3);
        FUN__text__004079c0(*(undefined4 *)(&DAT_0061ae18 + (local_1c & 0xff) * 8),
                            *(undefined4 *)(&DAT_0061ae1c + (local_1c & 0xff) * 8));
        for (local_c = 0; local_c != 8; local_c = local_c + 1) {
          local_18 = 0;
          uVar2 = *(ushort *)(*(int *)(local_20 + 600) + 0x84 + local_c * 2);
          local_10 = (uint)uVar2;
          if ((uVar2 & 0x7fff) == 0) {
            local_14 = 0xeb;
          }
          else if ((uVar2 & 0x8000) == 0) {
            local_14 = (local_10 & 0x7fff) + 0xeb;
            iVar3 = (local_10 & 0x7fff) * 0x48;
            local_2c = &DAT_006c2dc8 + iVar3;
            local_18 = (uint)(*(short *)(*(int *)(local_20 + 600) + 0x1c) <
                             *(short *)(&DAT_006c2dd0 + iVar3));
            if ((&DAT_006c2dcd)[iVar3] == '\x03') {
              *(undefined1 *)(local_8 + 0xde716) = 0x80;
              *(undefined1 *)(local_8 + 0xde715) = 0x80;
              *(undefined1 *)(local_8 + 0xde714) = 0x80;
              FUN__text__00407870(0x5a,0x242);
              FUN__text__004079c0(*(int *)(&DAT_0061add8 + local_c * 8) + 3,
                                  *(int *)(&DAT_0061addc + local_c * 8) + 0x16);
            }
            else {
              FUN__text__0056d810(local_4c,&PTR_DAT_005a042c,(int)*(short *)(&DAT_006c2dd0 + iVar3))
              ;
              FUN__text__0040ec50(*(int *)(&DAT_0061add8 + local_c * 8) + 0x10,
                                  *(int *)(&DAT_0061addc + local_c * 8) + 0x18,199,0xffffffff,1,
                                  local_4c);
            }
          }
          else {
            local_14 = (local_10 & 0x7fff) + 0x14f;
          }
          if (*(byte *)(*(int *)(local_20 + 600) + 0x9e) == local_c) {
            *(undefined1 *)(local_8 + 0xde716) = 0x80;
            *(undefined1 *)(local_8 + 0xde715) = 0x80;
            *(undefined1 *)(local_8 + 0xde714) = 0x80;
          }
          else {
            *(undefined1 *)(local_8 + 0xde716) = 0x40;
            *(undefined1 *)(local_8 + 0xde715) = 0x40;
            *(undefined1 *)(local_8 + 0xde714) = 0x40;
          }
          if (local_18 != 0) {
            *(char *)(local_8 + 0xde715) = (char)((int)(uint)*(byte *)(local_8 + 0xde715) >> 1);
            *(char *)(local_8 + 0xde714) = (char)((int)(uint)*(byte *)(local_8 + 0xde714) >> 1);
          }
          FUN__text__00407870(0x5a,local_14);
          FUN__text__004079c0(*(undefined4 *)(&DAT_0061add8 + local_c * 8),
                              *(undefined4 *)(&DAT_0061addc + local_c * 8));
        }
      }
    }
    if (*(char *)(local_8 + 0x2f156) != '\0') {
      *(undefined2 *)(local_8 + 0xde726) = 199;
      *(undefined1 *)(local_8 + 0xde716) = 0x80;
      *(undefined1 *)(local_8 + 0xde715) = 0x80;
      *(undefined1 *)(local_8 + 0xde714) = 0x80;
      FUN__text__00407870(0x5a,DAT_0061ae5a);
      FUN__text__004079c0(DAT_0061adc0,DAT_0061adc4);
    }
    if (*(char *)(local_8 + 0x2f157) != '\0') {
      *(undefined2 *)(local_8 + 0xde726) = 199;
      *(undefined1 *)(local_8 + 0xde716) = 0x80;
      *(undefined1 *)(local_8 + 0xde715) = 0x80;
      *(undefined1 *)(local_8 + 0xde714) = 0x80;
      FUN__text__00407870(0x5a,DAT_0061ae5c);
      FUN__text__004079c0(_DAT_0061adc8,DAT_0061adcc);
    }
  }
  local_8 = 0x49c3f5;
  FUN__text__0056ce80();
  return;
}

