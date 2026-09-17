
void __thiscall FUN__text__0040dcd0(int *param_1,int param_2)

{
  code *pcVar1;
  uint uVar2;
  int iVar3;
  undefined4 *puVar4;
  undefined4 local_50 [16];
  int local_10;
  uint local_c;
  int *local_8;
  
  puVar4 = local_50;
  for (iVar3 = 0x13; iVar3 != 0; iVar3 = iVar3 + -1) {
    *puVar4 = 0xcccccccc;
    puVar4 = puVar4 + 1;
  }
  local_8 = param_1;
  if ((*(short *)(*param_1 + 0xb28e) != 1) &&
     (iVar3 = FUN__text__00424f80("DxSys->DrawMode == 1",
                                  "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                                  DAT_005ff34c + 4,0), iVar3 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (local_8[5] != 0) {
    local_c = local_8[5] + local_8[3];
    local_10 = param_2 + -1;
    switch(local_10) {
    case 0:
      uVar2 = local_8[0xc] + 0x5c;
      break;
    case 1:
      uVar2 = local_8[0xc] + 0x18;
      break;
    case 2:
      uVar2 = local_8[0xc] + 0x14;
      break;
    case 3:
      uVar2 = local_8[0xc] + 0x18;
      break;
    case 4:
      uVar2 = local_8[0xc] + 0x24;
      break;
    case 5:
      uVar2 = local_8[0xc] + 0x24;
      break;
    case 6:
      uVar2 = local_8[0xc] + 0x14;
      break;
    case 7:
      uVar2 = local_8[0xc] + 0x18;
      break;
    case 8:
      uVar2 = local_8[0xc] + 0x10;
      break;
    default:
      goto switchD__text__0040dd5a_default;
    }
    if (uVar2 < local_c) goto LAB__text__0040de7e;
  }
switchD__text__0040dd5a_default:
  iVar3 = FUN__text__00424f80(&DAT_005924d4,
                              "E:\\CrossHermit\\GAME\\src\\system\\directx\\DxDraw.cpp",
                              DAT_005ff34c + 0x2c,0);
  if (iVar3 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
LAB__text__0040de7e:
  local_8 = (int *)0x40de8b;
  FUN__text__0056ce80();
  return;
}

