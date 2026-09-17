
void FUN__text__0046c290(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined4 local_c;
  undefined4 local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = FUN__text__0046a950(param_1);
  switch(local_c) {
  case 0:
  case 4:
    *(undefined1 *)(param_1 + 0x28a) = 3;
    break;
  case 1:
    *(undefined1 *)(param_1 + 0x28a) = 6;
    break;
  case 2:
    *(undefined1 *)(param_1 + 0x28a) = 9;
    break;
  case 3:
    *(undefined1 *)(param_1 + 0x28a) = 2;
    break;
  default:
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\UnitCtrl.cpp",
                                DAT_00618c08 + 0x11,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_8 = 0x46c336;
  FUN__text__0056ce80();
  return;
}

