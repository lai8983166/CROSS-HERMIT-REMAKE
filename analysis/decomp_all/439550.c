
void __thiscall FUN__text__00439550(int param_1,undefined4 param_2,undefined4 param_3,int param_4)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_54 [16];
  undefined4 local_14;
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_54;
  for (iVar2 = 0x14; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  *(undefined4 *)(param_1 + 0x30) = param_2;
  *(undefined4 *)(param_1 + 0x34) = param_3;
  *(int *)(param_1 + 0x2c) = *(int *)(param_1 + 0x30) * *(int *)(param_1 + 0x34);
  local_8 = param_1;
  local_10 = FUN__text__00427650(*(undefined4 *)(param_1 + 0x2c));
  if ((local_10 != 0) &&
     (iVar2 = FUN__text__00424f80(&DAT_0059544c,"E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                  DAT_005ff9b4 + 8,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  for (local_c = 0; local_c != *(int *)(local_8 + 0x2c); local_c = local_c + 1) {
    FUN__text__00427890(local_c,param_4 + local_c * 0x1c);
  }
  local_14 = FUN__text__00428a40(*(int *)(local_8 + 0x30) * *(int *)(local_8 + 0x34) * 4);
  *(undefined4 *)(local_8 + 0x88) = local_14;
  if ((*(int *)(local_8 + 0x88) == 0) &&
     (iVar2 = FUN__text__00424f80("NodePos!=0","E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                  DAT_005ff9b4 + 0xf,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*(int *)(local_8 + 0x88) == 0) {
    iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\YOSHIDA\\FindPath.CPP",
                                DAT_005ff9b4 + 0x1a,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
    FUN__text__004394a0();
  }
  else {
    FUN__text__00439790();
  }
  local_8 = 0x4396d1;
  FUN__text__0056ce80();
  return;
}

