
void __fastcall FUN__text__004568c0(int param_1)

{
  code *pcVar1;
  int iVar2;
  undefined4 *puVar3;
  undefined4 local_50 [16];
  int local_10;
  int local_c;
  int local_8;
  
  puVar3 = local_50;
  for (iVar2 = 0x13; iVar2 != 0; iVar2 = iVar2 + -1) {
    *puVar3 = 0xcccccccc;
    puVar3 = puVar3 + 1;
  }
  local_c = *(int *)(param_1 + 0x60) + 0x2450;
  for (local_10 = 0; local_10 != 0x20; local_10 = local_10 + 1) {
    if (*(short *)(local_c + local_10 * 2) == -1) goto LAB__text__0045694f;
  }
  local_8 = param_1;
  iVar2 = FUN__text__00424f80(&DAT_0059a6ac,"E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                              DAT_0060cdbc + 9,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
LAB__text__0045694f:
  local_8 = 0x45695c;
  FUN__text__0056ce80();
  return;
}

