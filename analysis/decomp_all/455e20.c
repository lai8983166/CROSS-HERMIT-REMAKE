
void __fastcall FUN__text__00455e20(int param_1)

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
  local_c = *(int *)(param_1 + 0x60) + 0x2234;
  for (local_10 = 0; local_10 != 0x20; local_10 = local_10 + 1) {
    if (*(char *)(local_c + local_10 * 0x10) == -1) goto LAB__text__00455ead;
  }
  local_8 = param_1;
  iVar2 = FUN__text__00424f80(&DAT_005924d4,"E:\\CrossHermit\\GAME\\src\\yoshida\\TacticsTask.cpp",
                              DAT_0060cdac + 8,0);
  if (iVar2 != 0) {
    pcVar1 = (code *)swi(3);
    (*pcVar1)();
    return;
  }
LAB__text__00455ead:
  local_8 = 0x455eba;
  FUN__text__0056ce80();
  return;
}

