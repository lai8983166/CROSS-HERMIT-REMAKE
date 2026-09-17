
void FUN__text__0047ba20(int param_1,int param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  uint local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  iVar2 = FUN__text__00469a30(param_1);
  if (iVar2 == 0) {
    local_c = (uint)*(byte *)(param_2 + 0x18);
    switch(local_c) {
    case 0:
    case 5:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e48 + 9,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    default:
      iVar2 = FUN__text__00424f80(&DAT_005924d4,
                                  "E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                  DAT_00618e48 + 0x27,0);
      if (iVar2 != 0) {
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
      break;
    case 2:
      if (((*(short *)(param_2 + 2) == 5) &&
          ((iVar2 = FUN__text__0046abc0(param_1,local_8 + 0x80aec +
                                                *(short *)(param_1 + 0x4ee) * 0x520), iVar2 != 0 ||
           (iVar2 = FUN__text__0046ad60(param_1,local_8 + 0x80aec +
                                                *(short *)(param_1 + 0x4ee) * 0x520), iVar2 != 0))))
         || (iVar2 = FUN__text__0046ae20(param_1,local_8 + 0x80aec +
                                                 *(short *)(param_1 + 0x4ee) * 0x520), iVar2 == 0))
      break;
    case 1:
    case 3:
      if (((*(short *)(param_2 + 2) != 5) ||
          ((iVar2 = FUN__text__0046abc0(param_1,local_8 + 0x80aec +
                                                *(short *)(param_1 + 0x4ee) * 0x520), iVar2 == 0 &&
           (iVar2 = FUN__text__0046ad60(param_1,local_8 + 0x80aec +
                                                *(short *)(param_1 + 0x4ee) * 0x520), iVar2 == 0))))
         && (iVar2 = FUN__text__004695d0(local_8 + 0x80aec + *(short *)(param_1 + 0x4ee) * 0x520),
            iVar2 == 0)) {
        FUN__text__004690a0(local_8 + 0x80aec + *(short *)(param_1 + 0x4ee) * 0x520);
      }
      break;
    case 4:
      break;
    case 6:
    }
  }
  local_8 = 0x47bc60;
  FUN__text__0056ce80();
  return;
}

