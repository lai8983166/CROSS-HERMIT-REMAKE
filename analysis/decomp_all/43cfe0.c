
void __thiscall FUN__text__0043cfe0(int param_1,int *param_2)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  int local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if ((*(int *)(param_1 + 0x2659c) == 0) &&
     (iVar2 = FUN__text__00424f80("MapCw!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ffa10 + 1,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  local_c = FUN__text__00428a40((int)*(short *)(*(int *)(local_8 + 0x2659c) + 4) *
                                (int)*(short *)(*(int *)(local_8 + 0x2659c) + 6));
  *param_2 = local_c;
  if ((*param_2 == 0) &&
     (iVar2 = FUN__text__00424f80("*pt!=0","E:\\CrossHermit\\GAME\\src\\yoshida\\MapCtrl.cpp",
                                  DAT_005ffa10 + 3,0), iVar2 != 0)) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
  if (*param_2 != 0) {
    FUN__text__0043d0c0(*param_2);
  }
  local_8 = 0x43d0b6;
  FUN__text__0056ce80();
  return;
}

