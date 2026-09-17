
void __fastcall FUN__text__00490fc0(int param_1)

{
  ushort uVar1;
  code *pcVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_68 [16];
  uint local_28;
  short local_24;
  short local_20;
  short local_1c;
  uint local_18;
  uint local_14;
  int local_10;
  undefined *local_c;
  int local_8;
  
  puVar4 = local_68;
  for (iVar3 = 0x19; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if (((((*(short *)(param_1 + 0x2a316) != -1) && (*(short *)(param_1 + 0x2a318) != -1)) &&
       (*(int *)(param_1 + 0x108b50) == 1)) &&
      ((iVar3 = FUN__text__0046a430(*(undefined4 *)(param_1 + 0x108b60)), iVar3 != 0 &&
       (iVar3 = FUN__text__004695d0(*(undefined4 *)(local_8 + 0x108b60)), iVar3 == 0)))) &&
     (iVar3 = FUN__text__004690a0(*(undefined4 *)(local_8 + 0x108b60)), iVar3 == 0)) {
    local_10 = *(int *)(local_8 + 0x108b60);
    local_18 = (uint)*(short *)(&DAT_006b2da0 +
                               (uint)*(ushort *)(*(int *)(local_10 + 600) + 0xc) * 0x40);
    if (*(char *)(*(int *)(local_10 + 600) + 0x9d) == '\0') goto LAB__text__0049109b;
    uVar1 = *(ushort *)
             (*(int *)(local_10 + 600) + 0x84 + (uint)*(byte *)(*(int *)(local_10 + 600) + 0x9e) * 2
             );
    local_14 = (uint)uVar1;
    if ((uVar1 & 0x8000) == 0) {
      if (local_14 == 0) {
        local_14 = local_18;
      }
      while( true ) {
        local_c = &DAT_006c2dc8 + local_14 * 0x48;
        if (local_14 == local_18) break;
        local_1c = (short)((int)((int)*(short *)(local_8 + 0x2a316) +
                                ((int)*(short *)(local_8 + 0x2a316) >> 0x1f & 0x1fU)) >> 5);
        local_20 = (short)((int)((int)*(short *)(local_8 + 0x2a318) +
                                ((int)*(short *)(local_8 + 0x2a318) >> 0x1f & 0xfU)) >> 4);
        if (((&DAT_006c2de0)[local_14 * 0x48] != '\x04') &&
           (iVar3 = FUN__text__0043c160((int)local_1c,(int)local_20), iVar3 == 0)) {
          *(undefined1 *)(local_8 + 0x30994) = 0;
          goto LAB__text__00491290;
        }
        if (local_c[5] != '\x03') {
          local_28 = (uint)(byte)local_c[0x18];
          switch(local_28) {
          case 0:
            iVar3 = FUN__text__00424f80(&DAT_005924d4,
                                        "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlCursor.cpp",
                                        DAT_006191f8 + 0x3d,0);
            if (iVar3 != 0) {
              pcVar2 = (code *)swi(3);
              (*pcVar2)();
              return;
            }
            break;
          case 1:
            FUN__text__004913f0(local_10,local_c);
            break;
          case 2:
            FUN__text__00491440(local_10,local_c,local_18,local_14);
            break;
          case 3:
            FUN__text__004914d0(local_10,local_c);
            break;
          case 4:
            FUN__text__00491570(local_10,local_c);
            break;
          case 5:
            FUN__text__004915a0(local_10,local_c);
            break;
          case 6:
            FUN__text__00491600(local_10,local_c);
          }
          local_24 = *(short *)(local_c + 8);
          if (*(short *)(*(int *)(local_10 + 600) + 0x1c) < local_24) {
            *(undefined1 *)(local_8 + 0x30995) = 1;
          }
          else {
            *(undefined1 *)(local_8 + 0x30995) = 0;
          }
          goto LAB__text__00491290;
        }
LAB__text__0049109b:
        local_14 = local_18;
      }
      FUN__text__004912c0(local_10,local_c,local_18);
      *(undefined1 *)(local_8 + 0x30995) = 0;
      goto LAB__text__00491290;
    }
  }
  *(undefined1 *)(local_8 + 0x30994) = 0;
LAB__text__00491290:
  local_8 = 0x49129d;
  FUN__text__0056ce80();
  return;
}

