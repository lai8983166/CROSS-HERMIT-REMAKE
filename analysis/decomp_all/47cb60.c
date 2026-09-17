
void __thiscall FUN__text__0047cb60(int param_1,int param_2,uint param_3)

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
  local_c = param_3 & 0xff;
  local_8 = param_1;
  switch(local_c) {
  case 0:
  case 4:
  case 5:
  case 6:
    break;
  case 1:
  case 2:
  case 3:
    iVar2 = FUN__text__00468d10(param_1 + 0x80aec + *(short *)(param_2 + 0x4ee) * 0x520);
    if ((iVar2 != 0) &&
       (iVar2 = FUN__text__00469480(local_8 + 0x80aec + *(short *)(param_2 + 0x4ee) * 0x520),
       iVar2 != 0)) {
      FUN__text__0046ae20(param_2,local_8 + 0x80aec + *(short *)(param_2 + 0x4ee) * 0x520);
    }
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\SRC\\YOSHIDA\\UnitCtrlAi.Cpp",
                                DAT_00618e64 + 0x14,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x47cc63;
  FUN__text__0056ce80();
  return;
}

