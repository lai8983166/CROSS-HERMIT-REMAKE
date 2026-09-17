
/* WARNING: Removing unreachable block (ram,0x00480bd0) */

void __thiscall FUN__text__00480a60(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_58 [16];
  uint local_18;
  undefined1 *local_14;
  int local_10;
  uint local_c;
  int local_8;
  
  puVar3 = local_58;
  for (iVar2 = 0x15; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  if (((*(char *)(param_1 + 0x108b48) == '\0') && (*(char *)(param_1 + 0x108b34) != '\0')) &&
     (*(short *)(param_2 + 0x4fe) != 0)) {
    local_18 = (uint)*(byte *)(*(int *)(param_2 + 600) + 0xa4);
    local_8 = param_1;
    switch(local_18) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 8:
    case 9:
    case 10:
    case 0xb:
    case 0xc:
    case 0xd:
    case 0xe:
    case 0xf:
      local_c = FUN__text__00480d00(param_2);
      if (local_c == 4) {
        local_c = 0xffffffff;
      }
      if (local_c == 0xffffffff) {
        iVar2 = FUN__text__00468d80(param_2);
        if (iVar2 == 0) {
          if (*(short *)(param_2 + 0x4fe) < 600) {
            *(short *)(param_2 + 0x4fe) = *(short *)(param_2 + 0x4fe) + 1;
          }
        }
        else if (*(short *)(param_2 + 0x4fe) < 900) {
          *(short *)(param_2 + 0x4fe) = *(short *)(param_2 + 0x4fe) + 1;
        }
        goto LAB__text__00480cd2;
      }
      if ((*(byte *)(*(int *)(param_2 + 600) + 0xa4) == local_c) ||
         (*(short *)(param_2 + 0x4fe) = *(short *)(param_2 + 0x4fe) + -1,
         *(short *)(param_2 + 0x4fe) != 0)) goto LAB__text__00480cd2;
      break;
    case 7:
      local_c = FUN__text__00480d00(param_2);
      if (local_c == 0xffffffff) goto LAB__text__00480cd2;
      *(undefined2 *)(param_2 + 0x4fe) = 0;
      break;
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618ea4 + 100,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      goto LAB__text__00480cd2;
    }
    iVar2 = FUN__text__0048e020(param_2,0xe);
    if (iVar2 == 0) {
      local_10 = FUN__text__00427d60();
      if ((local_10 == 0) &&
         (iVar2 = FUN__text__00424f80("lw!=0","E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                      DAT_00618ea4 + 0x24,0), iVar2 != 0)) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      local_14 = *(undefined1 **)(local_10 + 8);
      *local_14 = 0xe;
      local_14[1] = *(undefined1 *)(param_2 + 2);
      local_14[2] = 0xff;
      *(undefined2 *)(local_14 + 6) = (undefined2)local_c;
      FUN__text__00427e30(local_10);
      FUN__text__0042b2d0(&DAT_0059d80c,*(undefined4 *)(local_8 + 0x2e6f8));
    }
  }
LAB__text__00480cd2:
  local_8 = 0x480cdf;
  FUN__text__0056ce80();
  return;
}

