
void __thiscall
FUN__text__00455420(int param_1,int param_2,undefined1 param_3,char param_4,int param_5)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_4c [16];
  undefined1 *local_c;
  int local_8;
  
  puVar3 = local_4c;
  for (iVar2 = 0x12; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_8 = param_1;
  if (param_5 < 1) {
    iVar2 = FUN__text__00424f80("0 < timer","E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                                DAT_0060cda0 + 3,0);
    if (iVar2 != 0) {
      pcVar1 = (code *)swi(3);
      (*pcVar1)();
      return;
    }
  }
  local_c = (undefined1 *)(*(int *)(local_8 + 0x60) + 0x20ec + param_2 * 8);
  *local_c = 1;
  local_c[1] = param_3;
  *(short *)(local_c + 2) = (short)param_4;
  *(int *)(local_c + 4) = param_5;
  local_8 = 0x4554ab;
  FUN__text__0056ce80();
  return;
}

